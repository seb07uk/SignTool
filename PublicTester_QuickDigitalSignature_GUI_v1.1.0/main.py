import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import shutil
import glob
import logging
from PIL import Image, ImageTk

APP_NAME    = "PublicTester QuickDigital Signature GUI"
APP_VERSION = "1.1.0"
APP_AUTHOR  = "PublicTester QuickDigital Signature"

# ---------------------------------------------------------------------------
# Colour palette  (FIX: all colours in one place, consistent hex notation)
# ---------------------------------------------------------------------------

COLOR_PRIMARY  = "#0078D4"   # Microsoft Blue
COLOR_SUCCESS  = "#006400"   # Dark green
COLOR_ERROR    = "#C00000"   # Dark red  (FIX: was bare "red" in several places)
COLOR_BG       = "#F0F0F0"   # Light grey background
COLOR_BORDER   = "#CCCCCC"   # Separator / border
COLOR_BTN      = "#E1E1E1"   # Button background
COLOR_GREY_TXT = "grey"      # Footer / hint text

# ---------------------------------------------------------------------------
# Logging  (FIX: added file-based logging for troubleshooting)
# ---------------------------------------------------------------------------

logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "sign.log"),
    level=logging.DEBUG,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Resource helpers
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Standard Windows SDK / WDK search paths for signtool.exe
# ---------------------------------------------------------------------------

def _sdk_signtool_candidates() -> list[str]:
    """
    Return candidate paths for signtool.exe from standard Windows SDK / WDK
    installations (x64, x86, arm64).  Supports SDK versions 8.0 – 11+.
    Uses glob so it works even when the exact version sub-folder is unknown.
    """
    pf_roots = []
    for env in ("ProgramFiles(x86)", "ProgramFiles", "ProgramW6432"):
        v = os.environ.get(env, "")
        if v and v not in pf_roots:
            pf_roots.append(v)

    archs = ["x64", "x86", "arm64", "arm"]

    candidates = []
    for root in pf_roots:

        # Legacy WDK / Visual Studio integrated signtool
        candidates += [
            os.path.join(root, "Microsoft SDKs", "Windows", "v10.0A", "bin",
                         "NETFX 4.8 Tools", "x64", "signtool.exe"),
            os.path.join(root, "Microsoft SDKs", "Windows", "v10.0A", "bin",
                         "NETFX 4.8 Tools", "signtool.exe"),
            os.path.join(root, "Microsoft SDKs", "ClickOnce", "SignTool", "signtool.exe"),
        ]
        # Windows 8.x SDK
        for sdk8 in ("Windows Kits\\8.1", "Windows Kits\\8.0"):
            for arch in archs:
                candidates.append(os.path.join(root, sdk8, "bin", arch, "signtool.exe"))

        # Windows 10+ SDK (prefer newest; appended last so reversed() checks newest first)
        sdk_bin = os.path.join(root, "Windows Kits", "10", "bin")
        for arch in archs:
            versioned_dirs = glob.glob(os.path.join(sdk_bin, "10.*", arch))

            def _ver_key(path: str) -> tuple:
                folder = os.path.basename(os.path.dirname(path))
                try:
                    return tuple(int(x) for x in folder.split("."))
                except ValueError:
                    return (0,)
            for versioned in sorted(versioned_dirs, key=_ver_key):
                candidates.append(os.path.join(versioned, "signtool.exe"))
            candidates.append(os.path.join(sdk_bin, arch, "signtool.exe"))
 



# ---------------------------------------------------------------------------
# Locate signtool
# ---------------------------------------------------------------------------

def znajdz_signtool() -> str | None:
    # 1. Bundled inside PyInstaller EXE
    # FIX: unified filename casing — use lowercase "signtool.exe" everywhere.
    # On NTFS (case-insensitive) both work, but consistency avoids confusion.
    bundled = resource_path("signtool.exe")
    if os.path.isfile(bundled):
        log.debug("signtool found (bundled): %s", bundled)
        return bundled

    # 2. Same folder as the running EXE / script
    prog_dir = get_program_dir()
    local = os.path.join(prog_dir, "signtool.exe")
    if os.path.isfile(local):
        log.debug("signtool found (local): %s", local)
        return local

    # 3. Standard Windows SDK / WDK paths (newest version preferred)
    for candidate in reversed(_sdk_signtool_candidates()):
        if os.path.isfile(candidate):
            log.debug("signtool found (SDK): %s", candidate)
            return candidate

    # 4. System PATH
    found = shutil.which("signtool.exe")
    if found:
        log.debug("signtool found (PATH): %s", found)
        return found

    log.warning("signtool.exe not found anywhere")
    return None


# ---------------------------------------------------------------------------
# Standard search roots for .pfx certificates
# ---------------------------------------------------------------------------

def _standard_cert_dirs() -> list[tuple[str, str]]:
    """
    Return (directory, label) pairs for well-known certificate locations:
      - User profile  : %USERPROFILE%\\.certificates  and  Desktop
      - AppData roaming: %APPDATA%\\certificates
      - Public desktop : %PUBLIC%\\Desktop
    Only existing directories are included.
    """
    dirs = []

    def _add(path: str, label: str):
        if path and os.path.isdir(path):
            dirs.append((os.path.normpath(path), label))

    profile = os.environ.get("USERPROFILE", "")
    appdata = os.environ.get("APPDATA", "")
    public  = os.environ.get("PUBLIC", "")

    _add(os.path.join(profile, ".certificates"),      "%USERPROFILE%\\.certificates")
    _add(os.path.join(profile, "certificates"),       "%USERPROFILE%\\certificates")
    _add(os.path.join(profile, "Desktop"),            "Desktop")
    _add(os.path.join(appdata, "certificates"),       "%APPDATA%\\certificates")
    _add(os.path.join(public,  "Desktop"),            "Public Desktop")

    return dirs


# ---------------------------------------------------------------------------
# Certificate auto-discovery
# FIX: extra_dir passed as parameter instead of reading GUI widget directly.
#      This decouples business logic from the presentation layer.
# ---------------------------------------------------------------------------

def znajdz_certyfikaty(extra_dir: str = "") -> list:
    """
    Scan for .pfx certificates in (in order):
      1. sys._MEIPASS            – bundled inside EXE
      2. Program directory       – same folder as EXE / script
      3. Program directory\\certs – conventional sub-folder
      4. Standard Windows cert locations (see _standard_cert_dirs)
      5. extra_dir               – optional custom path supplied by caller
    Returns list of dicts: {name, path, source}
    """
    search_dirs: list[tuple[str, str]] = []

    resource_dir = get_resource_dir()
    search_dirs.append((resource_dir, "bundled"))

    prog_dir = get_program_dir()
    if os.path.normpath(prog_dir) != os.path.normpath(resource_dir):
        search_dirs.append((prog_dir, "program dir"))

    certs_subdir = os.path.join(prog_dir, "certs")
    if os.path.isdir(certs_subdir):
        search_dirs.append((certs_subdir, "certs/"))

    # Standard Windows locations
    already = {os.path.normpath(d) for d, _ in search_dirs}
    for d, label in _standard_cert_dirs():
        if os.path.normpath(d) not in already:
            search_dirs.append((d, label))
            already.add(os.path.normpath(d))

    # Caller-supplied extra path  (FIX: no longer touches cert_dir_var directly)
    if extra_dir and os.path.isdir(extra_dir) and os.path.normpath(extra_dir) not in already:
        search_dirs.append((extra_dir, extra_dir))

    found: dict[str, dict] = {}
    for directory, source in search_dirs:
        try:
            for fname in os.listdir(directory):
                if fname.lower().endswith(".pfx"):
                    full = os.path.join(directory, fname)
                    real = os.path.realpath(full)
                    if os.path.isfile(full) and real not in found:
                        found[real] = {"name": fname, "path": full, "source": source}
        except OSError:
            pass

    log.debug("Certificates found: %d", len(found))
    return list(found.values())


def odswiez_certyfikaty(*_):
    # FIX: pass extra_dir as argument instead of letting the function grab it
    extra = cert_dir_var.get().strip()
    certs = znajdz_certyfikaty(extra_dir=extra)
    cert_list.clear()
    cert_list.extend(certs)

    names = [f"{c['name']}  [{c['source']}]" for c in certs]
    combo_cert["values"] = names

    if names:
        combo_cert.current(0)
        label_cert_status.config(
            text=f"OK  {len(names)} certificate(s) found",
            fg=COLOR_SUCCESS   # FIX: use named colour constant
        )
    else:
        combo_cert.set("")
        label_cert_status.config(
            text="WARN  No .pfx certificates found",
            fg=COLOR_ERROR     # FIX: was bare "red", now consistent hex
        )


def wybierz_katalog_certow():
    katalog = filedialog.askdirectory(title="Select certificate directory")
    if katalog:
        cert_dir_var.set(katalog)
        odswiez_certyfikaty()


def pobierz_wybrany_cert():
    idx = combo_cert.current()
    if idx < 0:
        if cert_list:
            return cert_list[0]
        return None
    if idx >= len(cert_list):
        return None
    return cert_list[idx]


# ---------------------------------------------------------------------------
# GUI callbacks
# ---------------------------------------------------------------------------

def wybierz_wejscie():
    plik = filedialog.askopenfilename(
        title="Select file to sign",
        filetypes=[("Executable files", "*.exe *.dll *.msi *.cab"), ("All files", "*.*")]
    )
    if plik:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, plik)


# ---------------------------------------------------------------------------
# Signing worker  (FIX: runs in background thread — UI stays responsive)
# ---------------------------------------------------------------------------

def _sign_worker(cmd: list[str], cert: dict, input_path: str, password: str):
    """
    Executed in a daemon thread.  Never touches Tkinter widgets directly —
    all UI updates are dispatched via root.after() to the main thread.
    """
    # FIX: clear the password from the command list as soon as the process
    # is spawned so it lives in memory for the shortest possible time.
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    except Exception as exc:
        log.exception("Unexpected error running signtool")
        root.after(0, _on_sign_error, str(exc))
        return
    finally:
        # FIX: zero-out the password slot in cmd so it's not kept in memory
        if password and "/p" in cmd:
            idx = cmd.index("/p")
            if idx + 1 < len(cmd):
                cmd[idx + 1] = ""

    if result.returncode == 0:
        log.info("Signed OK: %s  cert=%s", input_path, cert["name"])
        root.after(0, _on_sign_success, input_path, cert, result.stdout)
    else:
        err = (result.stderr or "") + (result.stdout or "")
        if "Invalid Timestamp URL" in err:
            log.warning("Retrying with /t http timestamp due to Invalid Timestamp URL")
            fallback_cmd = [cmd[0], "sign", "/fd", "sha256", "/f", cert["path"]]
            if password:
                fallback_cmd += ["/p", password]
            fallback_cmd += ["/t", "http://timestamp.digicert.com", input_path]
            try:
                retry = subprocess.run(fallback_cmd, capture_output=True, text=True, shell=False)
            except Exception as exc2:
                log.exception("Fallback run error")
                root.after(0, _on_sign_error, str(exc2))
                return
            if retry.returncode == 0:
                log.info("Signed OK (fallback /t): %s  cert=%s", input_path, cert["name"])
                root.after(0, _on_sign_success, input_path, cert, retry.stdout)
                return
            err_out = f"{result.stdout.strip()}\n{result.stderr.strip()}\n--- Fallback ---\n{retry.stdout.strip()}\n{retry.stderr.strip()}"
            result.stdout = err_out
            result.stderr = ""
            log.error("Sign FAILED after fallback (code %d): %s\n%s",
                      retry.returncode, input_path, err_out)
            root.after(0, _on_sign_failure, cert, retry)
        else:
            log.error("Sign FAILED (code %d): %s\nSTDOUT: %s\nSTDERR: %s",
                      result.returncode, input_path,
                      result.stdout.strip(), result.stderr.strip())
            root.after(0, _on_sign_failure, cert, result)


def _on_sign_success(input_path: str, cert: dict, stdout: str):
    btn_run.config(state="normal", text="Sign File")
    label_result.config(text="OK  Signed successfully!", fg=COLOR_SUCCESS)
    messagebox.showinfo(
        "Success",
        f"File signed successfully!\n\n{os.path.basename(input_path)}\n\n"
        f"Certificate: {cert['name']}\n\n"
        f"Output:\n{stdout.strip()}"
    )


def _on_sign_failure(cert: dict, result):
    btn_run.config(state="normal", text="Sign File")
    label_result.config(text="FAIL  Signing failed!", fg=COLOR_ERROR)
    messagebox.showerror(
        "Signing Failed",
        f"SignTool returned code {result.returncode}.\n\n"
        f"Certificate: {cert['name']}\n\n"
        f"STDOUT:\n{result.stdout.strip()}\n\n"
        f"STDERR:\n{result.stderr.strip()}"
    )


def _on_sign_error(message: str):
    btn_run.config(state="normal", text="Sign File")
    label_result.config(text="ERROR  Unexpected error!", fg=COLOR_ERROR)
    messagebox.showerror("Error", f"Unexpected error:\n{message}")


def uruchom_signtool():
    input_path = entry_input.get().strip()

    if not input_path:
        messagebox.showerror("Error", "Please select a file to sign.")
        return

    if not os.path.isfile(input_path):
        messagebox.showerror("Error", f"File not found:\n{input_path}")
        return

    signtool_path = znajdz_signtool()
    if not signtool_path:
        messagebox.showerror(
            "Error",
            "signtool.exe not found.\n\n"
            "Expected locations:\n"
            "  * Bundled inside this EXE\n"
            f"  * Program directory: {get_program_dir()}\n"
            "  * Windows SDK:  C:\\Program Files (x86)\\Windows Kits\\10\\bin\\<ver>\\x64\\\n"
            "  * System PATH"
        )
        return

    cert = pobierz_wybrany_cert()
    if not cert:
        odswiez_certyfikaty()
        cert = pobierz_wybrany_cert()
    if not cert:
        messagebox.showerror(
            "Error",
            "No certificate selected.\n\n"
            "Put .pfx files next to this EXE (or in a 'certs' subfolder)\n"
            "and press the Refresh button, or browse to a custom folder."
        )
        return

    pfx_path     = cert["path"]
    pfx_password = entry_password.get()

    cmd = [
        signtool_path, "sign",
        "/fd", "sha256",
        "/f",  pfx_path,
    ]
    if pfx_password:
        cmd += ["/p", pfx_password]
    cmd += [
        # FIX: HTTPS instead of HTTP for the timestamp server
        "/tr", "https://timestamp.digicert.com",
        "/td", "sha256",
        input_path
    ]

    log.info("Starting sign: %s  cert=%s  tool=%s", input_path, cert["name"], signtool_path)
    btn_run.config(state="disabled", text="Signing...")
    label_result.config(text="", fg="black")
    root.update_idletasks()

    # FIX: run subprocess in background thread so the UI stays responsive
    t = threading.Thread(
        target=_sign_worker,
        args=(cmd, cert, input_path, pfx_password),
        daemon=True
    )
    t.start()


# ---------------------------------------------------------------------------
# GUI layout
# ---------------------------------------------------------------------------

root = tk.Tk()
root.title(APP_NAME)
root.resizable(False, False)
root.configure(bg=COLOR_BG)

# FIX: load icon once, reuse the same variable for both iconbitmap and header logo
app_logo_img = None
try:
    icon_path = resource_path("app_icon.ico")
    if os.path.isfile(icon_path):
        root.iconbitmap(icon_path)
        _img = Image.open(icon_path)
        _img = _img.resize((24, 24), Image.LANCZOS)
        app_logo_img = ImageTk.PhotoImage(_img)
except Exception:
    app_logo_img = None

FONT_NORMAL = ("Segoe UI", 9)
FONT_SMALL  = ("Segoe UI", 8)
FONT_BOLD   = ("Segoe UI", 10, "bold")
MINIMAL_GUI = True

# Header
frame_header = tk.Frame(root, bg=COLOR_PRIMARY, pady=8)
frame_header.pack(fill="x")
label_header = tk.Label(
    frame_header, text=f"  {APP_NAME}  v{APP_VERSION}",
    bg=COLOR_PRIMARY, fg="white",
    font=("Segoe UI", 12, "bold"), anchor="w"
)
if app_logo_img:
    label_header.config(image=app_logo_img, compound="left")
label_header.pack(fill="x", padx=12)

# SignTool status
signtool_found = znajdz_signtool()
status_label = tk.Label(
    root,
    text=("OK  signtool.exe found" if signtool_found else "WARN  signtool.exe NOT found!"),
    fg=(COLOR_SUCCESS if signtool_found else COLOR_ERROR),  # FIX: consistent colour constants
    anchor="w", font=FONT_SMALL, bg=COLOR_BG
)
if not MINIMAL_GUI:
    status_label.pack(padx=12, pady=(8, 0), fill="x")

tk.Frame(root, height=1, bg=COLOR_BORDER).pack(fill="x", padx=12, pady=4)

# Section: Certificates
cert_section_label = tk.Label(root, text="Certificates", font=FONT_BOLD, anchor="w",
         bg=COLOR_BG)
if not MINIMAL_GUI:
    cert_section_label.pack(padx=12, pady=(4, 0), fill="x")

# Cert directory
frame_certdir = tk.Frame(root, bg=COLOR_BG)
if not MINIMAL_GUI:
    frame_certdir.pack(padx=12, pady=2, fill="x")
tk.Label(frame_certdir, text="Cert folder:", width=12, anchor="w",
         font=FONT_NORMAL, bg=COLOR_BG).pack(side="left")
cert_dir_var = tk.StringVar(value=get_program_dir())
entry_certdir = tk.Entry(frame_certdir, textvariable=cert_dir_var, width=44, font=FONT_NORMAL)
entry_certdir.pack(side="left", padx=4)
tk.Button(
    frame_certdir, text="Browse...", command=wybierz_katalog_certow,
    font=FONT_NORMAL, relief="flat", bg=COLOR_BTN, cursor="hand2", padx=6
).pack(side="left", padx=2)
tk.Button(
    frame_certdir, text="Refresh", command=odswiez_certyfikaty,
    font=FONT_NORMAL, relief="flat", bg=COLOR_BTN, cursor="hand2", padx=6
).pack(side="left")

# Cert selector
frame_cert = tk.Frame(root, bg=COLOR_BG)
if not MINIMAL_GUI:
    frame_cert.pack(padx=12, pady=2, fill="x")
tk.Label(frame_cert, text="Certificate:", width=12, anchor="w",
         font=FONT_NORMAL, bg=COLOR_BG).pack(side="left")
cert_list = []
combo_cert = ttk.Combobox(frame_cert, width=53, state="readonly", font=FONT_NORMAL)
combo_cert.pack(side="left", padx=4)

label_cert_status = tk.Label(root, text="", font=FONT_SMALL, anchor="w", bg=COLOR_BG)
if not MINIMAL_GUI:
    label_cert_status.pack(padx=12, fill="x")

# PFX Password
frame_pass = tk.Frame(root, bg=COLOR_BG)
if not MINIMAL_GUI:
    frame_pass.pack(padx=12, pady=2, fill="x")
tk.Label(frame_pass, text="PFX password:", width=12, anchor="w",
         font=FONT_NORMAL, bg=COLOR_BG).pack(side="left")
entry_password = tk.Entry(frame_pass, width=28, show="*", font=FONT_NORMAL)
entry_password.pack(side="left", padx=4)
tk.Label(frame_pass, text="(leave blank if none)", font=FONT_SMALL,
         fg=COLOR_GREY_TXT, bg=COLOR_BG).pack(side="left")

tk.Frame(root, height=1, bg=COLOR_BORDER).pack(fill="x", padx=12, pady=6)

# Section: File to sign
tk.Label(root, text="File to sign", font=FONT_BOLD, anchor="w",
         bg=COLOR_BG).pack(padx=12, fill="x")
frame_input = tk.Frame(root, bg=COLOR_BG)
frame_input.pack(padx=12, pady=4, fill="x")
tk.Label(frame_input, text="File:", width=12, anchor="w",
         font=FONT_NORMAL, bg=COLOR_BG).pack(side="left")
entry_input = tk.Entry(frame_input, width=44, font=FONT_NORMAL)
entry_input.pack(side="left", padx=4)
tk.Button(
    frame_input, text="Browse...", command=wybierz_wejscie,
    font=FONT_NORMAL, relief="flat", bg=COLOR_BTN, cursor="hand2", padx=6
).pack(side="left")

# Sign button + result label
frame_bottom = tk.Frame(root, bg=COLOR_BG)
frame_bottom.pack(padx=12, pady=10, fill="x")
btn_run = tk.Button(
    frame_bottom, text="Sign File", command=uruchom_signtool,
    bg=COLOR_PRIMARY, fg="white", padx=16, pady=6,
    font=FONT_BOLD, relief="flat", cursor="hand2"
)
btn_run.pack(side="left")
label_result = tk.Label(frame_bottom, text="", font=FONT_NORMAL, bg=COLOR_BG)
label_result.pack(side="left", padx=12)

# Footer
tk.Frame(root, height=1, bg=COLOR_BORDER).pack(fill="x", padx=12)
tk.Label(root, text=f"{APP_NAME} v{APP_VERSION} — by Sebastian Januchowski",
         fg=COLOR_GREY_TXT, font=FONT_SMALL, bg=COLOR_BG).pack(side="bottom", pady=4)

# Initial scan
odswiez_certyfikaty()

root.mainloop()
