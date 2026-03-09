import os
import sys
import shutil
import glob
import subprocess
import json
import logging

APP_NAME = "Quick DigitalSignature GUI"  # Needed for config path

logger = logging.getLogger(__name__)

# --- Resource helpers ---
def get_resource_dir() -> str:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def get_program_dir() -> str:
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def resource_path(filename: str) -> str:
    return os.path.join(get_resource_dir(), filename)

# --- Config management ---
def get_config_path() -> str:
    app_data_dir = os.path.join(os.environ.get("APPDATA", ""), APP_NAME)
    os.makedirs(app_data_dir, exist_ok=True)
    return os.path.join(app_data_dir, "config.json")

def save_config(config_data: dict):
    config_path = get_config_path()
    try:
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        logger.warning(f"Could not save config to {config_path}: {e}")

def load_config() -> dict:
    config_path = get_config_path()
    if not os.path.isfile(config_path):
        return {}
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Could not load or parse config from {config_path}: {e}")
        return {}

import base64
try:
    import win32crypt
    DPAPI_AVAILABLE = True
except ImportError:
    DPAPI_AVAILABLE = False
    logger.warning("pywin32 not installed. Password encryption will not be available.")

def is_dpapi_available() -> bool:
    """Checks if the necessary encryption modules are available."""
    return DPAPI_AVAILABLE

def encrypt_password(password: str) -> str | None:
    """Encrypts a password using DPAPI and returns a Base64 encoded string."""
    if not is_dpapi_available() or not password:
        return None
    try:
        data_bytes = password.encode('utf-8')
        # The flag 0x1 is CRYPTPROTECT_UI_FORBIDDEN
        encrypted_bytes = win32crypt.CryptProtectData(data_bytes, None, None, None, None, 0x1)
        return base64.b64encode(encrypted_bytes).decode('ascii')
    except Exception as e:
        logger.error(f"Error encrypting password: {e}", exc_info=True)
        return None

def decrypt_password(encrypted_password_b64: str) -> str | None:
    """Decrypts a Base64 encoded password string that was encrypted with DPAPI."""
    if not is_dpapi_available() or not encrypted_password_b64:
        return None
    try:
        encrypted_bytes = base64.b64decode(encrypted_password_b64)
        # The flag 0x1 is CRYPTPROTECT_UI_FORBIDDEN
        decrypted_bytes, _ = win32crypt.CryptUnprotectData(encrypted_bytes, None, None, None, None, 0x1)
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        logger.error(f"Error decrypting password: {e}", exc_info=True)
        return None

class SignToolWrapper:
    """Encapsulates all business logic for finding and running signtool.exe."""

    def __init__(self):
        self.signtool_path = self._find_signtool()
        if self.signtool_path:
            logger.info(f"SignTool found at: {self.signtool_path}")

    def is_signtool_found(self) -> bool:
        return self.signtool_path is not None

    def _sdk_signtool_candidates(self) -> list[str]:
        pf_roots = []
        for env in ("ProgramFiles(x86)", "ProgramFiles", "ProgramW6432"):
            v = os.environ.get(env, "")
            if v and v not in pf_roots:
                pf_roots.append(v)
        archs = ["x64", "x86", "arm64", "arm"]
        candidates = []
        for root in pf_roots:
            sdk_bin = os.path.join(root, "Windows Kits", "10", "bin")
            for arch in archs:
                for versioned in sorted(glob.glob(os.path.join(sdk_bin, "10.*", arch))):
                    candidates.append(os.path.join(versioned, "signtool.exe"))
                candidates.append(os.path.join(sdk_bin, arch, "signtool.exe"))
            for sdk8 in ("Windows Kits\\8.1", "Windows Kits\\8.0"):
                for arch in archs:
                    candidates.append(os.path.join(root, sdk8, "bin", arch, "signtool.exe"))
            candidates += [
                os.path.join(root, "Microsoft SDKs", "Windows", "v10.0A", "bin", "NETFX 4.8 Tools", "x64", "signtool.exe"),
                os.path.join(root, "Microsoft SDKs", "Windows", "v10.0A", "bin", "NETFX 4.8 Tools", "signtool.exe"),
                os.path.join(root, "Microsoft SDKs", "ClickOnce", "SignTool", "signtool.exe"),
            ]
        return candidates

    def _find_signtool(self) -> str | None:
        bundled = resource_path("SignTool.exe")
        if os.path.isfile(bundled):
            return bundled
        prog_dir = get_program_dir()
        local = os.path.join(prog_dir, "signtool.exe")
        if os.path.isfile(local):
            return local
        logger.info("Searching for signtool.exe in Windows SDK paths...")
        for candidate in reversed(self._sdk_signtool_candidates()):
            if os.path.isfile(candidate):
                return candidate
        return shutil.which("signtool.exe")

    def _standard_cert_dirs(self) -> list[tuple[str, str]]:
        dirs = []
        def _add(path: str, label: str):
            if path and os.path.isdir(path):
                dirs.append((os.path.normpath(path), label))
        profile = os.environ.get("USERPROFILE", "")
        appdata = os.environ.get("APPDATA", "")
        public  = os.environ.get("PUBLIC", "")
        _add(os.path.join(profile, ".certificates"), "%USERPROFILE%\\.certificates")
        _add(os.path.join(profile, "certificates"), "%USERPROFILE%\\certificates")
        _add(os.path.join(profile, "Desktop"), "Desktop")
        _add(os.path.join(appdata, "certificates"), "%APPDATA%\\certificates")
        _add(os.path.join(public,  "Desktop"), "Public Desktop")
        return dirs

    def find_certificates(self, extra_dir: str | None = None) -> list[dict]:
        search_dirs: list[tuple[str, str]] = []
        resource_dir = get_resource_dir()
        search_dirs.append((resource_dir, "bundled"))
        prog_dir = get_program_dir()
        if os.path.normpath(prog_dir) != os.path.normpath(resource_dir):
            search_dirs.append((prog_dir, "program dir"))
        certs_subdir = os.path.join(prog_dir, "certs")
        if os.path.isdir(certs_subdir):
            search_dirs.append((certs_subdir, "certs/"))
        already = {os.path.normpath(d) for d, _ in search_dirs}
        for d, label in self._standard_cert_dirs():
            if os.path.normpath(d) not in already:
                search_dirs.append((d, label))
                already.add(os.path.normpath(d))
        if extra_dir and os.path.isdir(extra_dir) and os.path.normpath(extra_dir) not in already:
            search_dirs.append((extra_dir, extra_dir))
        found: dict[str, dict] = {}
        for directory, source in search_dirs:
            try:
                logger.info(f"Searching for .pfx certificates in: {directory} (source: {source})")
                for fname in os.listdir(directory):
                    if fname.lower().endswith(".pfx"):
                        full = os.path.join(directory, fname)
                        real = os.path.realpath(full)
                        if os.path.isfile(full) and real not in found:
                            found[real] = {"name": fname, "path": full, "source": source}
            except OSError:
                logger.warning(f"Could not access or read directory: {directory}")
        return list(found.values())

    def sign_file(self, input_path: str, pfx_path: str, password: str | None) -> tuple[int, str, str]:
        if not self.signtool_path:
            raise FileNotFoundError("SignTool.exe not found.")
        cmd = [self.signtool_path, "sign", "/fd", "sha256", "/f", pfx_path]
        if password:
            cmd.extend(["/p", password])
        cmd.extend(["/tr", "http://timestamp.digicert.com", "/td", "sha256", input_path])
        logger.info(f"Executing SignTool command: {' '.join(cmd[:-3])} ...") # Don't log password or file path
        result = subprocess.run(
            cmd, capture_output=True, text=True, shell=False,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
        return result.returncode, result.stdout, result.stderr

    def verify_signature(self, input_path: str, verify_timestamp: bool) -> tuple[int, str, str]:
        if not self.signtool_path:
            raise FileNotFoundError("SignTool.exe not found.")
        cmd = [self.signtool_path, "verify", "/pa"]
        if verify_timestamp:
            cmd.append("/tw")
        cmd.extend(["/v", input_path])
        logger.info(f"Executing SignTool command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd, capture_output=True, text=True, shell=False,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
        return result.returncode, result.stdout, result.stderr

    def install_certificate(self, store_name: str, cert_path: str) -> tuple[int, str, str, bool]:
        try:
            logger.info(f"Executing certutil to install '{cert_path}' into '{store_name}' store.")
            r = subprocess.run(
                ["certutil", "-addstore", store_name, cert_path],
                capture_output=True, text=True, shell=False,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
            if r.returncode == 0:
                return r.returncode, r.stdout, r.stderr, False
            err = (r.stderr or "").lower()
            out = (r.stdout or "").lower()
            if ("access is denied" in err or "denied" in err or
                "requires elevation" in err or "requires elevation" in out or
                "administrator permissions" in out):
                logger.warning("System store access denied, retrying with user store.")
                r2 = subprocess.run(
                    ["certutil", "-user", "-addstore", store_name, cert_path],
                    capture_output=True, text=True, shell=False,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
                )
                return r2.returncode, r2.stdout, r2.stderr, True
            return r.returncode, r.stdout, r.stderr, False
        except Exception as e:
            logger.error(f"Failed to run certutil.exe: {e}", exc_info=True)
            return -1, "", str(e), False