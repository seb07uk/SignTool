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
"""

__author__      = "Sebastian Januchowski"
__company__     = "polsoft.ITS™ Group"
__email__       = "polsoft.its@fastservice.com"
__github__      = "https://github.com/seb07uk"
__copyright__   = "2026© Sebastian Januchowski & polsoft.ITS™. All rights reserved."
__version__     = "1.0.0"

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess, threading, os, sys, shutil, json


# ─────────────────────────────────────────────────────────────────────────────
#  i18n
# ─────────────────────────────────────────────────────────────────────────────

TRANSLATIONS = {
    "en": {
        "app_subtitle":       "polsoft.ITS™ Group  •  Digital Signature Manager",
        "st_found":           "signtool: {name}",
        "st_missing":         "signtool.exe not found",
        "sec_file":           "FILE TO SIGN",
        "sec_cert":           "CERTIFICATE",
        "sec_advanced":       "ADVANCED OPTIONS",
        "lbl_file":           "File path",
        "lbl_cert":           "Certificate (.pfx)",
        "lbl_password":       "Password",
        "lbl_show_pass":      "Reveal",
        "lbl_timestamp":      "Timestamp URL",
        "lbl_algorithm":      "Algorithm",
        "btn_sign":           "SIGN FILE",
        "btn_signing":        "SIGNING…",
        "btn_cancel":         "CANCEL",
        "btn_clear_history":  "Clear history",
        "btn_lang":           "🌐 PL",
        "browse_file_title":  "Select file to sign",
        "browse_cert_title":  "Select PFX certificate",
        "browse_ft_binary":   "Executable / Library",
        "browse_ft_cert":     "PFX / P12 Certificate",
        "browse_ft_all":      "All files",
        "err_no_signtool":    "signtool.exe not found.\n\nPlace signtool.exe in the application directory or install Windows SDK (10/11).",
        "err_no_file":        "• No file selected for signing.",
        "err_file_missing":   "• File not found:\n  {path}",
        "err_no_cert":        "• No certificate (.pfx) selected.",
        "err_cert_missing":   "• Certificate not found:\n  {path}",
        "err_title":          "Validation error",
        "warn_no_pass_title": "Empty password",
        "warn_no_pass_msg":   "Certificate password is empty. Continue?",
        "sign_ok":            "File signed successfully.",
        "sign_fail":          "Signing failed (code: {code}).\n\n{detail}",
        "sign_not_found":     "Cannot launch signtool:\n{path}",
        "title_success":      "Success",
        "title_error":        "Error",
        "clear_title":        "Clear history",
        "clear_confirm":      "Delete all saved certificates and passwords?",
        "clear_done_title":   "Done",
        "clear_done_msg":     "History cleared.",
        "quit_title":         "Close",
        "quit_confirm":       "Close the application?",
    },
    "pl": {
        "app_subtitle":       "polsoft.ITS™ Group  •  Menedżer podpisów cyfrowych",
        "st_found":           "signtool: {name}",
        "st_missing":         "signtool.exe nie znaleziony",
        "sec_file":           "PLIK DO PODPISANIA",
        "sec_cert":           "CERTYFIKAT",
        "sec_advanced":       "OPCJE ZAAWANSOWANE",
        "lbl_file":           "Ścieżka pliku",
        "lbl_cert":           "Certyfikat (.pfx)",
        "lbl_password":       "Hasło",
        "lbl_show_pass":      "Pokaż",
        "lbl_timestamp":      "Timestamp URL",
        "lbl_algorithm":      "Algorytm",
        "btn_sign":           "PODPISZ",
        "btn_signing":        "PODPISYWANIE…",
        "btn_cancel":         "ANULUJ",
        "btn_clear_history":  "Wyczyść historię",
        "btn_lang":           "🌐 EN",
        "browse_file_title":  "Wybierz plik do podpisania",
        "browse_cert_title":  "Wybierz certyfikat PFX",
        "browse_ft_binary":   "Pliki exe/dll/msi/cab/appx",
        "browse_ft_cert":     "Certyfikat PFX/P12",
        "browse_ft_all":      "Wszystkie pliki",
        "err_no_signtool":    "Nie znaleziono signtool.exe.\n\nUmieść signtool.exe w katalogu aplikacji lub zainstaluj Windows SDK (10/11).",
        "err_no_file":        "• Nie wybrano pliku do podpisania.",
        "err_file_missing":   "• Plik nie istnieje:\n  {path}",
        "err_no_cert":        "• Nie wybrano certyfikatu (.pfx).",
        "err_cert_missing":   "• Certyfikat nie istnieje:\n  {path}",
        "err_title":          "Błąd walidacji",
        "warn_no_pass_title": "Brak hasła",
        "warn_no_pass_msg":   "Hasło certyfikatu jest puste. Kontynuować?",
        "sign_ok":            "Plik został podpisany pomyślnie.",
        "sign_fail":          "Podpisywanie nie powiodło się (kod: {code}).\n\n{detail}",
        "sign_not_found":     "Nie można uruchomić signtool:\n{path}",
        "title_success":      "Sukces",
        "title_error":        "Błąd",
        "clear_title":        "Wyczyść historię",
        "clear_confirm":      "Usunąć wszystkie zapamiętane certyfikaty i hasła?",
        "clear_done_title":   "Gotowe",
        "clear_done_msg":     "Historia została wyczyszczona.",
        "quit_title":         "Zamknij",
        "quit_confirm":       "Zamknąć aplikację?",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
#  Paths / history
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

MAX_HISTORY = 10


def find_signtool():
    for p in SDK_PATHS:
        if p == "signtool.exe":
            if shutil.which("signtool.exe"): return "signtool.exe"
        elif os.path.isfile(p): return p
    return ""


def load_history():
    try:
        if os.path.isfile(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception: pass
    return {"certs": [], "passwords": [], "files": []}


def save_history(h):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(h, f, ensure_ascii=False, indent=2)
    except Exception: pass


def push_history(lst, value):
    v = value.strip()
    if not v: return lst
    lst = [x for x in lst if x != v]
    lst.insert(0, v)
    return lst[:MAX_HISTORY]


# ─────────────────────────────────────────────────────────────────────────────
#  Design tokens — Industrial Precision theme
# ─────────────────────────────────────────────────────────────────────────────

C = {
    # backgrounds
    "bg0":        "#080b0f",   # near-black base
    "bg1":        "#0e1319",   # card / panel
    "bg2":        "#141a22",   # input well
    "bg3":        "#1a2230",   # input hover
    # chrome lines
    "line":       "#1e2a38",
    "line_hi":    "#2a3d52",
    # accent — electric cyan
    "cyan":       "#00d4ff",
    "cyan_dim":   "#0099cc",
    "cyan_glow":  "#003344",
    # success — sharp green
    "green":      "#00e676",
    "green_dim":  "#00b050",
    "green_bg":   "#001a0d",
    # danger — crimson
    "red":        "#ff3d57",
    "red_dim":    "#cc1a30",
    "red_bg":     "#1a0008",
    # text
    "txt":        "#d0dde8",
    "txt_dim":    "#6a7f94",
    "txt_label":  "#4a6070",
    "txt_mono":   "#a8c4d8",
    # status
    "ok":         "#00e676",
    "warn":       "#ffb300",
}

# Fonts
F_DISPLAY = ("Segoe UI",          11, "bold")   # section headers
F_LABEL   = ("Segoe UI",           9)
F_LABELB  = ("Segoe UI Semibold",  9)
F_MONO    = ("Consolas",           9)
F_MONO_S  = ("Consolas",           8)
F_TITLE   = ("Segoe UI",          14, "bold")
F_CAP     = ("Segoe UI Semibold",  7)            # ALL-CAPS section labels
F_BTN     = ("Segoe UI Semibold", 10)
F_MICRO   = ("Segoe UI",           7)


# ─────────────────────────────────────────────────────────────────────────────
#  Tiny reusable widgets
# ─────────────────────────────────────────────────────────────────────────────

class FlatButton(tk.Frame):
    """Styled flat button with hover/press states using tk.Button."""

    def __init__(self, master, text="", command=None,
                 bg_normal=None, bg_hover=None, bg_press=None,
                 fg=C["txt"], font=F_BTN,
                 padx=20, pady=8, radius=4, **kw):
        super().__init__(master, bg=C["bg0"], **kw)
        self._bg_n = bg_normal or C["bg2"]
        self._bg_h = bg_hover  or C["bg3"]
        self._bg_p = bg_press  or C["cyan_glow"]
        self._fg   = fg
        self._font = font
        self._text_var = tk.StringVar(value=text)

        self._btn = tk.Button(
            self,
            textvariable=self._text_var,
            command=command,
            bg=self._bg_n,
            fg=fg,
            activebackground=self._bg_h,
            activeforeground=fg,
            disabledforeground=C["txt_dim"],
            font=font,
            relief="flat", bd=0,
            padx=padx, pady=pady,
            cursor="hand2",
            highlightthickness=0,
            takefocus=0,
        )
        self._btn.pack(fill="both", expand=True)

        self._btn.bind("<Enter>",         self._on_enter)
        self._btn.bind("<Leave>",         self._on_leave)
        self._btn.bind("<ButtonPress-1>", self._on_press)
        self._btn.bind("<ButtonRelease-1>", self._on_release)

    def configure(self, **kw):
        if "text" in kw:
            self._text_var.set(kw.pop("text"))
        if "state" in kw:
            state = kw.pop("state")
            self._btn.configure(
                state=state,
                cursor="arrow" if state == "disabled" else "hand2")
        if kw:
            self._btn.configure(**kw)

    def _on_enter(self, e):
        if str(self._btn["state"]) != "disabled":
            self._btn.configure(bg=self._bg_h)

    def _on_leave(self, e):
        if str(self._btn["state"]) != "disabled":
            self._btn.configure(bg=self._bg_n)

    def _on_press(self, e):
        if str(self._btn["state"]) != "disabled":
            self._btn.configure(bg=self._bg_p)

    def _on_release(self, e):
        if str(self._btn["state"]) != "disabled":
            self._btn.configure(bg=self._bg_h)


class Separator(tk.Canvas):
    """Thin horizontal rule with optional label."""

    def __init__(self, master, label="", **kw):
        super().__init__(master, height=20, bg=C["bg1"],
                         bd=0, highlightthickness=0, **kw)
        self._label = label
        self.bind("<Configure>", self._redraw)

    def _redraw(self, e=None):
        self.delete("all")
        w = self.winfo_width() or 400
        y = 10
        if self._label:
            self.create_text(0, y, text=self._label,
                             font=F_CAP, fill=C["txt_label"],
                             anchor="w")
            tw = len(self._label) * 6 + 8
            self.create_line(tw, y, w, y,
                             fill=C["line"], width=1)
        else:
            self.create_line(0, y, w, y, fill=C["line"], width=1)

    def update_label(self, label):
        self._label = label
        self._redraw()


# ─────────────────────────────────────────────────────────────────────────────
#  HistoryEntry
# ─────────────────────────────────────────────────────────────────────────────

class HistoryEntry(tk.Frame):
    def __init__(self, master, items=None, show="", **kw):
        super().__init__(master, bg=C["bg1"], **kw)
        self._items = list(items or [])
        self._show  = show
        self._popup = None
        self.columnconfigure(0, weight=1)

        # outer border frame
        border = tk.Frame(self,
                          bg=C["line"],
                          highlightthickness=0)
        border.grid(row=0, column=0, columnspan=2, sticky="ew")
        border.columnconfigure(0, weight=1)

        self.var = tk.StringVar()
        self._e  = tk.Entry(border, textvariable=self.var,
                            show=show, font=F_MONO,
                            bg=C["bg2"], fg=C["txt_mono"],
                            insertbackground=C["cyan"],
                            selectbackground=C["cyan_glow"],
                            selectforeground=C["cyan"],
                            relief="flat", bd=0)
        self._e.grid(row=0, column=0, sticky="ew",
                     padx=(1, 0), pady=1, ipady=6)

        self._btn = tk.Label(border, text="▾",
                             font=("Segoe UI", 8),
                             bg=C["bg2"], fg=C["txt_label"],
                             cursor="hand2", padx=8, pady=0)
        self._btn.grid(row=0, column=1, sticky="ns", padx=(0, 1), pady=1)
        self._btn.bind("<Button-1>",   lambda e: self._toggle())
        self._btn.bind("<Enter>",      lambda e: self._btn.configure(fg=C["cyan"]))
        self._btn.bind("<Leave>",      lambda e: self._btn.configure(fg=C["txt_label"]))

        # focus ring
        self._e.bind("<FocusIn>",  lambda e: border.configure(bg=C["cyan_dim"]))
        self._e.bind("<FocusOut>", lambda e: border.configure(bg=C["line"]))
        self.bind_all("<Button-1>", self._on_global_click)

    def get(self)          -> str: return self.var.get()
    def set(self, v: str):         self.var.set(v)
    def update_items(self, items): self._items = list(items)

    def _toggle(self):
        if self._popup and self._popup.winfo_exists(): self._close()
        elif self._items: self._open()

    def _open(self):
        self._close()
        pop = tk.Toplevel(self)
        pop.overrideredirect(True)
        pop.configure(bg=C["cyan_dim"])
        self._popup = pop

        self.update_idletasks()
        rx = self.winfo_rootx()
        ry = self.winfo_rooty() + self.winfo_height()
        rw = self.winfo_width()

        ITEM_H  = 30
        visible = min(len(self._items), 7)

        outer = tk.Frame(pop, bg=C["bg2"],
                         highlightbackground=C["cyan_dim"],
                         highlightthickness=1)
        outer.pack(fill="both", expand=True)

        cv = tk.Canvas(outer, bg=C["bg2"], bd=0, highlightthickness=0,
                       width=rw - 2, height=visible * ITEM_H)
        cv.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(outer, orient="vertical", command=cv.yview,
                          bg=C["bg2"], troughcolor=C["bg1"], bd=0, width=8)
        if len(self._items) > visible: sb.pack(side="right", fill="y")
        cv.configure(yscrollcommand=sb.set)

        inner = tk.Frame(cv, bg=C["bg2"])
        wid   = cv.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: (cv.configure(scrollregion=cv.bbox("all")),
                               cv.itemconfig(wid, width=cv.winfo_width())))

        for item in self._items:
            label = ("*" * min(len(item), 16)) if self._show else item
            fr = tk.Frame(inner, bg=C["bg2"], cursor="hand2")
            fr.pack(fill="x")

            # left accent bar
            bar = tk.Frame(fr, bg=C["bg2"], width=3)
            bar.pack(side="left", fill="y")
            lb = tk.Label(fr, text=label, font=F_MONO,
                          bg=C["bg2"], fg=C["txt_dim"],
                          anchor="w", padx=8, pady=6)
            lb.pack(side="left", fill="x", expand=True)

            def _sel(v=item):         self.set(v); self._close()
            def _ent(e, f=fr, l=lb, b=bar):
                f.configure(bg=C["bg3"]); l.configure(bg=C["bg3"], fg=C["txt"])
                b.configure(bg=C["cyan"])
            def _lv(e, f=fr, l=lb, b=bar):
                f.configure(bg=C["bg2"]); l.configure(bg=C["bg2"], fg=C["txt_dim"])
                b.configure(bg=C["bg2"])

            for w in (fr, lb, bar):
                w.bind("<Button-1>", lambda e, s=_sel: s())
                w.bind("<Enter>", _ent); w.bind("<Leave>", _lv)

        pop.geometry(f"{rw}+{rx}+{ry}")
        pop.lift()

    def _close(self):
        if self._popup and self._popup.winfo_exists(): self._popup.destroy()
        self._popup = None

    def _on_global_click(self, event):
        if not (self._popup and self._popup.winfo_exists()): return
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
        self.configure(bg=C["bg0"])

        try: self.iconbitmap(default="")
        except Exception: pass

        self._signtool = find_signtool()
        self.history   = load_history()
        self._lang     = "en"

        self._theme()
        self._build()
        self._autosize()

    # ── i18n ─────────────────────────────────────────────────────────────────

    def _(self, key, **kw):
        t = TRANSLATIONS[self._lang].get(key, key)
        return t.format(**kw) if kw else t

    # ── layout ───────────────────────────────────────────────────────────────

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
                    background=C["bg1"], foreground=C["txt_dim"],
                    font=F_LABEL, focuscolor="")
        s.map("TCheckbutton",
              background=[("active", C["bg1"])],
              foreground=[("active", C["cyan"])])
        s.configure("TCombobox",
                    fieldbackground=C["bg2"],
                    background=C["bg2"],
                    foreground=C["txt_mono"],
                    selectbackground=C["cyan_glow"],
                    selectforeground=C["cyan"],
                    arrowcolor=C["txt_label"],
                    bordercolor=C["line"],
                    lightcolor=C["line"],
                    darkcolor=C["line"])
        s.map("TCombobox",
              fieldbackground=[("readonly", C["bg2"])],
              foreground=[("readonly", C["txt_mono"])])

    # ── build ─────────────────────────────────────────────────────────────────

    def _build(self):
        self.columnconfigure(0, weight=1)
        self._build_header()
        self._build_body()
        self._build_footer()

    # ── header ────────────────────────────────────────────────────────────────

    def _build_header(self):
        hdr = tk.Frame(self, bg=C["bg1"])
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.columnconfigure(1, weight=1)

        # top accent stripe — gradient-like via 2 lines
        tk.Frame(hdr, bg=C["cyan"],     height=2).grid(
            row=0, column=0, columnspan=3, sticky="ew")
        tk.Frame(hdr, bg=C["cyan_dim"], height=1).grid(
            row=1, column=0, columnspan=3, sticky="ew")

        # left: icon + title block
        left = tk.Frame(hdr, bg=C["bg1"])
        left.grid(row=2, column=0, padx=(18, 12), pady=(14, 14), sticky="w")

        # lock icon in a framed box
        icon_box = tk.Frame(left, bg=C["cyan_glow"],
                            highlightbackground=C["cyan_dim"],
                            highlightthickness=1)
        icon_box.pack(side="left", padx=(0, 14))
        tk.Label(icon_box, text="🔐",
                 font=("Segoe UI Emoji", 20),
                 bg=C["cyan_glow"], fg=C["cyan"],
                 padx=10, pady=8).pack()

        # title + subtitle
        titles = tk.Frame(left, bg=C["bg1"])
        titles.pack(side="left")
        tk.Label(titles, text="SignTool  GUI",
                 font=F_TITLE, bg=C["bg1"], fg=C["txt"]).pack(anchor="w")
        self._lbl_subtitle = tk.Label(
            titles, text=self._("app_subtitle"),
            font=F_MICRO, bg=C["bg1"], fg=C["txt_label"])
        self._lbl_subtitle.pack(anchor="w", pady=(2, 0))

        # right: controls column
        right = tk.Frame(hdr, bg=C["bg1"])
        right.grid(row=2, column=2, padx=(0, 16), sticky="e")

        # language button
        self._btn_lang = tk.Button(
            right, text=self._("btn_lang"),
            command=self._toggle_lang,
            bg=C["bg2"], fg=C["cyan"],
            activebackground=C["cyan_glow"],
            activeforeground=C["cyan"],
            relief="flat", bd=0,
            font=F_MICRO, padx=8, pady=3,
            cursor="hand2")
        self._btn_lang.pack(anchor="e", pady=(0, 6))

        # signtool status badge
        st_name = os.path.basename(self._signtool) if self._signtool else ""
        ok = bool(self._signtool)
        badge = tk.Frame(right,
                         bg=C["green_bg"] if ok else C["red_bg"],
                         highlightbackground=C["ok"] if ok else C["warn"],
                         highlightthickness=1)
        badge.pack(anchor="e")
        dot_clr = C["ok"] if ok else C["warn"]
        tk.Label(badge, text="●", font=("Segoe UI", 6),
                 bg=badge["bg"], fg=dot_clr).pack(side="left", padx=(5, 2))
        st_txt = (self._("st_found", name=st_name)
                  if ok else self._("st_missing"))
        self._lbl_st = tk.Label(badge, text=st_txt,
                                font=F_MONO_S,
                                bg=badge["bg"], fg=dot_clr)
        self._lbl_st.pack(side="left", padx=(0, 6), pady=4)
        self._st_badge = badge
        self._st_dot_clr = dot_clr

        # version
        tk.Label(right, text=f"v{__version__}",
                 font=F_MICRO, bg=C["bg1"],
                 fg=C["txt_label"]).pack(anchor="e", pady=(4, 0))

        # bottom rule
        tk.Frame(hdr, bg=C["line"], height=1).grid(
            row=3, column=0, columnspan=3, sticky="ew")

    # ── body ──────────────────────────────────────────────────────────────────

    def _build_body(self):
        body = tk.Frame(self, bg=C["bg0"])
        body.grid(row=1, column=0, sticky="ew", padx=0)
        body.columnconfigure(0, weight=1)

        # card
        card = tk.Frame(body, bg=C["bg1"],
                        highlightbackground=C["line_hi"],
                        highlightthickness=1)
        card.grid(row=0, column=0, sticky="ew",
                  padx=16, pady=16)
        card.columnconfigure(1, weight=1)

        # ── section: file ──────────────────────────────────────────────────
        self._sep_file = self._sec(card, self._("sec_file"), 0)
        self._lbl_file = self._row_label(card, self._("lbl_file"), 1)
        self.he_file   = HistoryEntry(card, items=self.history.get("files", []))
        self.he_file.grid(row=1, column=1, sticky="ew", pady=(4, 4))
        self._bbf = self._dot_btn(card,
            lambda: self._browse(self.he_file,
                self._("browse_file_title"),
                [(self._("browse_ft_binary"), "*.exe *.dll *.msi *.cab *.appx"),
                 (self._("browse_ft_all"), "*.*")], "files"), 1)

        # ── section: certificate ──────────────────────────────────────────
        self._sep_cert = self._sec(card, self._("sec_cert"), 2)
        self._lbl_cert = self._row_label(card, self._("lbl_cert"), 3)
        self.he_cert   = HistoryEntry(card, items=self.history.get("certs", []))
        self.he_cert.grid(row=3, column=1, sticky="ew", pady=(4, 4))
        self._bbc = self._dot_btn(card,
            lambda: self._browse(self.he_cert,
                self._("browse_cert_title"),
                [(self._("browse_ft_cert"), "*.pfx *.p12"),
                 (self._("browse_ft_all"), "*.*")], "certs"), 3)

        self._lbl_pass = self._row_label(card, self._("lbl_password"), 4)
        pw = tk.Frame(card, bg=C["bg1"])
        pw.grid(row=4, column=1, columnspan=2, sticky="ew",
                pady=(4, 4), padx=(0, 16))
        pw.columnconfigure(0, weight=1)

        self.he_pass = HistoryEntry(pw,
                                    items=self.history.get("passwords", []),
                                    show="*")
        self.he_pass.grid(row=0, column=0, sticky="ew")

        self.var_showp  = tk.BooleanVar(value=False)
        self._chk_showp = ttk.Checkbutton(
            pw, text=self._("lbl_show_pass"),
            variable=self.var_showp,
            command=self._toggle_pass)
        self._chk_showp.grid(row=0, column=1, padx=(10, 0))

        # ── section: advanced ─────────────────────────────────────────────
        self._sep_adv = self._sec(card, self._("sec_advanced"), 5)

        opt = tk.Frame(card, bg=C["bg1"])
        opt.grid(row=6, column=0, columnspan=3, sticky="ew",
                 padx=0, pady=(4, 16))
        opt.columnconfigure(1, weight=1)

        self.var_ts    = tk.BooleanVar(value=True)
        self.var_tsurl = tk.StringVar(value="http://timestamp.sectigo.com")
        self.var_hash  = tk.StringVar(value="sha256")

        self._chk_ts = ttk.Checkbutton(opt, text=self._("lbl_timestamp"),
                                        variable=self.var_ts)
        self._chk_ts.grid(row=0, column=0, sticky="w", padx=(14, 8))

        ts_border = tk.Frame(opt, bg=C["line"])
        ts_border.grid(row=0, column=1, sticky="ew",
                       padx=(0, 16), pady=4)
        ts_border.columnconfigure(0, weight=1)
        tk.Entry(ts_border, textvariable=self.var_tsurl,
                 font=F_MONO, bg=C["bg2"], fg=C["txt_mono"],
                 insertbackground=C["cyan"],
                 selectbackground=C["cyan_glow"],
                 relief="flat", bd=0).grid(
            row=0, column=0, sticky="ew",
            padx=1, pady=1, ipady=5)

        self._lbl_alg = self._row_label(opt, self._("lbl_algorithm"), 1)
        self._lbl_alg.grid(row=1, column=0, sticky="w",
                           padx=(14, 8), pady=(6, 0))
        ttk.Combobox(opt, textvariable=self.var_hash,
                     values=["sha256", "sha384", "sha512"],
                     state="readonly", width=12, font=F_MONO).grid(
            row=1, column=1, sticky="w", padx=(0, 16), pady=(6, 0))

        # ── action buttons ────────────────────────────────────────────────
        btn_row = tk.Frame(body, bg=C["bg0"])
        btn_row.grid(row=1, column=0, sticky="ew",
                     padx=16, pady=(0, 16))
        btn_row.columnconfigure(0, weight=1)

        right_btns = tk.Frame(btn_row, bg=C["bg0"])
        right_btns.grid(row=0, column=1)

        self.btn_cancel = FlatButton(
            right_btns,
            text=self._("btn_cancel"),
            command=self._on_cancel,
            bg_normal=C["red_bg"],
            bg_hover=C["red_dim"],
            bg_press=C["red"],
            fg=C["red"],
            font=F_BTN, padx=22, pady=9, radius=3)
        self.btn_cancel.pack(side="right", padx=(8, 0))

        self.btn_sign = FlatButton(
            right_btns,
            text=self._("btn_sign"),
            command=self._on_sign,
            bg_normal=C["green_bg"],
            bg_hover=C["green_dim"],
            bg_press=C["green"],
            fg=C["green"],
            font=F_BTN, padx=28, pady=9, radius=3)
        self.btn_sign.pack(side="right")

    # ── footer ────────────────────────────────────────────────────────────────

    def _build_footer(self):
        ft = tk.Frame(self, bg=C["bg1"],
                      highlightbackground=C["line"],
                      highlightthickness=1)
        ft.grid(row=2, column=0, sticky="ew")
        ft.columnconfigure(1, weight=1)

        self._btn_clear = tk.Button(
            ft, text=self._("btn_clear_history"),
            command=self._clear_history,
            bg=C["bg1"], fg=C["txt_label"],
            activebackground=C["bg2"],
            activeforeground=C["red"],
            relief="flat", bd=0,
            font=F_MICRO, padx=10, pady=0,
            cursor="hand2")
        self._btn_clear.grid(row=0, column=0, sticky="w",
                             padx=(10, 0), pady=7)

        tk.Label(ft,
                 text=f"{__copyright__}  •  {__email__}  •  {__github__}",
                 font=F_MICRO, bg=C["bg1"],
                 fg=C["txt_label"]).grid(
            row=0, column=1, sticky="e", padx=(0, 14), pady=7)

    # ── widget helpers ────────────────────────────────────────────────────────

    def _sec(self, parent, label, row):
        """Section separator with ALL-CAPS label + line."""
        f = tk.Frame(parent, bg=C["bg1"])
        f.grid(row=row, column=0, columnspan=3, sticky="ew",
               padx=14, pady=(14, 2))
        f.columnconfigure(1, weight=1)

        lbl = tk.Label(f, text=label, font=F_CAP,
                       bg=C["bg1"], fg=C["cyan_dim"])
        lbl.grid(row=0, column=0, sticky="w", padx=(0, 8))
        line = tk.Frame(f, bg=C["line"], height=1)
        line.grid(row=0, column=1, sticky="ew")
        # store ref so we can retranslate
        f._lbl = lbl
        return f

    def _row_label(self, parent, text, row):
        l = tk.Label(parent, text=text, font=F_LABELB,
                     bg=C["bg1"], fg=C["txt_dim"])
        l.grid(row=row, column=0, sticky="w",
               padx=(16, 12), pady=(4, 4))
        return l

    def _dot_btn(self, parent, cmd, row):
        """Small square browse button."""
        b = tk.Button(parent, text="⋯", command=cmd,
                      bg=C["bg2"], fg=C["cyan"],
                      activebackground=C["cyan_glow"],
                      activeforeground=C["cyan"],
                      relief="flat", bd=0,
                      font=("Segoe UI", 11), padx=10, pady=3,
                      cursor="hand2")
        b.grid(row=row, column=2, padx=(6, 16), pady=(4, 4), sticky="ew")
        return b

    # ── i18n ─────────────────────────────────────────────────────────────────

    def _toggle_lang(self):
        self._lang = "pl" if self._lang == "en" else "en"
        self._retranslate()

    def _retranslate(self):
        self._lbl_subtitle.configure(text=self._("app_subtitle"))
        self._btn_lang.configure(text=self._("btn_lang"))
        st_name = os.path.basename(self._signtool) if self._signtool else ""
        self._lbl_st.configure(
            text=(self._("st_found", name=st_name)
                  if self._signtool else self._("st_missing")))
        for frm, key in [(self._sep_file, "sec_file"),
                          (self._sep_cert, "sec_cert"),
                          (self._sep_adv,  "sec_advanced")]:
            frm._lbl.configure(text=self._(key))
        self._lbl_file.configure(text=self._("lbl_file"))
        self._lbl_cert.configure(text=self._("lbl_cert"))
        self._lbl_pass.configure(text=self._("lbl_password"))
        self._chk_showp.configure(text=self._("lbl_show_pass"))
        self._chk_ts.configure(text=self._("lbl_timestamp"))
        self._lbl_alg.configure(text=self._("lbl_algorithm"))
        self.btn_sign.configure(text=self._("btn_sign"))
        self.btn_cancel.configure(text=self._("btn_cancel"))
        self._btn_clear.configure(text=self._("btn_clear_history"))

    # ── UI events ─────────────────────────────────────────────────────────────

    def _toggle_pass(self):
        sh = "" if self.var_showp.get() else "*"
        self.he_pass._e.configure(show=sh)
        self.he_pass._show = sh

    def _browse(self, widget, title, filetypes, key):
        path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if path:
            widget.set(path)
            self.history[key] = push_history(self.history.get(key, []), path)
            widget.update_items(self.history[key])
            save_history(self.history)

    def _clear_history(self):
        if not messagebox.askyesno(self._("clear_title"),
                                   self._("clear_confirm")): return
        self.history = {"certs": [], "passwords": [], "files": []}
        save_history(self.history)
        for w in (self.he_cert, self.he_pass, self.he_file):
            w.update_items([])
        messagebox.showinfo(self._("clear_done_title"),
                            self._("clear_done_msg"))

    # ── validation ────────────────────────────────────────────────────────────

    def _validate(self):
        if not self._signtool:
            messagebox.showerror(self._("title_error"),
                                 self._("err_no_signtool"))
            return False
        errors = []
        ft = self.he_file.get().strip()
        ct = self.he_cert.get().strip()
        if not ft:                   errors.append(self._("err_no_file"))
        elif not os.path.isfile(ft): errors.append(self._("err_file_missing", path=ft))
        if not ct:                   errors.append(self._("err_no_cert"))
        elif not os.path.isfile(ct): errors.append(self._("err_cert_missing", path=ct))
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
        if not self._validate(): return
        for val, key, widget in [
            (self.he_cert.get(), "certs",     self.he_cert),
            (self.he_pass.get(), "passwords", self.he_pass),
            (self.he_file.get(), "files",     self.he_file),
        ]:
            if val.strip():
                self.history[key] = push_history(self.history.get(key, []), val)
                widget.update_items(self.history[key])
        save_history(self.history)
        self.btn_sign.configure(state="disabled", text=self._("btn_signing"))
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        cmd = [self._signtool, "sign",
               "/f", self.he_cert.get().strip(),
               "/p", self.he_pass.get(),
               "/fd", self.var_hash.get(), "/v"]
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
                    False, self._("sign_fail", code=r.returncode, detail=detail)))
        except FileNotFoundError:
            self.after(0, lambda: done(
                False, self._("sign_not_found", path=self._signtool)))
        except Exception as exc:
            self.after(0, lambda: done(False, str(exc)))


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = SignToolGUI()
    app.mainloop()
