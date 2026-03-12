"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         SignTool GUI - polsoft.ITS™                         ║
║                                                                              ║
║  Project Manager : Sebastian Januchowski                                     ║
║  Company         : polsoft.ITS™ Group                                        ║
║  E-mail          : polsoft.its@fastservice.com                               ║
║  GitHub          : https://github.com/seb07uk                                ║
║                                                                              ║
║  2026© Sebastian Januchowski & polsoft.ITS™. All rights reserved.            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Standalone GUI for signtool.exe — digital file signing.
Requirements: Python 3.8+, tkinter (built-in).
              Place signtool.exe next to this script or install Windows SDK
              (auto-detected).
"""

__author__      = "Sebastian Januchowski"
__company__     = "polsoft.ITS™ Group"
__email__       = "polsoft.its@fastservice.com"
__github__      = "https://github.com/seb07uk"
__copyright__   = "2026© Sebastian Januchowski & polsoft.ITS™. All rights reserved."
__version__     = "1.0.0"
__description__ = "GUI wrapper for signtool.exe"

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import sys
import shutil
import json


# ─────────────────────────────────────────────────────────────────────────────
#  i18n — translations
# ─────────────────────────────────────────────────────────────────────────────

TRANSLATIONS = {
    "en": {
        # header
        "app_subtitle":       "polsoft.ITS™ Group  •  Digital Signature Manager",
        "st_found":           "✔  signtool: {name}",
        "st_missing":         "⚠  signtool.exe not found",
        # sections
        "sec_file":           "📄  File to Sign",
        "sec_cert":           "🔐  Certificate",
        "sec_advanced":       "🛠  Advanced Options",
        # labels
        "lbl_file":           "File",
        "lbl_cert":           "Certificate file (.pfx)",
        "lbl_password":       "Certificate password",
        "lbl_show_pass":      "Show password",
        "lbl_timestamp":      "Timestamp URL:",
        "lbl_algorithm":      "Algorithm:",
        # buttons
        "btn_sign":           "  ✅  Sign",
        "btn_signing":        "  ⏳  Signing…",
        "btn_cancel":         "  ✖  Cancel",
        "btn_clear_history":  "🗑  Clear history",
        "btn_lang":           "🌐 PL",
        # browse dialogs
        "browse_file_title":  "Select file to sign",
        "browse_cert_title":  "Select PFX certificate",
        "browse_ft_binary":   "Executable / Library",
        "browse_ft_cert":     "PFX / P12 Certificate",
        "browse_ft_all":      "All files",
        # validation
        "err_no_signtool":    (
            "signtool.exe not found.\n\n"
            "Place signtool.exe in the application directory or install "
            "Windows SDK (10/11)."),
        "err_no_file":        "• No file selected for signing.",
        "err_file_missing":   "• File not found:\n  {path}",
        "err_no_cert":        "• No certificate (.pfx) selected.",
        "err_cert_missing":   "• Certificate not found:\n  {path}",
        "err_title":          "Validation error",
        "warn_no_pass_title": "Empty password",
        "warn_no_pass_msg":   "Certificate password is empty. Continue?",
        # sign result
        "sign_ok":            "File signed successfully! ✅",
        "sign_fail":          "Signing failed (code: {code}).\n\n{detail}",
        "sign_not_found":     "Cannot launch signtool:\n{path}",
        "title_success":      "Success",
        "title_error":        "Error",
        # clear history
        "clear_title":        "Clear history",
        "clear_confirm":      "Delete all saved certificates and passwords?",
        "clear_done_title":   "Done",
        "clear_done_msg":     "History has been cleared.",
        # cancel / quit
        "quit_title":         "Close",
        "quit_confirm":       "Close the application?",
    },
    "pl": {
        # header
        "app_subtitle":       "polsoft.ITS™ Group  •  Menedżer podpisów cyfrowych",
        "st_found":           "✔  signtool: {name}",
        "st_missing":         "⚠  signtool.exe nie znaleziony",
        # sections
        "sec_file":           "📄  Plik do podpisania",
        "sec_cert":           "🔐  Certyfikat",
        "sec_advanced":       "🛠  Opcje zaawansowane",
        # labels
        "lbl_file":           "Plik",
        "lbl_cert":           "Plik certyfikatu (.pfx)",
        "lbl_password":       "Hasło certyfikatu",
        "lbl_show_pass":      "Pokaż hasło",
        "lbl_timestamp":      "Timestamp URL:",
        "lbl_algorithm":      "Algorytm:",
        # buttons
        "btn_sign":           "  ✅  Podpisz",
        "btn_signing":        "  ⏳  Podpisywanie…",
        "btn_cancel":         "  ✖  Anuluj",
        "btn_clear_history":  "🗑  Wyczyść historię",
        "btn_lang":           "🌐 EN",
        # browse dialogs
        "browse_file_title":  "Wybierz plik do podpisania",
        "browse_cert_title":  "Wybierz certyfikat PFX",
        "browse_ft_binary":   "Pliki exe/dll/msi/cab/appx",
        "browse_ft_cert":     "Certyfikat PFX/P12",
        "browse_ft_all":      "Wszystkie pliki",
        # validation
        "err_no_signtool":    (
            "Nie znaleziono signtool.exe.\n\n"
            "Umieść signtool.exe w katalogu aplikacji lub zainstaluj "
            "Windows SDK (10/11)."),
        "err_no_file":        "• Nie wybrano pliku do podpisania.",
        "err_file_missing":   "• Plik nie istnieje:\n  {path}",
        "err_no_cert":        "• Nie wybrano certyfikatu (.pfx).",
        "err_cert_missing":   "• Certyfikat nie istnieje:\n  {path}",
        "err_title":          "Błąd walidacji",
        "warn_no_pass_title": "Brak hasła",
        "warn_no_pass_msg":   "Hasło certyfikatu jest puste. Kontynuować?",
        # sign result
        "sign_ok":            "Plik został podpisany pomyślnie! ✅",
        "sign_fail":          "Podpisywanie nie powiodło się (kod: {code}).\n\n{detail}",
        "sign_not_found":     "Nie można uruchomić signtool:\n{path}",
        "title_success":      "Sukces",
        "title_error":        "Błąd",
        # clear history
        "clear_title":        "Wyczyść historię",
        "clear_confirm":      "Usunąć wszystkie zapamiętane certyfikaty i hasła?",
        "clear_done_title":   "Gotowe",
        "clear_done_msg":     "Historia została wyczyszczona.",
        # cancel / quit
        "quit_title":         "Zamknij",
        "quit_confirm":       "Zamknąć aplikację?",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
#  Paths
# ─────────────────────────────────────────────────────────────────────────────

APP_DIR      = os.path.dirname(os.path.abspath(sys.argv[0]))
HISTORY_FILE = os.path.join(APP_DIR, "signtool_history.json")

SDK_PATHS = [
    os.path.join(APP_DIR, "signtool.exe"),
    r"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe",
    r"C:\Program Files (x86)\Windows Kits\10\bin\x86\signtool.exe",
    r"C:\Program Files\Windows Kits\10\bin\x64\signtool.exe",
    "signtool.exe",
]


def find_signtool() -> str:
    for path in SDK_PATHS:
        if path == "signtool.exe":
            if shutil.which("signtool.exe"):
                return "signtool.exe"
        elif os.path.isfile(path):
            return path
    return ""


# ─────────────────────────────────────────────────────────────────────────────
#  History
# ─────────────────────────────────────────────────────────────────────────────

MAX_HISTORY = 10


def load_history() -> dict:
    try:
        if os.path.isfile(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {"certs": [], "passwords": [], "files": []}


def save_history(history: dict):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def push_history(lst: list, value: str) -> list:
    value = value.strip()
    if not value:
        return lst
    lst = [x for x in lst if x != value]
    lst.insert(0, value)
    return lst[:MAX_HISTORY]


# ─────────────────────────────────────────────────────────────────────────────
#  Colors / fonts
# ─────────────────────────────────────────────────────────────────────────────

CLR = {
    "bg":         "#0d1117",
    "panel":      "#161b22",
    "input":      "#1c2128",
    "border":     "#30363d",
    "border_hi":  "#58a6ff",
    "accent":     "#1f6feb",
    "success":    "#238636",
    "success_h":  "#2ea043",
    "danger":     "#da3633",
    "danger_h":   "#f85149",
    "text":       "#e6edf3",
    "muted":      "#7d8590",
    "label":      "#8b949e",
    "brand":      "#58a6ff",
    "item_hover": "#21262d",
}

FM = ("Consolas",          9)
FL = ("Segoe UI",          9)
FB = ("Segoe UI Semibold", 9)
FT = ("Segoe UI",         13, "bold")
FS = ("Segoe UI",          8)


# ─────────────────────────────────────────────────────────────────────────────
#  HistoryEntry — input field with dropdown history
# ─────────────────────────────────────────────────────────────────────────────

class HistoryEntry(tk.Frame):
    def __init__(self, master, items=None, show="", **kw):
        super().__init__(master, bg=CLR["panel"], **kw)
        self._items = list(items or [])
        self._show  = show
        self._popup = None

        self.columnconfigure(0, weight=1)

        self.var = tk.StringVar()
        self._e  = tk.Entry(self, textvariable=self.var,
                            show=show, font=FM,
                            bg=CLR["input"], fg=CLR["text"],
                            insertbackground=CLR["text"],
                            highlightbackground=CLR["border"],
                            highlightcolor=CLR["border_hi"],
                            highlightthickness=1, bd=0, relief="flat")
        self._e.grid(row=0, column=0, sticky="ew", ipady=5)

        self._btn = tk.Button(self, text="▾", font=("Segoe UI", 8),
                              bg=CLR["input"], fg=CLR["muted"],
                              activebackground=CLR["accent"],
                              activeforeground=CLR["text"],
                              bd=0, padx=7, pady=0,
                              cursor="hand2", relief="flat",
                              command=self._toggle)
        self._btn.grid(row=0, column=1, sticky="ns", padx=(1, 0), ipady=5)

        self.bind_all("<Button-1>", self._on_global_click)

    def get(self)          -> str: return self.var.get()
    def set(self, v: str):         self.var.set(v)
    def update_items(self, items): self._items = list(items)

    def _toggle(self):
        if self._popup and self._popup.winfo_exists():
            self._close()
        elif self._items:
            self._open()

    def _open(self):
        self._close()
        pop = tk.Toplevel(self)
        pop.overrideredirect(True)
        pop.configure(bg=CLR["border_hi"])
        self._popup = pop

        self.update_idletasks()
        rx = self.winfo_rootx()
        ry = self.winfo_rooty() + self.winfo_height()
        rw = self.winfo_width()

        ITEM_H  = 28
        visible = min(len(self._items), 7)

        outer = tk.Frame(pop, bg=CLR["input"],
                         highlightbackground=CLR["border_hi"],
                         highlightthickness=1)
        outer.pack(fill="both", expand=True)

        cv = tk.Canvas(outer, bg=CLR["input"], bd=0,
                       highlightthickness=0,
                       width=rw - 2, height=visible * ITEM_H)
        cv.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(outer, orient="vertical", command=cv.yview,
                          bg=CLR["input"], troughcolor=CLR["panel"],
                          bd=0, width=10)
        if len(self._items) > visible:
            sb.pack(side="right", fill="y")
        cv.configure(yscrollcommand=sb.set)

        inner = tk.Frame(cv, bg=CLR["input"])
        wid   = cv.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: (cv.configure(scrollregion=cv.bbox("all")),
                               cv.itemconfig(wid, width=cv.winfo_width())))

        for item in self._items:
            label = ("*" * min(len(item), 14)) if self._show else item
            fr = tk.Frame(inner, bg=CLR["input"], cursor="hand2")
            fr.pack(fill="x")
            lb = tk.Label(fr, text=label, font=FM, anchor="w",
                          bg=CLR["input"], fg=CLR["text"], padx=10, pady=5)
            lb.pack(fill="x")

            def _sel(v=item):
                self.set(v); self._close()

            def _ent(e, f=fr, l=lb):
                f.configure(bg=CLR["item_hover"])
                l.configure(bg=CLR["item_hover"])

            def _lv(e, f=fr, l=lb):
                f.configure(bg=CLR["input"])
                l.configure(bg=CLR["input"])

            fr.bind("<Button-1>", lambda e, s=_sel: s())
            lb.bind("<Button-1>", lambda e, s=_sel: s())
            fr.bind("<Enter>", _ent); fr.bind("<Leave>", _lv)
            lb.bind("<Enter>", _ent); lb.bind("<Leave>", _lv)

        pop.geometry(f"{rw}+{rx}+{ry}")
        pop.lift()

    def _close(self):
        if self._popup and self._popup.winfo_exists():
            self._popup.destroy()
        self._popup = None

    def _on_global_click(self, event):
        if not (self._popup and self._popup.winfo_exists()):
            return
        px, py = self._popup.winfo_rootx(), self._popup.winfo_rooty()
        pw, ph = self._popup.winfo_width(),  self._popup.winfo_height()
        if not (px <= event.x_root <= px + pw and
                py <= event.y_root <= py + ph):
            self._close()


# ─────────────────────────────────────────────────────────────────────────────
#  Main application
# ─────────────────────────────────────────────────────────────────────────────

class SignToolGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SignTool GUI — polsoft.ITS™")
        self.resizable(True, False)
        self.configure(bg=CLR["bg"])

        try:
            self.iconbitmap(default="")
        except Exception:
            pass

        self._signtool = find_signtool()
        self.history   = load_history()
        self._lang     = "en"           # default language

        self._theme()
        self._build()
        self._autosize()

    # ── i18n helper ──────────────────────────────────────────────────────────

    def _(self, key: str, **kw) -> str:
        t = TRANSLATIONS[self._lang].get(key, key)
        return t.format(**kw) if kw else t

    # ── layout helpers ───────────────────────────────────────────────────────

    def _autosize(self):
        self.update_idletasks()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.minsize(w, h)

    def _theme(self):
        s = ttk.Style(self)
        s.theme_use("default")
        s.configure("TCheckbutton",
                    background=CLR["panel"],
                    foreground=CLR["text"], font=FL)
        s.map("TCheckbutton",
              background=[("active", CLR["panel"])],
              foreground=[("active", CLR["brand"])])

    def _sep(self, p, text, row):
        f = tk.Frame(p, bg=CLR["panel"])
        f.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(10, 2))
        tk.Label(f, text=text, font=FB,
                 bg=CLR["panel"], fg=CLR["brand"]).pack(side="left", padx=12)
        tk.Frame(f, bg=CLR["border"], height=1).pack(
            side="left", fill="x", expand=True, padx=(4, 12))
        return f

    def _lbl(self, p, text, row):
        l = tk.Label(p, text=text, font=FL,
                     bg=CLR["panel"], fg=CLR["label"])
        l.grid(row=row, column=0, sticky="w", padx=(14, 10), pady=4)
        return l

    def _browse_btn(self, p, cmd, row):
        b = tk.Button(p, text="…", command=cmd,
                      bg=CLR["input"], fg=CLR["brand"],
                      activebackground=CLR["accent"],
                      activeforeground=CLR["text"],
                      font=FB, bd=0, padx=10, pady=4,
                      cursor="hand2", relief="flat")
        b.grid(row=row, column=2, padx=(6, 14), pady=4, sticky="ew")
        return b

    # ── build ─────────────────────────────────────────────────────────────────

    def _build(self):
        self.columnconfigure(0, weight=1)
        self._build_header()
        self._build_form()
        self._build_footer()

    def _build_header(self):
        h = tk.Frame(self, bg=CLR["panel"],
                     highlightbackground=CLR["border"],
                     highlightthickness=1)
        h.grid(row=0, column=0, sticky="ew")
        h.columnconfigure(1, weight=1)

        tk.Frame(h, bg=CLR["accent"], height=3).grid(
            row=0, column=0, columnspan=3, sticky="ew")

        tk.Label(h, text="🔏", font=("Segoe UI Emoji", 22),
                 bg=CLR["panel"], fg=CLR["brand"]).grid(
            row=1, column=0, padx=(16, 8), pady=(10, 10))

        info = tk.Frame(h, bg=CLR["panel"])
        info.grid(row=1, column=1, sticky="w")
        tk.Label(info, text="SignTool GUI",
                 font=FT, bg=CLR["panel"], fg=CLR["text"]).pack(anchor="w")
        self._lbl_subtitle = tk.Label(
            info, text=self._("app_subtitle"),
            font=FS, bg=CLR["panel"], fg=CLR["muted"])
        self._lbl_subtitle.pack(anchor="w")

        right = tk.Frame(h, bg=CLR["panel"])
        right.grid(row=1, column=2, padx=12, sticky="e")

        # language toggle button
        self._btn_lang = tk.Button(
            right, text=self._("btn_lang"),
            command=self._toggle_lang,
            bg=CLR["input"], fg=CLR["brand"],
            activebackground=CLR["accent"],
            activeforeground=CLR["text"],
            font=FS, bd=0, padx=8, pady=3,
            cursor="hand2", relief="flat")
        self._btn_lang.pack(anchor="e", pady=(0, 4))

        # signtool status
        st_name = os.path.basename(self._signtool) if self._signtool else ""
        st_txt  = (self._("st_found", name=st_name)
                   if self._signtool else self._("st_missing"))
        st_clr  = "#3fb950" if self._signtool else "#d29922"
        self._lbl_st = tk.Label(right, text=st_txt, font=FS,
                                bg=CLR["panel"], fg=st_clr)
        self._lbl_st.pack(anchor="e")
        tk.Label(right, text=f"v{__version__}", font=FS,
                 bg=CLR["panel"], fg=CLR["muted"]).pack(anchor="e")

    def _build_form(self):
        outer = tk.Frame(self, bg=CLR["bg"])
        outer.grid(row=1, column=0, sticky="ew", padx=16, pady=(12, 0))
        outer.columnconfigure(0, weight=1)

        panel = tk.Frame(outer, bg=CLR["panel"],
                         highlightbackground=CLR["border"],
                         highlightthickness=1)
        panel.grid(row=0, column=0, sticky="ew")
        panel.columnconfigure(1, weight=1)

        # ── file to sign ────────────────────────────────────────────────────
        self._sep_file = self._sep(panel, self._("sec_file"), row=0)
        self._lbl_file = self._lbl(panel, self._("lbl_file"), 1)
        self.he_file   = HistoryEntry(panel, items=self.history.get("files", []))
        self.he_file.grid(row=1, column=1, sticky="ew", pady=4)
        self._btn_browse_file = self._browse_btn(
            panel, lambda: self._browse(
                self.he_file,
                self._("browse_file_title"),
                [(self._("browse_ft_binary"),
                  "*.exe *.dll *.msi *.cab *.appx"),
                 (self._("browse_ft_all"), "*.*")],
                "files"), 1)

        # ── certificate ─────────────────────────────────────────────────────
        self._sep_cert = self._sep(panel, self._("sec_cert"), row=2)
        self._lbl_cert = self._lbl(panel, self._("lbl_cert"), 3)
        self.he_cert   = HistoryEntry(panel, items=self.history.get("certs", []))
        self.he_cert.grid(row=3, column=1, sticky="ew", pady=4)
        self._btn_browse_cert = self._browse_btn(
            panel, lambda: self._browse(
                self.he_cert,
                self._("browse_cert_title"),
                [(self._("browse_ft_cert"), "*.pfx *.p12"),
                 (self._("browse_ft_all"), "*.*")],
                "certs"), 3)

        self._lbl_pass = self._lbl(panel, self._("lbl_password"), 4)
        pw = tk.Frame(panel, bg=CLR["panel"])
        pw.grid(row=4, column=1, columnspan=2, sticky="ew",
                pady=4, padx=(0, 14))
        pw.columnconfigure(0, weight=1)

        self.he_pass = HistoryEntry(pw,
                                    items=self.history.get("passwords", []),
                                    show="*")
        self.he_pass.grid(row=0, column=0, sticky="ew")

        self.var_showp = tk.BooleanVar(value=False)
        self._chk_showp = ttk.Checkbutton(
            pw, text=self._("lbl_show_pass"),
            variable=self.var_showp,
            command=self._toggle_pass)
        self._chk_showp.grid(row=0, column=1, padx=(10, 0))

        # ── advanced options ─────────────────────────────────────────────────
        self._sep_adv = self._sep(panel, self._("sec_advanced"), row=5)
        opt = tk.Frame(panel, bg=CLR["panel"])
        opt.grid(row=6, column=0, columnspan=3, sticky="w",
                 padx=0, pady=(4, 14))

        self.var_ts    = tk.BooleanVar(value=True)
        self.var_tsurl = tk.StringVar(value="http://timestamp.sectigo.com")
        self.var_hash  = tk.StringVar(value="sha256")

        self._chk_ts = ttk.Checkbutton(opt, text=self._("lbl_timestamp"),
                                        variable=self.var_ts)
        self._chk_ts.grid(row=0, column=0, sticky="w", padx=(14, 6))
        tk.Entry(opt, textvariable=self.var_tsurl,
                 width=28, font=FM,
                 bg=CLR["input"], fg=CLR["text"],
                 insertbackground=CLR["text"],
                 highlightbackground=CLR["border"],
                 highlightthickness=1, bd=0, relief="flat").grid(
            row=0, column=1, sticky="ew", ipady=4, pady=2)

        self._lbl_alg = tk.Label(opt, text=self._("lbl_algorithm"),
                                  font=FL, bg=CLR["panel"], fg=CLR["label"])
        self._lbl_alg.grid(row=1, column=0, sticky="w",
                           padx=(14, 6), pady=(4, 0))
        ttk.Combobox(opt, textvariable=self.var_hash,
                     values=["sha256", "sha384", "sha512"],
                     state="readonly", width=10, font=FL).grid(
            row=1, column=1, sticky="w", pady=(4, 0))

        # ── action buttons ───────────────────────────────────────────────────
        btns = tk.Frame(outer, bg=CLR["bg"])
        btns.grid(row=1, column=0, sticky="e", pady=12)

        self.btn_sign = tk.Button(
            btns, text=self._("btn_sign"),
            command=self._on_sign,
            bg=CLR["success"], fg=CLR["text"],
            activebackground=CLR["success_h"],
            activeforeground=CLR["text"],
            font=FB, bd=0, padx=26, pady=9,
            cursor="hand2", relief="flat")
        self.btn_sign.pack(side="right", padx=(8, 0))

        self.btn_cancel = tk.Button(
            btns, text=self._("btn_cancel"),
            command=self._on_cancel,
            bg=CLR["danger"], fg=CLR["text"],
            activebackground=CLR["danger_h"],
            activeforeground=CLR["text"],
            font=FB, bd=0, padx=26, pady=9,
            cursor="hand2", relief="flat")
        self.btn_cancel.pack(side="right")

    def _build_footer(self):
        f = tk.Frame(self, bg=CLR["panel"],
                     highlightbackground=CLR["border"],
                     highlightthickness=1)
        f.grid(row=2, column=0, sticky="ew")
        f.columnconfigure(1, weight=1)

        self._btn_clear = tk.Button(
            f, text=self._("btn_clear_history"),
            command=self._clear_history,
            bg=CLR["panel"], fg=CLR["muted"],
            activebackground=CLR["input"],
            activeforeground=CLR["danger_h"],
            font=FS, bd=0, padx=10, pady=0,
            cursor="hand2", relief="flat")
        self._btn_clear.grid(row=0, column=0, sticky="w",
                             padx=(8, 0), pady=6)

        tk.Label(f, text=f"{__copyright__}  •  {__email__}  •  {__github__}",
                 font=FS, bg=CLR["panel"], fg=CLR["muted"]).grid(
            row=0, column=1, sticky="e", padx=(0, 12), pady=6)

    # ── language toggle ───────────────────────────────────────────────────────

    def _toggle_lang(self):
        self._lang = "pl" if self._lang == "en" else "en"
        self._retranslate()

    def _retranslate(self):
        """Update all translatable widget texts without rebuilding."""
        # header
        self._lbl_subtitle.configure(text=self._("app_subtitle"))
        self._btn_lang.configure(text=self._("btn_lang"))
        st_name = os.path.basename(self._signtool) if self._signtool else ""
        self._lbl_st.configure(
            text=(self._("st_found", name=st_name)
                  if self._signtool else self._("st_missing")))
        # section separators — find label widgets inside frames
        for sep_frame, key in [
            (self._sep_file, "sec_file"),
            (self._sep_cert, "sec_cert"),
            (self._sep_adv,  "sec_advanced"),
        ]:
            for child in sep_frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(text=self._(key))
                    break
        # row labels
        self._lbl_file.configure(text=self._("lbl_file"))
        self._lbl_cert.configure(text=self._("lbl_cert"))
        self._lbl_pass.configure(text=self._("lbl_password"))
        self._chk_showp.configure(text=self._("lbl_show_pass"))
        self._chk_ts.configure(text=self._("lbl_timestamp"))
        self._lbl_alg.configure(text=self._("lbl_algorithm"))
        # buttons
        self.btn_sign.configure(text=self._("btn_sign"))
        self.btn_cancel.configure(text=self._("btn_cancel"))
        self._btn_clear.configure(text=self._("btn_clear_history"))
        # browse button filetypes are re-bound on each click so no update needed

    # ── UI events ─────────────────────────────────────────────────────────────

    def _toggle_pass(self):
        sh = "" if self.var_showp.get() else "*"
        self.he_pass._e.configure(show=sh)
        self.he_pass._show = sh

    def _browse(self, widget: HistoryEntry,
                title: str, filetypes: list, key: str):
        path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if path:
            widget.set(path)
            self.history[key] = push_history(self.history.get(key, []), path)
            widget.update_items(self.history[key])
            save_history(self.history)

    def _clear_history(self):
        if not messagebox.askyesno(self._("clear_title"),
                                   self._("clear_confirm")):
            return
        self.history = {"certs": [], "passwords": [], "files": []}
        save_history(self.history)
        self.he_cert.update_items([])
        self.he_pass.update_items([])
        self.he_file.update_items([])
        messagebox.showinfo(self._("clear_done_title"),
                            self._("clear_done_msg"))

    # ── validation ────────────────────────────────────────────────────────────

    def _validate(self) -> bool:
        if not self._signtool:
            messagebox.showerror(self._("title_error"),
                                 self._("err_no_signtool"))
            return False

        errors = []
        ft = self.he_file.get().strip()
        ct = self.he_cert.get().strip()

        if not ft:
            errors.append(self._("err_no_file"))
        elif not os.path.isfile(ft):
            errors.append(self._("err_file_missing", path=ft))

        if not ct:
            errors.append(self._("err_no_cert"))
        elif not os.path.isfile(ct):
            errors.append(self._("err_cert_missing", path=ct))

        if errors:
            messagebox.showerror(self._("err_title"), "\n".join(errors))
            return False

        if not self.he_pass.get():
            return messagebox.askyesno(self._("warn_no_pass_title"),
                                       self._("warn_no_pass_msg"))
        return True

    # ── actions ───────────────────────────────────────────────────────────────

    def _on_cancel(self):
        if messagebox.askyesno(self._("quit_title"),
                               self._("quit_confirm")):
            self.destroy()

    def _on_sign(self):
        if not self._validate():
            return
        for val, key, widget in [
            (self.he_cert.get(), "certs",     self.he_cert),
            (self.he_pass.get(), "passwords", self.he_pass),
            (self.he_file.get(), "files",     self.he_file),
        ]:
            if val.strip():
                self.history[key] = push_history(
                    self.history.get(key, []), val)
                widget.update_items(self.history[key])
        save_history(self.history)

        self.btn_sign.configure(state="disabled",
                                text=self._("btn_signing"))
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        cmd = [
            self._signtool, "sign",
            "/f",  self.he_cert.get().strip(),
            "/p",  self.he_pass.get(),
            "/fd", self.var_hash.get(),
            "/v",
        ]
        if self.var_ts.get() and self.var_tsurl.get().strip():
            cmd += ["/tr", self.var_tsurl.get().strip(),
                    "/td", self.var_hash.get()]
        cmd.append(self.he_file.get().strip())

        def done(ok, msg):
            self.btn_sign.configure(state="normal",
                                    text=self._("btn_sign"))
            (messagebox.showinfo if ok else messagebox.showerror)(
                self._("title_success" if ok else "title_error"), msg)

        try:
            r = subprocess.run(cmd, capture_output=True,
                               text=True, encoding="utf-8", errors="replace")
            if r.returncode == 0:
                self.after(0, lambda: done(True, self._("sign_ok")))
            else:
                detail = (r.stdout + "\n" + r.stderr).strip()[:500]
                self.after(0, lambda: done(
                    False, self._("sign_fail",
                                  code=r.returncode, detail=detail)))
        except FileNotFoundError:
            self.after(0, lambda: done(
                False, self._("sign_not_found", path=self._signtool)))
        except Exception as exc:
            self.after(0, lambda: done(False, str(exc)))


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = SignToolGUI()
    app.mainloop()
