import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import logging
import logging.handlers
import re
import os
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
from signtool_logic import (
    SignToolWrapper, load_config, save_config, resource_path, get_program_dir,
    is_dpapi_available, encrypt_password, decrypt_password, get_config_path, get_resource_dir
)

APP_NAME    = "Quick DigitalSignature GUI"
APP_VERSION = "1.9"
APP_AUTHOR  = "Sebastian Januchowski"
last_op = None

# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------
def setup_logging():
    """Configures logging to a file."""
    try:
        log_dir = os.path.dirname(get_config_path())
        log_file = os.path.join(log_dir, "app.log")

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Use a rotating file handler to keep log files from growing too large
        handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=1024*1024, backupCount=5, encoding='utf-8'
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    except Exception as e:
        # If logging setup fails, we can't log, so print to stderr
        print(f"FATAL: Could not set up logging. Error: {e}")

# ---------------------------------------------------------------------------
# Theme Management
# ---------------------------------------------------------------------------
THEMES = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "black",
        "entry_bg": "white",
        "entry_fg": "black",
        "button_bg": "#e1e1e1",
        "button_fg": "black",
        "accent_bg": "#0078D4",
        "accent_fg": "white",
        "header_bg": "#0078D4",
        "header_fg": "white",
        "success_fg": "#006400",
        "error_fg": "red",
        "info_fg": "grey",
        "tooltip_bg": "#ffffe0",
        "tooltip_fg": "black",
        "separator_bg": "#cccccc",
        "select_color": "#f0f0f0", # For checkbox
    },
    "dark": {
        "bg": "#2b2b2b",
        "fg": "#dcdcdc",
        "entry_bg": "#3c3c3c",
        "entry_fg": "#dcdcdc",
        "button_bg": "#4f4f4f",
        "button_fg": "#dcdcdc",
        "accent_bg": "#0078D4",
        "accent_fg": "white",
        "header_bg": "#005a9e",
        "header_fg": "white",
        "success_fg": "#6a9955",
        "error_fg": "#f44747",
        "info_fg": "#8c8c8c",
        "tooltip_bg": "#4f4f4f",
        "tooltip_fg": "#dcdcdc",
        "separator_bg": "#555555",
        "select_color": "#2b2b2b", # For checkbox
    }
}
current_theme_name = "light"

# A dictionary to hold all widgets that need to be themed
themed_widgets = {
    "bg_fg": [],
    "bg_only": [],
    "button": [],
    "accent_button": [],
    "entry": [],
    "header": [],
    "separator": [],
    "checkbox": [],
}

def toggle_theme():
    """Switches between light and dark themes."""
    global current_theme_name
    new_theme = "dark" if current_theme_name == "light" else "light"
    apply_theme(new_theme)


# ---------------------------------------------------------------------------
# Tooltip Helper Class
# ---------------------------------------------------------------------------
class Tooltip:
    """Create a tooltip for a given widget."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        wx = self.widget.winfo_rootx()
        wy = self.widget.winfo_rooty()
        w  = self.widget.winfo_width()
        h  = self.widget.winfo_height()
        x  = wx + (w // 2)
        y  = wy + h + 12
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        theme = THEMES[current_theme_name]
        label = tk.Label(self.tooltip_window, text=self.text, justify='left',
                         background=theme["tooltip_bg"], foreground=theme["tooltip_fg"],
                         relief='solid', borderwidth=1,
                         font=("Segoe UI", 8, "normal"))
        label.pack(ipadx=2, ipady=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

# ---------------------------------------------------------------------------
# Resource helpers
# Application Logic
# ---------------------------------------------------------------------------

def apply_theme(theme_name: str):
    """Applies the selected color theme to all registered widgets."""
    global current_theme_name
    current_theme_name = theme_name
    theme = THEMES[theme_name]

    # Update theme toggle button icon
    if 'btn_theme' in globals():
        btn_theme.config(text="☀️" if theme_name == "dark" else "🌙")

    # Root window
    root.config(bg=theme["bg"])

    # Style for ttk widgets (Combobox)
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox",
                    fieldbackground=theme["entry_bg"],
                    background=theme["button_bg"],
                    foreground=theme["entry_fg"],
                    arrowcolor=theme["fg"],
                    selectbackground=theme["entry_bg"],
                    selectforeground=theme["entry_fg"],
                    bordercolor=theme["separator_bg"])
    root.option_add('*TCombobox*Listbox.background', theme["entry_bg"])
    root.option_add('*TCombobox*Listbox.foreground', theme["entry_fg"])
    root.option_add('*TCombobox*Listbox.selectBackground', theme["accent_bg"])
    root.option_add('*TCombobox*Listbox.selectForeground', theme["accent_fg"])

    # Apply theme to categorized widgets
    for widget in themed_widgets["bg_fg"]:
        widget.config(bg=theme["bg"], fg=theme["fg"])

    for widget in themed_widgets["bg_only"]:
        widget.config(bg=theme["bg"])

    for widget in themed_widgets["button"]:
        widget.config(bg=theme["button_bg"], fg=theme["button_fg"])

    for widget in themed_widgets["accent_button"]:
        widget.config(bg=theme["accent_bg"], fg=theme["accent_fg"])

    for widget in themed_widgets["entry"]:
        widget.config(bg=theme["entry_bg"], fg=theme["entry_fg"],
                      insertbackground=theme["fg"], highlightbackground=theme["separator_bg"],
                      highlightcolor=theme["accent_bg"], highlightthickness=1)

    for widget in themed_widgets["header"]:
        try:
            widget.config(bg=theme["header_bg"])
        except Exception:
            pass
        try:
            if "fg" in widget.keys():
                widget.config(fg=theme["header_fg"])
            elif "foreground" in widget.keys():
                widget.config(foreground=theme["header_fg"])
        except Exception:
            pass

    for widget in themed_widgets["separator"]:
        widget.config(bg=theme["separator_bg"])

    for widget in themed_widgets["checkbox"]:
        widget.config(bg=theme["bg"], fg=theme["fg"], selectcolor=theme["select_color"])

    if 'label_pass_info' in globals():
        label_pass_info.config(fg=theme["info_fg"])

logic = SignToolWrapper()

def odswiez_certyfikaty(*_):
    try:
        extra_dir = cert_dir_var.get().strip()
    except (NameError, tk.TclError):
        extra_dir = None
    certs = logic.find_certificates(extra_dir)
    cert_list.clear()
    cert_list.extend(certs)
    names = [f"{c['name']}  [{c['source']}]" for c in certs]
    combo_cert["values"] = names
    if names:
        combo_cert.current(0)
    else:
        combo_cert.set("")

def wybierz_katalog_certow():
    katalog = filedialog.askdirectory(title="Select certificate directory")
    if katalog:
        cert_dir_var.set(katalog)
        odswiez_certyfikaty()


def pobierz_wybrany_cert():
    idx = combo_cert.current()
    if idx < 0:
        return None
    if idx >= len(cert_list):
        return None
    return cert_list[idx]

def wybierz_cert_pfx():
    sciezka = filedialog.askopenfilename(
        title="Select certificate (.pfx)",
        filetypes=[("PFX certificates", "*.pfx"), ("All files", "*.*")]
    )
    if not sciezka:
        return
    try:
        cert_list.clear()
        cert_list.append({"name": os.path.basename(sciezka), "path": sciezka, "source": "selected"})
        combo_cert["values"] = [f"{os.path.basename(sciezka)}  [selected]"]
        combo_cert.current(0)
        label_result.config(text=f"OK  Selected certificate: {os.path.basename(sciezka)}", fg="#006400")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")
        logging.exception("Error while selecting PFX certificate.")

# ---------------------------------------------------------------------------
# GUI Callbacks
# ---------------------------------------------------------------------------

def handle_drop(event):
    """Handles file drop events."""
    # The event.data can be a list of file paths, sometimes with braces.
    # We'll find the first valid file from the list.
    # A simple regex to find paths, handling both braced and non-braced items.
    potential_paths = re.findall(r'\{[^{}]*\}|\S+', event.data)
    
    found_file = None
    for path in potential_paths:
        # Clean up path, removing braces if they exist
        clean_path = path.strip()
        if clean_path.startswith('{') and clean_path.endswith('}'):
            clean_path = clean_path[1:-1]
        
        if os.path.isfile(clean_path):
            found_file = clean_path
            break # Found a valid file, stop searching

    if found_file:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, found_file)
        label_result.config(text=f"OK  Loaded file: {os.path.basename(found_file)}", fg="#006400")
    else:
        messagebox.showwarning("Drag & Drop", f"Dropped item is not a valid file:\n{event.data}")
        logging.warning(f"Invalid item dropped: {event.data}")

def wybierz_wejscie():
    plik = filedialog.askopenfilename(
        title="Select file to sign",
        filetypes=[("Executable files", "*.exe *.dll *.msi *.cab"), ("All files", "*.*")]
    )
    if plik:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, plik)


def uruchom_signtool():
    global last_op
    logging.info("'Sign File' button clicked.")
    input_path = entry_input.get().strip()

    if not input_path:
        logging.warning("Sign action aborted: No file selected.")
        messagebox.showerror("Error", "Please select a file to sign.")
        return

    if not os.path.isfile(input_path):
        logging.error(f"Sign action aborted: File not found at '{input_path}'.")
        messagebox.showerror("Error", f"File not found:\n{input_path}")
        return

    if not logic.is_signtool_found():
        logging.critical("Sign action aborted: SignTool.exe not found.")
        messagebox.showerror(
            "Error",
            "SignTool.exe not found.\n\n"
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
        logging.error("Sign action aborted: No certificate selected.")
        messagebox.showerror(
            "Error",
            "No certificate selected.\n\n"
            "Put .pfx files next to this EXE (or in a 'certs' subfolder)\n"
            "and press the Refresh button, or browse to a custom folder."
        )
        return

    pfx_path = cert["path"]
    password = entry_password.get()
    last_op = "sign"

    btn_run.config(state="disabled", text="Signing...")
    label_result.config(text="", fg="black")
    root.update_idletasks()

    logging.info(f"Attempting to sign file: {input_path}")
    logging.info(f"Using certificate: {pfx_path}")
    try:
        returncode, stdout, stderr = logic.sign_file(input_path, pfx_path, password)

        if returncode == 0:
            label_result.config(text="OK  Signed successfully!", fg="#006400")
            logging.info(f"Successfully signed '{os.path.basename(input_path)}'. Output: {stdout.strip()}")
            messagebox.showinfo(
                "Success",
                f"File signed successfully!\n\n{os.path.basename(input_path)}\n\n"
                f"Certificate: {cert['name']}\n\n"
                f"Output:\n{stdout.strip()}"
            )
        else:
            label_result.config(text="FAIL  Signing failed!", fg="red")
            logging.error(f"Signing failed with code {returncode}. STDOUT: {stdout.strip()} STDERR: {stderr.strip()}")
            messagebox.showerror(
                "Signing Failed",
                f"SignTool returned code {returncode}.\n\n"
                f"Certificate: {cert['name']}\n\n"
                f"STDOUT:\n{stdout.strip()}\n\n"
                f"STDERR:\n{stderr.strip()}"
            )
    except Exception as e:
        label_result.config(text="ERROR  Unexpected error!", fg="red")
        logging.exception("An unexpected error occurred during the signing process.")
        messagebox.showerror("Error", f"Unexpected error:\n{e}")
    finally:
        btn_run.config(state="normal", text="Sign File")

def _uruchom_weryfikacje(verify_timestamp: bool):
    global last_op
    input_path = entry_input.get().strip()
    if not input_path or not os.path.isfile(input_path):
        logging.warning("Verify action aborted: No valid file selected.")
        messagebox.showerror("Error", "Please select a valid file to verify.")
        return
    if not logic.is_signtool_found():
        logging.critical("Verify action aborted: SignTool.exe not found.")
        messagebox.showerror("Error", "SignTool.exe not found.")
        return

    last_op = "verify_ts" if verify_timestamp else "verify_pa"
    logging.info(f"Verification called for: {input_path}, with timestamp: {verify_timestamp}")
    try:
        returncode, stdout, stderr = logic.verify_signature(input_path, verify_timestamp)
        if returncode == 0:
            label_text = "OK  Signature+Timestamp valid" if verify_timestamp else "OK  Signature valid (PA)"
            label_result.config(text=label_text, fg="#006400")
            logging.info(f"Verification successful for '{input_path}'. Output: {stdout.strip()}")
            messagebox.showinfo("Verification OK", stdout.strip() or "Signature valid.")
        else:
            label_text = "FAIL  Timestamp invalid" if verify_timestamp else "FAIL  Signature invalid (PA)"
            label_result.config(text=label_text, fg="red")
            logging.error(f"Verification failed for '{input_path}' with code {returncode}. STDOUT: {stdout.strip()} STDERR: {stderr.strip()}")
            err_txt = (stderr or "").lower() + "\n" + (stdout or "").lower()
            if "root certificate which is not trusted" in err_txt or "not trusted by the trust provider" in err_txt:
                logging.warning("Verification failed due to untrusted root certificate.")
                messagebox.showerror(
                    "Verification Failed",
                    f"Return code {returncode}\n\n"
                    f"{stdout.strip()}\n\n"
                    "Cause: The signing chain ends at a root certificate that is not trusted on this machine.\n\n"
                    "Fix:\n"
                    "1) Import the issuer root certificate to 'Trusted Root Certification Authorities'.\n"
                    "2) Import any intermediate certificates to 'Intermediate Certification Authorities'.\n"
                    "Use certmgr.msc (Local Computer) or PowerShell:\n"
                    "  Import-Certificate -FilePath <root.cer> -CertStoreLocation Cert:\\LocalMachine\\Root\n"
                    "  Import-Certificate -FilePath <intermediate.cer> -CertStoreLocation Cert:\\LocalMachine\\CA"
                )
            else:
                messagebox.showerror(
                    "Verification Failed",
                    f"Return code {returncode}\n\nSTDOUT:\n{stdout.strip()}\n\nSTDERR:\n{stderr.strip()}"
                )
    except Exception as e:
        label_result.config(text="ERROR  Unexpected error!", fg="red")
        logging.exception("An unexpected error occurred during the verification process.")
        messagebox.showerror("Error", f"Unexpected error:\n{e}")

def weryfikuj_podpis_pa():
    _uruchom_weryfikacje(verify_timestamp=False)

def weryfikuj_podpis_ts():
    _uruchom_weryfikacje(verify_timestamp=True)

def ponow():
    if last_op == "sign":
        uruchom_signtool()
    elif last_op == "verify_pa":
        weryfikuj_podpis_pa()
    elif last_op == "verify_ts":
        weryfikuj_podpis_ts()
    else:
        logging.info("Retry button clicked, but no previous operation found.")
        messagebox.showinfo("Retry", "No previous operation to retry.")

def _zainstaluj_cert(store_name: str, title: str):
    sciezka = filedialog.askopenfilename(
        title=title,
        filetypes=[("Certificates", "*.cer;*.crt;*.pem"), ("All files", "*.*")]
    )
    if not sciezka:
        return
    code, out, err, user_store = logic.install_certificate(store_name, sciezka)
    logging.info(f"Attempting to install certificate '{sciezka}' into store '{store_name}'.")
    if code == 0:
        label = f"OK  Installed {store_name} CA" + (" (User store)" if user_store else "")
        label_result.config(text=label, fg="#006400")
        info = out.strip() or "OK"
        if user_store:
            info += "\n\nInstalled in Current User store. For system-wide trust, run as Administrator."
        logging.info(f"Certificate installation successful. Store: {store_name}, User: {user_store}. Output: {info}")
        messagebox.showinfo(f"{store_name} CA Installed", info)
    else:
        label_result.config(text=f"FAIL  {store_name} CA installation failed", fg="red")
        msg = f"Return code {code}\n\nSTDOUT:\n{out.strip()}\n\nSTDERR:\n{err.strip()}"
        logging.error(f"Certificate installation failed with code {code}. STDOUT: {out.strip()} STDERR: {err.strip()}")
        messagebox.showerror(f"{store_name} CA Installation Error", msg)

def zainstaluj_root_ca():
    _zainstaluj_cert("Root", "Wybierz certyfikat Root CA (.cer/.crt/.pem)")

def zainstaluj_intermediate_ca():
    _zainstaluj_cert("CA", "Wybierz certyfikat Intermediate CA (.cer/.crt/.pem)")

def toggle_topmost():
    try:
        current = bool(root.attributes("-topmost"))
        root.attributes("-topmost", not current)
        theme = THEMES[current_theme_name]
        btn_topmost.config(
            text=("🔝" if not current else "⬇"),
            bg=theme["button_bg"]
        )
        label_result.config(text=("Topmost ON" if not current else "Topmost OFF"))
    except Exception as e:
        logging.exception("Error toggling 'Always on Top' mode.")
        messagebox.showerror("Error", f"Unexpected error:\n{e}")

def show_about():
    info = (
        f"{APP_NAME} v{APP_VERSION}\n\n"
        "GUI for signing Windows binaries with Microsoft SignTool.\n"
        "Supports SHA-256 and RFC3161 timestamp verification.\n\n"
        f"Project Manager: {APP_AUTHOR}\n"
        "Company: polsoft.ITS™ Group\n"
        "Contact: polsoft.its@fastservice.com\n"
        "Website: https://github.com/seb07uk\n"
        "Copyright: 2026© polsoft.ITS™. All rights reserved."
    )
    messagebox.showinfo("About", info)

def on_closing():
    """Save configuration on window close."""
    logging.info("Application closing. Saving configuration.")
    config_data = {}
    # Save last file path
    last_file = entry_input.get().strip()
    if last_file and os.path.isfile(last_file):
        config_data["last_file_path"] = last_file

    # Save last certificate path
    selected_cert = pobierz_wybrany_cert()
    if selected_cert and os.path.isfile(selected_cert.get("path", "")):
        config_data["last_cert_path"] = selected_cert["path"]

    # Save encrypted password if requested
    if save_password_var.get() == 1 and is_dpapi_available():
        password = entry_password.get()
        if password:
            encrypted = encrypt_password(password)
            if encrypted:
                config_data["encrypted_password"] = encrypted

    # Save theme
    config_data["theme"] = current_theme_name

    if config_data:
        save_config(config_data)

    logging.info("Application finished.")
    root.destroy()
# ---------------------------------------------------------------------------
# GUI layout
# --------------------------------------------------------------------------- 

# Initialize logging first
setup_logging()

logging.info("==================================================")
logging.info(f"Application '{APP_NAME}' v{APP_VERSION} starting up.")
logging.info(f"Program directory: {get_program_dir()}")
logging.info(f"Resource directory: {get_resource_dir()}")


root = TkinterDnD.Tk()  # Use TkinterDnD for drag & drop
root.title(APP_NAME)
root.resizable(False, False)
themed_widgets["bg_only"].append(root)

try:
    icon_path = resource_path("app_icon.ico")
    if os.path.isfile(icon_path):
        root.iconbitmap(icon_path)
except Exception:
    pass
try:
    app_logo_img = None
    if os.path.isfile(icon_path):
        _img = Image.open(icon_path)
        _img = _img.resize((32, 32), Image.LANCZOS)
        app_logo_img = ImageTk.PhotoImage(_img)
except Exception:
    app_logo_img = None

FONT_NORMAL = ("Segoe UI", 9)
FONT_SMALL  = ("Segoe UI", 8)
FONT_BOLD   = ("Segoe UI", 10, "bold")
MINIMAL_GUI = True

# Header
frame_header = tk.Frame(root, pady=8)
themed_widgets["header"].append(frame_header)
frame_header.pack(fill="x")
label_header = tk.Label(
    frame_header, text=f"  {APP_NAME}  v{APP_VERSION}",
    font=("Segoe UI", 12, "bold"), anchor="w"
)
themed_widgets["header"].append(label_header)
if app_logo_img:
    label_header.config(image=app_logo_img, compound="left")
label_header.pack(fill="x", padx=12)

# SignTool status
signtool_found = logic.is_signtool_found()
status_label = tk.Label(root, anchor="w", font=FONT_SMALL)
themed_widgets["bg_fg"].append(status_label)
if not MINIMAL_GUI:
    status_label.pack(padx=12, pady=(8, 0), fill="x")

separator1 = tk.Frame(root, height=1)
themed_widgets["separator"].append(separator1)
separator1.pack(fill="x", padx=12, pady=4)

# Cert selector (will be packed later under File section)
frame_cert = tk.Frame(root)
themed_widgets["bg_only"].append(frame_cert)
label_cert_title = tk.Label(frame_cert, text="Certificate:", width=12, anchor="w", font=FONT_NORMAL)
themed_widgets["bg_fg"].append(label_cert_title)
label_cert_title.pack(side="left")
cert_list = []
cert_dir_var = tk.StringVar()
combo_cert = ttk.Combobox(frame_cert, width=32, state="readonly", font=FONT_NORMAL)
combo_cert.pack(side="left", padx=4)
btn_refresh_certs = tk.Button(
    frame_cert, text="🔄", command=odswiez_certyfikaty,
    font=FONT_NORMAL, relief="flat", cursor="hand2", padx=4
)
themed_widgets["button"].append(btn_refresh_certs)
btn_refresh_certs.pack(side="left")
Tooltip(btn_refresh_certs, "Rescan default locations for .pfx certificates.")
btn_browse_cert = tk.Button(
    frame_cert, text="Browse...", command=wybierz_cert_pfx,
    font=FONT_NORMAL, relief="flat", cursor="hand2", padx=6
)
themed_widgets["button"].append(btn_browse_cert)
btn_browse_cert.pack(side="left")
Tooltip(btn_browse_cert, "Browse for a specific .pfx certificate file.")

# PFX Password (will be packed later under File section)
frame_pass = tk.Frame(root)
themed_widgets["bg_only"].append(frame_pass)
label_pass_title = tk.Label(frame_pass, text="PFX password:", width=12, anchor="w", font=FONT_NORMAL)
themed_widgets["bg_fg"].append(label_pass_title)
label_pass_title.pack(side="left")
entry_password = tk.Entry(frame_pass, width=24, show="*", font=FONT_NORMAL)
themed_widgets["entry"].append(entry_password)
entry_password.pack(side="left", padx=4)

save_password_var = tk.IntVar()
check_save_pass = tk.Checkbutton(
    frame_pass, text="Save", variable=save_password_var,
    font=FONT_SMALL, cursor="hand2"
)
themed_widgets["checkbox"].append(check_save_pass)
if is_dpapi_available():
    check_save_pass.pack(side="left", padx=(0, 4))
else:
    check_save_pass.config(state="disabled")
    check_save_pass.pack(side="left", padx=(0, 4))
Tooltip(check_save_pass, "Save the password securely using Windows Data Protection.\n"
                         "It will only be accessible on this computer by your user account.")

label_pass_info = tk.Label(frame_pass, text="(leave blank if none)", font=FONT_SMALL)
themed_widgets["bg_fg"].append(label_pass_info)
label_pass_info.pack(side="left")

separator2 = tk.Frame(root, height=1)
themed_widgets["separator"].append(separator2)
separator2.pack(fill="x", padx=12, pady=6)

# Section: File to sign
label_file_section = tk.Label(root, text="File to sign", font=FONT_BOLD, anchor="w")
themed_widgets["bg_fg"].append(label_file_section)
label_file_section.pack(padx=12, fill="x")
frame_input = tk.Frame(root)
themed_widgets["bg_only"].append(frame_input)
frame_input.pack(padx=12, pady=4, fill="x")
# Register the whole frame as a drop target for better UX
frame_input.drop_target_register(DND_FILES)
frame_input.dnd_bind('<<Drop>>', handle_drop)
label_file_title = tk.Label(frame_input, text="File:", width=12, anchor="w", font=FONT_NORMAL)
themed_widgets["bg_fg"].append(label_file_title)
label_file_title.pack(side="left")
entry_input = tk.Entry(frame_input, width=39, font=FONT_NORMAL)
themed_widgets["entry"].append(entry_input)
entry_input.pack(side="left", padx=4)
btn_browse_file = tk.Button(
    frame_input, text="Browse...", command=wybierz_wejscie,
    font=FONT_NORMAL, relief="flat", cursor="hand2", padx=6
)
themed_widgets["button"].append(btn_browse_file)
btn_browse_file.pack(side="left")
Tooltip(btn_browse_file, "Browse for a file to sign or verify.")

# Place certificate selector and password below File section
frame_cert.pack(padx=12, pady=2, fill="x")
frame_pass.pack(padx=12, pady=2, fill="x")

# Sign button + result label
frame_bottom = tk.Frame(root)
themed_widgets["bg_only"].append(frame_bottom)
frame_bottom.pack(padx=12, pady=10, fill="x")
frame_actions = tk.Frame(frame_bottom)
themed_widgets["bg_only"].append(frame_actions)
frame_actions.pack(expand=True)
btn_run = tk.Button(
    frame_actions, text="Sign File", command=uruchom_signtool,
    padx=16, pady=6, font=FONT_BOLD, relief="flat", cursor="hand2"
)
themed_widgets["accent_button"].append(btn_run)
btn_run.pack(side="left")
Tooltip(btn_run, "Sign the selected file using the chosen certificate and password.")
btn_verify_pa = tk.Button(
    frame_actions, text="Verify (PA)", command=weryfikuj_podpis_pa,
    padx=10, pady=6, font=FONT_NORMAL, relief="flat", cursor="hand2"
)
themed_widgets["button"].append(btn_verify_pa)
btn_verify_pa.pack(side="left", padx=6)
Tooltip(btn_verify_pa, "Verify the file's signature against the local certificate store (Policy-based).")
btn_verify_ts = tk.Button(
    frame_actions, text="Verify (PA+TS)", command=weryfikuj_podpis_ts,
    padx=10, pady=6, font=FONT_NORMAL, relief="flat", cursor="hand2"
)
themed_widgets["button"].append(btn_verify_ts)
btn_verify_ts.pack(side="left", padx=6)
Tooltip(btn_verify_ts, "Verify the file's signature and the timestamp against an online authority.")
btn_retry = tk.Button(
    frame_actions, text="Retry", command=ponow,
    padx=10, pady=6, font=FONT_NORMAL, relief="flat", cursor="hand2"
)
themed_widgets["button"].append(btn_retry)
btn_retry.pack(side="left", padx=6)
Tooltip(btn_retry, "Repeat the last operation (Sign or Verify).")
frame_install = tk.Frame(root)
themed_widgets["bg_only"].append(frame_install)
frame_install.pack(padx=12, pady=(0, 8), fill="x")
frame_install_buttons = tk.Frame(frame_install)
themed_widgets["bg_only"].append(frame_install_buttons)
frame_install_buttons.pack(expand=True)
btn_install_root = tk.Button(
    frame_install_buttons, text="Install Root CA", command=zainstaluj_root_ca,
    padx=10, pady=6, font=FONT_NORMAL, relief="flat", cursor="hand2"
)
themed_widgets["button"].append(btn_install_root)
btn_install_root.pack(side="left")
Tooltip(btn_install_root, "Install a root certificate (.cer, .crt) into the system's\n'Trusted Root Certification Authorities' store.")
btn_install_intermediate = tk.Button(
    frame_install_buttons, text="Install Intermediate CA", command=zainstaluj_intermediate_ca,
    padx=10, pady=6, font=FONT_NORMAL, relief="flat", cursor="hand2"
)
themed_widgets["button"].append(btn_install_intermediate)
btn_install_intermediate.pack(side="left", padx=6)
Tooltip(btn_install_intermediate, "Install an intermediate certificate (.cer, .crt) into the system's\n'Intermediate Certification Authorities' store.")
frame_status = tk.Frame(root)
themed_widgets["bg_only"].append(frame_status)
frame_status.pack(padx=12, pady=(0, 8), fill="x")
btn_about = tk.Button(frame_status, text="ℹ", command=show_about,
                      padx=6, pady=4, font=FONT_NORMAL, relief="flat", cursor="hand2")
themed_widgets["button"].append(btn_about)
btn_about.pack(side="left", padx=6)
Tooltip(btn_about, "Show application information.")
label_result = tk.Label(frame_status, text="", font=FONT_NORMAL, anchor="center", justify="center")
themed_widgets["bg_fg"].append(label_result)
label_result.pack(side="left", fill="x", expand=True)
btn_theme = tk.Button(frame_status, text="🌙", command=toggle_theme,
                      padx=6, pady=4, font=FONT_NORMAL, relief="flat", cursor="hand2")
themed_widgets["button"].append(btn_theme)
btn_theme.pack(side="right")
Tooltip(btn_theme, "Toggle light/dark theme.")
btn_topmost = tk.Button(frame_status, text="🔝", command=toggle_topmost,
                        padx=6, pady=4, font=FONT_NORMAL, relief="flat", cursor="hand2")
themed_widgets["button"].append(btn_topmost)
btn_topmost.pack(side="right")
Tooltip(btn_topmost, "Toggle 'Always on Top' for this window.")

# Footer
separator3 = tk.Frame(root, height=1)
themed_widgets["separator"].append(separator3)
separator3.pack(fill="x", padx=12)
label_footer = tk.Label(root, text=f"{APP_NAME} v{APP_VERSION} — by {APP_AUTHOR}", font=FONT_SMALL)
themed_widgets["bg_fg"].append(label_footer)
label_footer.pack(side="bottom", pady=4)
label_result.config(
    text=("OK  SignTool.exe found" if signtool_found else "WARN  SignTool.exe NOT found!"),
    fg=("#006400" if signtool_found else "red")
)

# --- Load configuration and bind closing event ---
config = load_config()

logging.info("Loading configuration from file.")
# Restore last used file path
last_file = config.get("last_file_path")
if last_file and os.path.isfile(last_file):
    entry_input.delete(0, tk.END)
    entry_input.insert(0, last_file)
    label_result.config(text=f"OK  Restored last session", fg="#006400")

logging.info("Checking for saved encrypted password.")
# Restore encrypted password
encrypted_pass = config.get("encrypted_password")
if encrypted_pass and is_dpapi_available():
    decrypted_pass = decrypt_password(encrypted_pass)
    if decrypted_pass:
        entry_password.delete(0, tk.END)
        entry_password.insert(0, decrypted_pass)
        save_password_var.set(1) # Check the box to indicate password was loaded

logging.info("Applying saved theme.")
# Apply theme from config
saved_theme = config.get("theme", "light")
apply_theme(saved_theme)

# Initial certificate scan
odswiez_certyfikaty()

logging.info("Checking for last used certificate.")
# Restore last used certificate
last_cert_path = config.get("last_cert_path")
if last_cert_path:
    for i, cert_info in enumerate(cert_list):
        if os.path.normpath(cert_info.get("path", "")) == os.path.normpath(last_cert_path):
            combo_cert.current(i)
            break

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
