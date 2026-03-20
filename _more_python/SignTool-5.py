import sys
import subprocess
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel,
    QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QCompleter,
    QFrame, QStackedWidget, QComboBox
)
from PyQt6.QtCore import Qt, QSettings, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import (
    QColor, QPainter, QPainterPath, QBrush, QPen,
    QLinearGradient, QRadialGradient
)

# ══════════════════════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════════════════════
TR = {
    "en": {
        "window_title":     "SignTool  ·  Sign · Verify · Install",
        "header_sub":       "Sign · Verify · Install  ·  SHA-256  ·  DigiCert",
        "tab_sign":         "▶  Sign",
        "tab_verify":       "🔍  Verify",
        "tab_install":      "📥  Install",
        # Sign page
        "lbl_target":       "Target File",
        "ph_target":        "path/to/application.exe",
        "lbl_cert":         "Certificate (PFX / P12)",
        "ph_cert":          "path/to/certificate.pfx",
        "lbl_password":     "Password",
        "ph_password":      "••••••••",
        "btn_browse":       "Browse",
        "btn_show":         "Show",
        "btn_hide":         "Hide",
        "btn_sign":         "▶   SIGN  FILE",
        # Verify page
        "lbl_verify_file":  "File to Verify",
        "ph_verify":        "path/to/signed_file.exe",
        "lbl_options":      "Options",
        "opt_deep":         "⚙  Deep Check",
        "opt_timestamp":    "🕐  Require Timestamp",
        "btn_verify":       "🔍   VERIFY  SIGNATURE",
        # Install page
        "lbl_inst_file":    "Certificate File  (PFX / P12 / CER / CRT)",
        "ph_inst_file":     "path/to/certificate.pfx",
        "lbl_inst_pass":    "Password  (PFX only)",
        "ph_inst_pass":     "leave blank for CER / CRT",
        "lbl_store":        "Target Store",
        "warn_admin":       "⚠  Installation may require Administrator privileges.",
        "btn_install":      "📥   INSTALL  CERTIFICATE",
        # Log
        "lbl_log":          "Output Log",
        "log_ready":        "// awaiting command...",
        # Log messages
        "log_no_file":      "  ⚠  No target file.",
        "log_no_cert":      "  ⚠  No certificate.",
        "log_no_verify":    "  ⚠  No file to verify.",
        "log_no_inst":      "  ⚠  No certificate file.",
        "log_sign_ok":      "\n  ✔  Signing successful.\n",
        "log_sign_fail":    "\n  ✖  Signing failed  (exit {code})\n",
        "log_verify_ok":    "\n  ✔  Signature VALID.\n",
        "log_verify_fail":  "\n  ✖  INVALID  (exit {code})\n",
        "log_details":      "  ─── Certificate Details ───\n",
        "log_no_details":   "  (no details found)",
        "log_inst_ok":      "\n  ✔  Installed to '{store}' store successfully.\n",
        "log_inst_fail":    "\n  ✖  Installation failed  (exit {code})\n",
        "log_need_admin":   "  ⚠  Try running as Administrator.\n",
        "log_running":      "  ⟳  Running...",
        "log_installing":   "  ⟳  Installing...",
        "stdout_lbl":       "── stdout ──",
        "stderr_lbl":       "── stderr ──",
        # Cert detail field names
        "cert_issued_to":   "Issued to",
        "cert_issued_by":   "Issued by",
        "cert_expires":     "Expires",
        "cert_sha1":        "SHA1 hash",
        "cert_sign_time":   "Signing time",
        # File dialogs
        "dlg_select_file":  "Select File",
        "dlg_select_cert":  "Select Certificate",
        "dlg_select_verify":"Select File to Verify",
        "dlg_select_inst":  "Select Certificate",
        "dlg_all_files":    "All Files (*.*)",
        "dlg_certs":        "Certificates (*.pfx *.p12)",
        "dlg_inst_certs":   "Certificates (*.pfx *.p12 *.cer *.crt)",
        # Theme toggle
        "theme_dark":       "DARK",
        "theme_light":      "LIGHT",
        # Lang toggle
        "lang_btn":         "PL",
    },
    "pl": {
        "window_title":     "SignTool  ·  Podpisz · Weryfikuj · Instaluj",
        "header_sub":       "Podpisz · Weryfikuj · Instaluj  ·  SHA-256  ·  DigiCert",
        "tab_sign":         "▶  Podpisz",
        "tab_verify":       "🔍  Weryfikuj",
        "tab_install":      "📥  Instaluj",
        # Sign page
        "lbl_target":       "Plik docelowy",
        "ph_target":        "ścieżka/do/aplikacji.exe",
        "lbl_cert":         "Certyfikat (PFX / P12)",
        "ph_cert":          "ścieżka/do/certyfikatu.pfx",
        "lbl_password":     "Hasło",
        "ph_password":      "••••••••",
        "btn_browse":       "Wybierz",
        "btn_show":         "Pokaż",
        "btn_hide":         "Ukryj",
        "btn_sign":         "▶   PODPISZ  PLIK",
        # Verify page
        "lbl_verify_file":  "Plik do weryfikacji",
        "ph_verify":        "ścieżka/do/podpisanego.exe",
        "lbl_options":      "Opcje",
        "opt_deep":         "⚙  Pełna weryfikacja",
        "opt_timestamp":    "🕐  Wymagaj znacznika czasu",
        "btn_verify":       "🔍   WERYFIKUJ  PODPIS",
        # Install page
        "lbl_inst_file":    "Plik certyfikatu  (PFX / P12 / CER / CRT)",
        "ph_inst_file":     "ścieżka/do/certyfikatu.pfx",
        "lbl_inst_pass":    "Hasło  (tylko PFX)",
        "ph_inst_pass":     "pozostaw puste dla CER / CRT",
        "lbl_store":        "Magazyn docelowy",
        "warn_admin":       "⚠  Instalacja może wymagać uprawnień Administratora.",
        "btn_install":      "📥   INSTALUJ  CERTYFIKAT",
        # Log
        "lbl_log":          "Dziennik zdarzeń",
        "log_ready":        "// oczekiwanie na polecenie...",
        # Log messages
        "log_no_file":      "  ⚠  Nie podano pliku docelowego.",
        "log_no_cert":      "  ⚠  Nie podano certyfikatu.",
        "log_no_verify":    "  ⚠  Nie podano pliku do weryfikacji.",
        "log_no_inst":      "  ⚠  Nie podano pliku certyfikatu.",
        "log_sign_ok":      "\n  ✔  Podpisywanie zakończone sukcesem.\n",
        "log_sign_fail":    "\n  ✖  Błąd podpisywania  (exit {code})\n",
        "log_verify_ok":    "\n  ✔  Podpis jest WAŻNY.\n",
        "log_verify_fail":  "\n  ✖  Podpis NIEWAŻNY  (exit {code})\n",
        "log_details":      "  ─── Szczegóły certyfikatu ───\n",
        "log_no_details":   "  (brak szczegółów)",
        "log_inst_ok":      "\n  ✔  Zainstalowano do magazynu '{store}'.\n",
        "log_inst_fail":    "\n  ✖  Instalacja nieudana  (exit {code})\n",
        "log_need_admin":   "  ⚠  Uruchom program jako Administrator.\n",
        "log_running":      "  ⟳  Przetwarzanie...",
        "log_installing":   "  ⟳  Instalowanie...",
        "stdout_lbl":       "── stdout ──",
        "stderr_lbl":       "── stderr ──",
        # Cert detail field names
        "cert_issued_to":   "Wystawiono dla",
        "cert_issued_by":   "Wystawca",
        "cert_expires":     "Ważny do",
        "cert_sha1":        "Hash SHA1",
        "cert_sign_time":   "Czas podpisu",
        # File dialogs
        "dlg_select_file":  "Wybierz plik",
        "dlg_select_cert":  "Wybierz certyfikat",
        "dlg_select_verify":"Wybierz plik do weryfikacji",
        "dlg_select_inst":  "Wybierz certyfikat",
        "dlg_all_files":    "Wszystkie pliki (*.*)",
        "dlg_certs":        "Certyfikaty (*.pfx *.p12)",
        "dlg_inst_certs":   "Certyfikaty (*.pfx *.p12 *.cer *.crt)",
        # Theme toggle
        "theme_dark":       "CIEMNY",
        "theme_light":      "JASNY",
        # Lang toggle
        "lang_btn":         "EN",
    },
}

# ══════════════════════════════════════════════════════════
#  THEMES
# ══════════════════════════════════════════════════════════
THEMES = {
    "dark": {
        "bg_base":      QColor(4, 12, 35),
        "orb1":         (30, 80, 200, 55),
        "orb2":         (0, 140, 220, 45),
        "orb3":         (80, 40, 180, 35),
        "grid":         QColor(60, 120, 220, 7),
        "vign":         QColor(0, 5, 20, 90),
        "panel_fill":   QColor(200, 220, 255, 13),
        "panel_accent": QColor(30, 80, 180, 28),
        "gloss":        QColor(255, 255, 255, 18),
        "border_top":   QColor(160, 210, 255, 75),
        "border_mid":   QColor(100, 170, 255, 40),
        "border_bot":   QColor(80, 140, 220, 25),
    },
    "light": {
        "bg_base":      QColor(220, 232, 255),
        "orb1":         (100, 160, 255, 55),
        "orb2":         (60, 180, 240, 40),
        "orb3":         (150, 100, 240, 30),
        "grid":         QColor(80, 130, 220, 10),
        "vign":         QColor(180, 200, 240, 60),
        "panel_fill":   QColor(255, 255, 255, 100),
        "panel_accent": QColor(180, 210, 255, 120),
        "gloss":        QColor(255, 255, 255, 80),
        "border_top":   QColor(100, 160, 255, 120),
        "border_mid":   QColor(80, 130, 220, 80),
        "border_bot":   QColor(60, 110, 200, 50),
    },
}

STYLE_DARK = """
QWidget{font-family:'Segoe UI','Arial',sans-serif;font-size:12px;color:#e8f0ff;}
QLineEdit{background-color:rgba(255,255,255,0.07);border:1px solid rgba(120,180,255,0.25);border-radius:6px;padding:6px 10px;color:#ddeeff;font-size:12px;selection-background-color:rgba(80,160,255,0.5);}
QLineEdit:focus{border:1px solid rgba(100,180,255,0.7);background-color:rgba(255,255,255,0.11);}
QLineEdit:hover{border:1px solid rgba(120,180,255,0.45);background-color:rgba(255,255,255,0.09);}
QComboBox{background-color:rgba(255,255,255,0.07);border:1px solid rgba(120,180,255,0.25);border-radius:6px;padding:6px 10px;color:#ddeeff;font-size:12px;}
QComboBox:focus{border:1px solid rgba(100,180,255,0.7);}
QComboBox::drop-down{border:none;width:20px;}
QComboBox::down-arrow{image:none;border-left:4px solid transparent;border-right:4px solid transparent;border-top:5px solid rgba(120,180,255,0.6);margin-right:6px;}
QComboBox QAbstractItemView{background-color:rgba(10,25,60,0.97);border:1px solid rgba(100,160,255,0.3);color:#c0dcff;selection-background-color:rgba(60,130,230,0.5);}
QPushButton{background-color:rgba(80,140,220,0.18);border:1px solid rgba(120,180,255,0.35);border-radius:6px;padding:6px 14px;color:#a8d4ff;font-size:12px;font-weight:bold;}
QPushButton:hover{background-color:rgba(100,170,255,0.28);border:1px solid rgba(150,210,255,0.6);color:#cce8ff;}
QPushButton:pressed{background-color:rgba(60,120,200,0.35);color:#88bbff;}
#ActionButton{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 rgba(60,140,255,0.45),stop:0.45 rgba(40,110,230,0.35),stop:0.5 rgba(20,80,200,0.25),stop:1 rgba(10,60,180,0.35));border:1px solid rgba(120,200,255,0.6);border-radius:8px;color:#b8e0ff;font-size:13px;font-weight:bold;letter-spacing:2px;padding:10px 20px;}
#ActionButton:hover{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 rgba(80,160,255,0.55),stop:1 rgba(20,80,195,0.45));border:1px solid rgba(160,220,255,0.8);color:#ddf0ff;}
#ActionButton:pressed{background:rgba(30,90,200,0.4);color:#88c4ff;}
#ActionButton:disabled{background:rgba(30,60,120,0.2);border:1px solid rgba(80,120,200,0.2);color:rgba(150,200,255,0.3);}
QTextEdit{background-color:rgba(0,10,30,0.55);border:1px solid rgba(80,140,220,0.25);border-radius:6px;color:#7ac4ff;font-family:'Consolas','Courier New',monospace;font-size:11px;padding:8px;selection-background-color:rgba(80,160,255,0.4);}
QScrollBar:vertical{background:transparent;width:5px;border-radius:2px;}
QScrollBar::handle:vertical{background:rgba(100,160,255,0.3);border-radius:2px;min-height:16px;}
QScrollBar::handle:vertical:hover{background:rgba(130,190,255,0.55);}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0px;}
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:none;}
QAbstractItemView{background-color:rgba(10,25,60,0.92);border:1px solid rgba(100,160,255,0.3);color:#c0dcff;selection-background-color:rgba(60,130,230,0.5);font-size:12px;}
"""

STYLE_LIGHT = """
QWidget{font-family:'Segoe UI','Arial',sans-serif;font-size:12px;color:#1a2a4a;}
QLineEdit{background-color:rgba(255,255,255,0.75);border:1px solid rgba(80,130,210,0.35);border-radius:6px;padding:6px 10px;color:#1a2a4a;font-size:12px;selection-background-color:rgba(80,160,255,0.35);}
QLineEdit:focus{border:1px solid rgba(60,120,220,0.8);background-color:rgba(255,255,255,0.92);}
QLineEdit:hover{border:1px solid rgba(80,140,220,0.55);background-color:rgba(255,255,255,0.85);}
QComboBox{background-color:rgba(255,255,255,0.75);border:1px solid rgba(80,130,210,0.35);border-radius:6px;padding:6px 10px;color:#1a2a4a;font-size:12px;}
QComboBox:focus{border:1px solid rgba(60,120,220,0.8);}
QComboBox::drop-down{border:none;width:20px;}
QComboBox::down-arrow{image:none;border-left:4px solid transparent;border-right:4px solid transparent;border-top:5px solid rgba(60,100,200,0.7);margin-right:6px;}
QComboBox QAbstractItemView{background-color:rgba(240,245,255,0.98);border:1px solid rgba(80,130,210,0.35);color:#1a2a4a;selection-background-color:rgba(100,160,255,0.3);}
QPushButton{background-color:rgba(80,140,220,0.15);border:1px solid rgba(80,130,210,0.4);border-radius:6px;padding:6px 14px;color:#2a4a90;font-size:12px;font-weight:bold;}
QPushButton:hover{background-color:rgba(80,140,220,0.25);border:1px solid rgba(60,120,200,0.7);color:#1a3a80;}
QPushButton:pressed{background-color:rgba(60,110,190,0.3);color:#0a2a70;}
#ActionButton{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 rgba(80,150,255,0.55),stop:0.45 rgba(60,120,235,0.45),stop:0.5 rgba(40,100,215,0.38),stop:1 rgba(30,85,200,0.48));border:1px solid rgba(80,160,255,0.7);border-radius:8px;color:#ffffff;font-size:13px;font-weight:bold;letter-spacing:2px;padding:10px 20px;}
#ActionButton:hover{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 rgba(100,170,255,0.65),stop:1 rgba(40,100,220,0.58));border:1px solid rgba(100,180,255,0.9);color:#ffffff;}
#ActionButton:pressed{background:rgba(40,100,210,0.55);color:#e0eeff;}
#ActionButton:disabled{background:rgba(80,120,200,0.15);border:1px solid rgba(80,120,200,0.25);color:rgba(80,120,200,0.4);}
QTextEdit{background-color:rgba(240,246,255,0.85);border:1px solid rgba(80,130,210,0.3);border-radius:6px;color:#1a3a6a;font-family:'Consolas','Courier New',monospace;font-size:11px;padding:8px;selection-background-color:rgba(80,160,255,0.3);}
QScrollBar:vertical{background:transparent;width:5px;border-radius:2px;}
QScrollBar::handle:vertical{background:rgba(80,130,220,0.35);border-radius:2px;min-height:16px;}
QScrollBar::handle:vertical:hover{background:rgba(60,110,200,0.6);}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0px;}
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:none;}
QAbstractItemView{background-color:rgba(240,245,255,0.98);border:1px solid rgba(80,130,210,0.3);color:#1a2a4a;selection-background-color:rgba(100,160,255,0.3);font-size:12px;}
"""

# ══════════════════════════════════════════════════════════
#  CERT STORES (localised labels, fixed keys)
# ══════════════════════════════════════════════════════════
CERT_STORE_KEYS = ["My", "Root", "CA", "TrustedPublisher", "AuthRoot"]
CERT_STORE_LABELS = {
    "en": [
        "My  — Personal",
        "Root  — Trusted Root CAs",
        "CA  — Intermediate CAs",
        "TrustedPublisher",
        "AuthRoot",
    ],
    "pl": [
        "Mój  — Osobisty",
        "Główny  — Zaufane główne CA",
        "CA  — Pośrednie CA",
        "TrustedPublisher",
        "AuthRoot",
    ],
}

def install_cert_certutil(cert_path, store, password):
    ext = cert_path.lower().split(".")[-1]
    if ext in ("pfx", "p12"):
        cmd = (["certutil", "-f", "-p", password, "-importpfx", store, cert_path]
               if password else ["certutil", "-f", "-importpfx", store, cert_path])
    else:
        cmd = ["certutil", "-f", "-addstore", store, cert_path]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -1, "", str(e)


# ══════════════════════════════════════════════════════════
#  GLASS PANEL
# ══════════════════════════════════════════════════════════
class GlassPanel(QFrame):
    def __init__(self, parent=None, accent=False):
        super().__init__(parent)
        self.accent = accent
        self._theme = "dark"
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_theme(self, name):
        self._theme = name
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect()
        th = THEMES[self._theme]
        path = QPainterPath()
        path.addRoundedRect(0, 0, r.width(), r.height(), 10, 10)
        p.fillPath(path, th["panel_accent"] if self.accent else th["panel_fill"])
        gloss = QPainterPath()
        gloss.addRoundedRect(1, 1, r.width() - 2, r.height() // 2, 9, 9)
        gg = QLinearGradient(0, 0, 0, r.height() // 2)
        gg.setColorAt(0, th["gloss"])
        gg.setColorAt(1, QColor(255, 255, 255, 0))
        p.fillPath(gloss, QBrush(gg))
        bg = QLinearGradient(0, 0, 0, r.height())
        bg.setColorAt(0,   th["border_top"])
        bg.setColorAt(0.5, th["border_mid"])
        bg.setColorAt(1,   th["border_bot"])
        p.setPen(QPen(QBrush(bg), 1))
        p.drawPath(path)
        p.end()


# ══════════════════════════════════════════════════════════
#  THEME TOGGLE
# ══════════════════════════════════════════════════════════
class ThemeToggle(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(52, 26)
        self._is_light = False
        self._anim_pos = 0.0
        self._anim_dir = 0
        self._timer = QTimer(self)
        self._timer.setInterval(12)
        self._timer.timeout.connect(self._step)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _step(self):
        self._anim_pos = max(0.0, min(1.0, self._anim_pos + self._anim_dir * 0.08))
        self.update()
        if self._anim_pos in (0.0, 1.0):
            self._timer.stop()

    def set_light(self, val):
        self._is_light = val
        self._anim_pos = 1.0 if val else 0.0
        self.update()

    def mousePressEvent(self, _):
        self._is_light = not self._is_light
        self._anim_dir = 1 if self._is_light else -1
        self._timer.start()
        self.toggled.emit(self._is_light)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        t = self._anim_pos
        w, h = self.width(), self.height()

        def lerp(a, b, x): return int(a + (b - a) * x)
        track = QColor(lerp(40, 220, t), lerp(80, 215, t), lerp(180, 255, t), lerp(130, 210, t))
        tp = QPainterPath()
        tp.addRoundedRect(0, 0, w, h, h // 2, h // 2)
        p.fillPath(tp, track)
        p.setPen(QPen(QColor(120, 180, 255, 70), 1))
        p.drawPath(tp)

        pad = 3
        tr = h - pad * 2
        tx = pad + (w - pad * 2 - tr) * t

        glow = QRadialGradient(tx + tr / 2, h / 2, tr)
        if self._is_light:
            glow.setColorAt(0, QColor(255, 230, 100, 55))
        else:
            glow.setColorAt(0, QColor(100, 160, 255, 40))
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(glow))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(int(tx - 2), int(h / 2 - tr / 2 - 2), tr + 4, tr + 4)

        tg = QLinearGradient(tx, pad, tx, pad + tr)
        if self._is_light:
            tg.setColorAt(0, QColor(255, 240, 160))
            tg.setColorAt(1, QColor(240, 190, 60))
        else:
            tg.setColorAt(0, QColor(160, 210, 255))
            tg.setColorAt(1, QColor(80, 150, 230))
        p.setBrush(QBrush(tg))
        p.setPen(QPen(QColor(255, 255, 255, 55), 1))
        p.drawEllipse(int(tx), pad, tr, tr)

        cx, cy = tx + tr / 2, h / 2
        if t > 0.5:
            a = int(200 * (t - 0.5) * 2)
            p.setPen(QPen(QColor(180, 120, 10, a), 1.5))
            p.setBrush(Qt.BrushStyle.NoBrush)
            for i in range(8):
                ang = math.radians(i * 45)
                p.drawLine(int(cx + 4.5 * math.cos(ang)), int(cy + 4.5 * math.sin(ang)),
                           int(cx + 6.5 * math.cos(ang)), int(cy + 6.5 * math.sin(ang)))
            p.setBrush(QColor(200, 140, 10, a))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx - 3), int(cy - 3), 6, 6)
        else:
            a = int(200 * (1 - t * 2)) if t < 0.5 else 0
            p.setBrush(QColor(200, 220, 255, a))
            p.setPen(Qt.PenStyle.NoPen)
            moon = QPainterPath()
            moon.addEllipse(int(cx - 3.5), int(cy - 3.5), 7, 7)
            cut = QPainterPath()
            cut.addEllipse(int(cx - 1), int(cy - 4), 6, 6)
            p.drawPath(moon.subtracted(cut))
        p.end()


# ══════════════════════════════════════════════════════════
#  LANGUAGE TOGGLE BUTTON
# ══════════════════════════════════════════════════════════
class LangButton(QWidget):
    toggled = pyqtSignal(str)   # emits "en" or "pl"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(44, 24)
        self._lang = "en"
        self._theme = "dark"
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_theme(self, t):
        self._theme = t
        self.update()

    def set_lang(self, lang):
        self._lang = lang
        self.update()

    def mousePressEvent(self, _):
        self._lang = "pl" if self._lang == "en" else "en"
        self.update()
        self.toggled.emit(self._lang)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        is_dark = self._theme == "dark"

        # Background pill
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, h // 2, h // 2)
        if is_dark:
            p.fillPath(path, QColor(40, 90, 200, 55))
            p.setPen(QPen(QColor(100, 170, 255, 80), 1))
        else:
            p.fillPath(path, QColor(180, 210, 255, 130))
            p.setPen(QPen(QColor(80, 130, 220, 120), 1))
        p.drawPath(path)

        # EN / PL split — highlight active half
        mid = w // 2
        left_active = self._lang == "en"

        hl = QPainterPath()
        if left_active:
            hl.addRoundedRect(1, 1, mid - 1, h - 2, (h - 2) // 2, (h - 2) // 2)
        else:
            hl.addRoundedRect(mid, 1, mid - 1, h - 2, (h - 2) // 2, (h - 2) // 2)
        if is_dark:
            p.fillPath(hl, QColor(80, 160, 255, 70))
        else:
            p.fillPath(hl, QColor(80, 140, 220, 80))

        # Labels
        font = p.font()
        font.setPointSize(8)
        font.setBold(True)
        p.setFont(font)

        en_alpha = 255 if self._lang == "en" else (130 if is_dark else 110)
        pl_alpha = 255 if self._lang == "pl" else (130 if is_dark else 110)
        col = 220 if is_dark else 30

        p.setPen(QColor(col, col + 20, 255, en_alpha) if is_dark else QColor(20, 50, 180, en_alpha))
        p.drawText(0, 0, mid, h, Qt.AlignmentFlag.AlignCenter, "EN")
        p.setPen(QColor(col, col + 20, 255, pl_alpha) if is_dark else QColor(20, 50, 180, pl_alpha))
        p.drawText(mid, 0, mid, h, Qt.AlignmentFlag.AlignCenter, "PL")
        p.end()


# ══════════════════════════════════════════════════════════
#  TAB BAR
# ══════════════════════════════════════════════════════════
class TabBar(QWidget):
    tab_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current = 0
        self._theme = "dark"
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(36)
        self._lay = QHBoxLayout(self)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(5)
        self._btns = []
        for i in range(3):
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, x=i: self._select(x))
            self._btns.append(btn)
            self._lay.addWidget(btn)
        self._lay.addStretch()
        self._restyle()

    def set_theme(self, name):
        self._theme = name
        self._restyle()

    def set_labels(self, labels):
        for btn, lbl in zip(self._btns, labels):
            btn.setText(lbl)

    def _select(self, idx):
        self._current = idx
        self._restyle()
        self.tab_changed.emit(idx)

    def _restyle(self):
        if self._theme == "dark":
            on  = ("QPushButton{background:rgba(60,140,255,0.35);border:1px solid rgba(120,200,255,0.6);"
                   "border-radius:6px;color:#cce8ff;font-weight:bold;padding:6px 16px;font-size:12px;}")
            off = ("QPushButton{background:rgba(255,255,255,0.05);border:1px solid rgba(100,160,255,0.18);"
                   "border-radius:6px;color:rgba(160,200,255,0.5);padding:6px 16px;font-size:12px;}"
                   "QPushButton:hover{background:rgba(80,140,220,0.15);color:#a0ccff;}")
        else:
            on  = ("QPushButton{background:rgba(60,120,220,0.25);border:1px solid rgba(60,130,220,0.7);"
                   "border-radius:6px;color:#1a3a80;font-weight:bold;padding:6px 16px;font-size:12px;}")
            off = ("QPushButton{background:rgba(255,255,255,0.5);border:1px solid rgba(80,130,200,0.3);"
                   "border-radius:6px;color:rgba(60,100,180,0.6);padding:6px 16px;font-size:12px;}"
                   "QPushButton:hover{background:rgba(255,255,255,0.75);color:#2a4a90;}")
        for i, b in enumerate(self._btns):
            b.setStyleSheet(on if i == self._current else off)


# ══════════════════════════════════════════════════════════
#  WORKERS
# ══════════════════════════════════════════════════════════
class Worker(QThread):
    result_ready = pyqtSignal(int, str, str)
    def __init__(self, cmd):
        super().__init__(); self.cmd = cmd
    def run(self):
        try:
            r = subprocess.run(self.cmd, capture_output=True, text=True, shell=False)
            self.result_ready.emit(r.returncode, r.stdout, r.stderr)
        except Exception as e:
            self.result_ready.emit(-1, "", str(e))

class InstWorker(QThread):
    def __init__(self, fn): super().__init__(); self._fn = fn
    def run(self): self._fn()


# ══════════════════════════════════════════════════════════
#  AERO BACKGROUND
# ══════════════════════════════════════════════════════════
class AeroBackground(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._off = 0
        self._theme = "dark"
        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(40)

    def _tick(self):
        self._off = (self._off + 1) % 360
        self.update()

    def set_theme(self, name):
        self._theme = name
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        th = THEMES[self._theme]
        p.fillRect(0, 0, w, h, th["bg_base"])

        def orb(cx, cy, rad, rgba):
            r, g, b, a = rgba
            gr = QRadialGradient(cx, cy, rad)
            gr.setColorAt(0, QColor(r, g, b, a))
            gr.setColorAt(1, QColor(r // 3, g // 3, b // 3, 0))
            p.setBrush(QBrush(gr))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx - rad), int(cy - rad), rad * 2, rad * 2)

        o = self._off
        orb(w * .3  + math.sin(math.radians(o * .7)) * 50,
            h * .25 + math.cos(math.radians(o * .5)) * 25, 240, th["orb1"])
        orb(w * .75 + math.cos(math.radians(o * .6)) * 40,
            h * .65 + math.sin(math.radians(o * .8)) * 35, 190, th["orb2"])
        orb(w * .15 + math.sin(math.radians(o * .4 + 90)) * 35,
            h * .82, 160, th["orb3"])

        pen = QPen(th["grid"]); pen.setWidth(1); p.setPen(pen)
        for x in range(0, w, 38): p.drawLine(x, 0, x, h)
        for y in range(0, h, 38): p.drawLine(0, y, w, y)

        vgn = QLinearGradient(0, h * .65, 0, h)
        vgn.setColorAt(0, QColor(0, 0, 0, 0))
        vgn.setColorAt(1, th["vign"])
        p.setBrush(QBrush(vgn)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(0, int(h * .65), w, h)
        p.end()


# ══════════════════════════════════════════════════════════
#  MAIN WINDOW
# ══════════════════════════════════════════════════════════
class SignToolGUI(AeroBackground):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(620, 520)
        self.resize(640, 540)

        self.settings = QSettings("polsoftITS", "SignToolGUI")
        self.history_files     = self.settings.value("history_files", [])
        self.history_certs     = self.settings.value("history_certs", [])
        self.history_passwords = self.settings.value("history_passwords", [])
        self._workers  = []
        self._panels   = []
        self._slbls    = []   # section QLabel list for retranslation

        self._theme = self.settings.value("theme", "dark")
        self._lang  = self.settings.value("lang",  "en")

        self.setStyleSheet(STYLE_DARK if self._theme == "dark" else STYLE_LIGHT)
        self.set_theme(self._theme)
        self._build_ui()
        self._apply_lang(self._lang, init=True)

    # ── translation helper ─────────────────────────────────
    def t(self, key, **kw):
        s = TR[self._lang].get(key, key)
        return s.format(**kw) if kw else s

    # ──────────────────────────────────────────────────────
    #  BUILD UI  (called once)
    # ──────────────────────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 14, 16, 16)
        root.setSpacing(9)

        # ── Header ──
        hdr = self._panel(accent=True)
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(14, 9, 14, 9)
        hl.setSpacing(8)

        self._title_lbl = QLabel("✦  SignTool GUI")
        self._sub_lbl   = QLabel()
        self._title_lbl.setStyleSheet("color:#a8d8ff;font-size:16px;font-weight:bold;letter-spacing:2px;background:transparent;")
        self._sub_lbl.setStyleSheet("color:rgba(140,190,255,0.5);font-size:10px;letter-spacing:2px;background:transparent;")

        self.theme_toggle = ThemeToggle()
        self.theme_toggle.set_light(self._theme == "light")
        self.theme_toggle.toggled.connect(self._on_theme)

        self._theme_lbl = QLabel()
        self._theme_lbl.setStyleSheet("color:rgba(140,190,255,0.6);font-size:10px;letter-spacing:1px;background:transparent;")

        self.lang_btn = LangButton()
        self.lang_btn.set_lang(self._lang)
        self.lang_btn.set_theme(self._theme)
        self.lang_btn.toggled.connect(self._on_lang)

        hl.addWidget(self._title_lbl)
        hl.addStretch()
        hl.addWidget(self._sub_lbl)
        hl.addSpacing(12)
        hl.addWidget(self._theme_lbl)
        hl.addWidget(self.theme_toggle)
        hl.addSpacing(8)
        hl.addWidget(self.lang_btn)
        root.addWidget(hdr)

        # ── Tabs ──
        self.tabs = TabBar()
        self.tabs.set_theme(self._theme)
        self.tabs.tab_changed.connect(lambda i: self.stack.setCurrentIndex(i))
        root.addWidget(self.tabs)

        # ── Pages ──
        self.stack = QStackedWidget()
        self.stack.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.stack.addWidget(self._page_sign())
        self.stack.addWidget(self._page_verify())
        self.stack.addWidget(self._page_install())
        root.addWidget(self.stack, stretch=1)

        # ── Log ──
        lp = self._panel()
        ll = QVBoxLayout(lp)
        ll.setContentsMargins(12, 8, 12, 12)
        ll.setSpacing(5)
        self._log_lbl = self._slbl_raw()
        ll.addWidget(self._log_lbl)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(120)
        ll.addWidget(self.log)
        root.addWidget(lp)

    # ──────────────────────────────────────────────────────
    #  SIGN PAGE
    # ──────────────────────────────────────────────────────
    def _page_sign(self):
        pg = self._tw()
        vb = QVBoxLayout(pg); vb.setContentsMargins(0,0,0,0); vb.setSpacing(8)
        card = self._panel()
        cl = QVBoxLayout(card); cl.setContentsMargins(14,12,14,14); cl.setSpacing(8)

        self._sl_target = self._slbl_raw(); cl.addWidget(self._sl_target)
        self.sign_file_edit = self._le(self.history_files)
        cl.addLayout(self._browse_row(self.sign_file_edit, self._choose_sign_file))

        self._sl_cert = self._slbl_raw(); cl.addWidget(self._sl_cert)
        self.cert_edit = self._le(self.history_certs)
        cl.addLayout(self._browse_row(self.cert_edit, self._choose_cert))

        self._sl_pass = self._slbl_raw(); cl.addWidget(self._sl_pass)
        pr = QHBoxLayout(); pr.setSpacing(6)
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedWidth(72)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.toggled.connect(lambda c: (
            self.pass_edit.setEchoMode(QLineEdit.EchoMode.Normal if c else QLineEdit.EchoMode.Password),
            self.toggle_btn.setText(self.t("btn_hide") if c else self.t("btn_show"))
        ))
        pr.addWidget(self.pass_edit); pr.addWidget(self.toggle_btn)
        cl.addLayout(pr)
        vb.addWidget(card)

        self.btn_sign = self._action_btn(self.do_sign)
        vb.addWidget(self.btn_sign)
        vb.addStretch()
        return pg

    # ──────────────────────────────────────────────────────
    #  VERIFY PAGE
    # ──────────────────────────────────────────────────────
    def _page_verify(self):
        pg = self._tw()
        vb = QVBoxLayout(pg); vb.setContentsMargins(0,0,0,0); vb.setSpacing(8)
        card = self._panel()
        cl = QVBoxLayout(card); cl.setContentsMargins(14,12,14,14); cl.setSpacing(8)

        self._sl_vfile = self._slbl_raw(); cl.addWidget(self._sl_vfile)
        self.verify_file_edit = self._le(self.history_files)
        cl.addLayout(self._browse_row(self.verify_file_edit, self._choose_verify_file))

        self._sl_opts = self._slbl_raw(); cl.addWidget(self._sl_opts)
        orow = QHBoxLayout(); orow.setSpacing(6)
        self.btn_deep = self._opt_btn(True)
        self.btn_ts   = self._opt_btn(False)
        self.btn_deep.toggled.connect(lambda _: self._restyle_opt(self.btn_deep))
        self.btn_ts.toggled.connect(lambda _: self._restyle_opt(self.btn_ts))
        orow.addWidget(self.btn_deep); orow.addWidget(self.btn_ts); orow.addStretch()
        cl.addLayout(orow)
        vb.addWidget(card)

        self.btn_verify = self._action_btn(self.do_verify)
        vb.addWidget(self.btn_verify)
        vb.addStretch()
        return pg

    # ──────────────────────────────────────────────────────
    #  INSTALL PAGE
    # ──────────────────────────────────────────────────────
    def _page_install(self):
        pg = self._tw()
        vb = QVBoxLayout(pg); vb.setContentsMargins(0,0,0,0); vb.setSpacing(8)
        card = self._panel()
        cl = QVBoxLayout(card); cl.setContentsMargins(14,12,14,14); cl.setSpacing(8)

        self._sl_ifile = self._slbl_raw(); cl.addWidget(self._sl_ifile)
        self.inst_file_edit = self._le(self.history_certs)
        cl.addLayout(self._browse_row(self.inst_file_edit, self._choose_inst_file))

        self._sl_ipass = self._slbl_raw(); cl.addWidget(self._sl_ipass)
        ip = QHBoxLayout(); ip.setSpacing(6)
        self.inst_pass_edit = QLineEdit()
        self.inst_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.inst_toggle = QPushButton()
        self.inst_toggle.setFixedWidth(72)
        self.inst_toggle.setCheckable(True)
        self.inst_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.inst_toggle.toggled.connect(lambda c: (
            self.inst_pass_edit.setEchoMode(QLineEdit.EchoMode.Normal if c else QLineEdit.EchoMode.Password),
            self.inst_toggle.setText(self.t("btn_hide") if c else self.t("btn_show"))
        ))
        ip.addWidget(self.inst_pass_edit); ip.addWidget(self.inst_toggle)
        cl.addLayout(ip)

        self._sl_store = self._slbl_raw(); cl.addWidget(self._sl_store)
        self.store_combo = QComboBox()
        self.store_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        cl.addWidget(self.store_combo)

        self._warn_lbl = QLabel()
        self._warn_lbl.setWordWrap(True)
        cl.addWidget(self._warn_lbl)
        vb.addWidget(card)

        self.btn_install = self._action_btn(self.do_install)
        vb.addWidget(self.btn_install)
        vb.addStretch()
        return pg

    # ──────────────────────────────────────────────────────
    #  LANGUAGE APPLICATION  (full retranslation)
    # ──────────────────────────────────────────────────────
    def _apply_lang(self, lang, init=False):
        self._lang = lang
        self.settings.setValue("lang", lang)
        self.lang_btn.set_lang(lang)
        is_light = self._theme == "light"

        self.setWindowTitle(self.t("window_title"))
        self._sub_lbl.setText(self.t("header_sub"))
        self._theme_lbl.setText(self.t("theme_light") if is_light else self.t("theme_dark"))

        # Tabs
        self.tabs.set_labels([self.t("tab_sign"), self.t("tab_verify"), self.t("tab_install")])

        # Sign page
        self._sl_target.setText(self.t("lbl_target").upper())
        self.sign_file_edit.setPlaceholderText(self.t("ph_target"))
        self._sl_cert.setText(self.t("lbl_cert").upper())
        self.cert_edit.setPlaceholderText(self.t("ph_cert"))
        self._sl_pass.setText(self.t("lbl_password").upper())
        self.pass_edit.setPlaceholderText(self.t("ph_password"))
        self.toggle_btn.setText(self.t("btn_show"))
        self.btn_sign.setText(self.t("btn_sign"))

        # Verify page
        self._sl_vfile.setText(self.t("lbl_verify_file").upper())
        self.verify_file_edit.setPlaceholderText(self.t("ph_verify"))
        self._sl_opts.setText(self.t("lbl_options").upper())
        self.btn_deep.setText(self.t("opt_deep"))
        self.btn_ts.setText(self.t("opt_timestamp"))
        self.btn_verify.setText(self.t("btn_verify"))

        # Install page
        self._sl_ifile.setText(self.t("lbl_inst_file").upper())
        self.inst_file_edit.setPlaceholderText(self.t("ph_inst_file"))
        self._sl_ipass.setText(self.t("lbl_inst_pass").upper())
        self.inst_pass_edit.setPlaceholderText(self.t("ph_inst_pass"))
        self.inst_toggle.setText(self.t("btn_show"))
        self._sl_store.setText(self.t("lbl_store").upper())
        self._warn_lbl.setText(self.t("warn_admin"))
        self.btn_install.setText(self.t("btn_install"))

        # Store combo
        current_idx = self.store_combo.currentIndex()
        self.store_combo.blockSignals(True)
        self.store_combo.clear()
        for lbl in CERT_STORE_LABELS[lang]:
            self.store_combo.addItem(lbl)
        self.store_combo.setCurrentIndex(max(0, current_idx))
        self.store_combo.blockSignals(False)

        # Log
        self._log_lbl.setText(self.t("lbl_log").upper())
        if init:
            self.log.setPlaceholderText(self.t("log_ready"))

        # Style refresh
        self._refresh_label_styles(is_light)

    def _on_lang(self, lang):
        self._apply_lang(lang)

    # ──────────────────────────────────────────────────────
    #  THEME APPLICATION
    # ──────────────────────────────────────────────────────
    def _on_theme(self, is_light):
        name = "light" if is_light else "dark"
        self._theme = name
        self.settings.setValue("theme", name)
        self.set_theme(name)
        self.setStyleSheet(STYLE_LIGHT if is_light else STYLE_DARK)
        for pn in self._panels: pn.set_theme(name)
        self.tabs.set_theme(name)
        self.lang_btn.set_theme(name)
        self._theme_lbl.setText(self.t("theme_light") if is_light else self.t("theme_dark"))
        self._refresh_label_styles(is_light)
        self.update()

    def _refresh_label_styles(self, is_light):
        if is_light:
            ts = "color:#1a3a80;font-size:16px;font-weight:bold;letter-spacing:2px;background:transparent;"
            ss = "color:rgba(40,80,180,0.55);font-size:10px;letter-spacing:2px;background:transparent;"
            ls = "color:rgba(40,90,180,0.75);font-size:10px;font-weight:bold;letter-spacing:2px;background:transparent;"
            ws = "color:rgba(160,100,0,0.8);font-size:11px;background:transparent;"
            ths= "color:rgba(40,90,180,0.65);font-size:10px;letter-spacing:1px;background:transparent;"
        else:
            ts = "color:#a8d8ff;font-size:16px;font-weight:bold;letter-spacing:2px;background:transparent;"
            ss = "color:rgba(140,190,255,0.5);font-size:10px;letter-spacing:2px;background:transparent;"
            ls = "color:rgba(120,190,255,0.7);font-size:10px;font-weight:bold;letter-spacing:2px;background:transparent;"
            ws = "color:rgba(255,200,80,0.65);font-size:11px;background:transparent;"
            ths= "color:rgba(140,190,255,0.6);font-size:10px;letter-spacing:1px;background:transparent;"
        self._title_lbl.setStyleSheet(ts)
        self._sub_lbl.setStyleSheet(ss)
        self._theme_lbl.setStyleSheet(ths)
        self._warn_lbl.setStyleSheet(ws)
        for lbl in self._slbls:
            lbl.setStyleSheet(ls)
        for b in (self.btn_deep, self.btn_ts):
            self._restyle_opt(b)

    # ──────────────────────────────────────────────────────
    #  ACTIONS
    # ──────────────────────────────────────────────────────
    def do_sign(self):
        fp = self.sign_file_edit.text().strip()
        cp = self.cert_edit.text().strip()
        pw = self.pass_edit.text().strip()
        if not fp: return self.log_line(self.t("log_no_file"))
        if not cp: return self.log_line(self.t("log_no_cert"))
        self.add_hist("history_files", self.history_files, fp)
        self.add_hist("history_certs", self.history_certs, cp)
        if pw: self.add_hist("history_passwords", self.history_passwords, pw)
        cmd = ["signtool.exe","sign","/f",cp,"/p",pw,"/fd","sha256",
               "/tr","http://timestamp.digicert.com","/td","sha256",fp]
        self.log_line(f"\n  ╔═  SIGN\n  »  {' '.join(cmd)}\n")
        self._run(cmd, self.btn_sign, self.t("btn_sign"),
                  lambda c,o,e: (self._out(o,e),
                      self.log_line(self.t("log_sign_ok") if c==0 else self.t("log_sign_fail", code=c))))

    def do_verify(self):
        fp = self.verify_file_edit.text().strip()
        if not fp: return self.log_line(self.t("log_no_verify"))
        self.add_hist("history_files", self.history_files, fp)
        cmd = ["signtool.exe","verify","/pa"]
        if self.btn_deep.isChecked(): cmd.append("/all")
        if self.btn_ts.isChecked():   cmd.append("/tw")
        cmd.append(fp)
        cmd_v = ["signtool.exe","verify","/pa","/v",fp]
        self.log_line(f"\n  ╔═  VERIFY\n  »  {' '.join(cmd)}\n")

        def _after(code, out, err):
            self._out(out, err)
            if code == 0:
                self.log_line(self.t("log_verify_ok"))
                self.log_line(self.t("log_details"))
                self._run(cmd_v, self.btn_verify, self.t("btn_verify"),
                          lambda c,o,e: [self.log_line(l) for l in self._parse_cert(o)], restore=True)
            else:
                self.log_line(self.t("log_verify_fail", code=code))
                self.btn_verify.setEnabled(True)
                self.btn_verify.setText(self.t("btn_verify"))
        self._run(cmd, self.btn_verify, self.t("btn_verify"), _after, restore=False)

    def do_install(self):
        fp  = self.inst_file_edit.text().strip()
        pw  = self.inst_pass_edit.text().strip()
        idx = self.store_combo.currentIndex()
        store = CERT_STORE_KEYS[idx] if 0 <= idx < len(CERT_STORE_KEYS) else "My"
        if not fp: return self.log_line(self.t("log_no_inst"))
        self.add_hist("history_certs", self.history_certs, fp)
        self.log_line(f"\n  ╔═  INSTALL\n  »  certutil → store:{store}\n  »  {fp}\n")
        self.btn_install.setEnabled(False)
        self.btn_install.setText(self.t("log_installing"))

        def _fn():
            code, out, err = install_cert_certutil(fp, store, pw)
            self._out(out, err)
            if code == 0:
                self.log_line(self.t("log_inst_ok", store=store))
            else:
                self.log_line(self.t("log_inst_fail", code=code))
                if "access" in (out+err).lower() or code == 5:
                    self.log_line(self.t("log_need_admin"))
            self.btn_install.setEnabled(True)
            self.btn_install.setText(self.t("btn_install"))

        w = InstWorker(_fn)
        self._workers.append(w)
        w.start()

    # ──────────────────────────────────────────────────────
    #  UI HELPERS
    # ──────────────────────────────────────────────────────
    def _panel(self, accent=False):
        pn = GlassPanel(accent=accent)
        pn.set_theme(self._theme)
        self._panels.append(pn)
        return pn

    def _slbl_raw(self):
        lbl = QLabel()
        lbl.setStyleSheet("color:rgba(120,190,255,0.7);font-size:10px;font-weight:bold;letter-spacing:2px;background:transparent;")
        self._slbls.append(lbl)
        return lbl

    def _le(self, hist):
        e = QLineEdit()
        e.setCompleter(QCompleter(hist))
        return e

    def _browse_row(self, edit, cb):
        row = QHBoxLayout(); row.setSpacing(6)
        btn = QPushButton(self.t("btn_browse"))
        btn.setFixedWidth(76)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(cb)
        # keep reference so we can retranslate browse buttons
        row.addWidget(edit); row.addWidget(btn)
        return row

    def _action_btn(self, cb):
        b = QPushButton()
        b.setObjectName("ActionButton")
        b.setMinimumHeight(42)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(cb)
        return b

    def _opt_btn(self, checked):
        b = QPushButton()
        b.setCheckable(True)
        b.setChecked(checked)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        self._restyle_opt(b)
        return b

    def _restyle_opt(self, btn):
        is_light = self._theme == "light"
        if btn.isChecked():
            if is_light:
                btn.setStyleSheet("QPushButton{background:rgba(60,120,220,0.25);border:1px solid rgba(60,120,220,0.7);border-radius:6px;color:#1a3a80;font-weight:bold;padding:6px 14px;}")
            else:
                btn.setStyleSheet("QPushButton{background:rgba(40,120,220,0.35);border:1px solid rgba(120,200,255,0.6);border-radius:6px;color:#cce8ff;font-weight:bold;padding:6px 14px;}")
        else:
            if is_light:
                btn.setStyleSheet("QPushButton{background:rgba(255,255,255,0.5);border:1px solid rgba(80,130,200,0.3);border-radius:6px;color:rgba(60,100,180,0.55);padding:6px 14px;}"
                                  "QPushButton:hover{background:rgba(255,255,255,0.8);color:#2a4a90;}")
            else:
                btn.setStyleSheet("QPushButton{background:rgba(255,255,255,0.05);border:1px solid rgba(100,160,255,0.18);border-radius:6px;color:rgba(160,200,255,0.5);padding:6px 14px;}"
                                  "QPushButton:hover{background:rgba(80,140,220,0.15);color:#a0ccff;}")

    def _tw(self):
        w = QWidget()
        w.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        return w

    # ──────────────────────────────────────────────────────
    #  FILE CHOOSERS
    # ──────────────────────────────────────────────────────
    def _choose_sign_file(self):
        p,_ = QFileDialog.getOpenFileName(self, self.t("dlg_select_file"), "", self.t("dlg_all_files"))
        if p: self.sign_file_edit.setText(p); self.add_hist("history_files",self.history_files,p)

    def _choose_cert(self):
        p,_ = QFileDialog.getOpenFileName(self, self.t("dlg_select_cert"), "", self.t("dlg_certs"))
        if p: self.cert_edit.setText(p); self.add_hist("history_certs",self.history_certs,p)

    def _choose_verify_file(self):
        p,_ = QFileDialog.getOpenFileName(self, self.t("dlg_select_verify"), "", self.t("dlg_all_files"))
        if p: self.verify_file_edit.setText(p); self.add_hist("history_files",self.history_files,p)

    def _choose_inst_file(self):
        p,_ = QFileDialog.getOpenFileName(self, self.t("dlg_select_inst"), "", self.t("dlg_inst_certs"))
        if p: self.inst_file_edit.setText(p); self.add_hist("history_certs",self.history_certs,p)

    # ──────────────────────────────────────────────────────
    #  CMD RUNNER / OUTPUT
    # ──────────────────────────────────────────────────────
    def _run(self, cmd, btn, label, cb, restore=True):
        btn.setEnabled(False)
        btn.setText(self.t("log_running"))
        def _done(c, o, e):
            cb(c, o, e)
            if restore:
                btn.setEnabled(True)
                btn.setText(label)
        w = Worker(cmd)
        self._workers.append(w)
        w.result_ready.connect(_done)
        w.start()

    def _out(self, out, err):
        if out and out.strip(): self.log_line(self.t("stdout_lbl") + "\n" + out.strip())
        if err and err.strip(): self.log_line(self.t("stderr_lbl") + "\n" + err.strip())

    def log_line(self, text):
        self.log.append(text)

    def _parse_cert(self, raw):
        map_en = {"Issued to": "cert_issued_to", "Issued by": "cert_issued_by",
                  "Expires": "cert_expires", "SHA1 hash": "cert_sha1", "Signing time": "cert_sign_time"}
        found = {}
        for line in raw.splitlines():
            s = line.strip()
            for en_key, tr_key in map_en.items():
                if s.lower().startswith(en_key.lower()):
                    v = s[len(en_key):].lstrip(": ").strip()
                    if v: found[tr_key] = v
        if not found:
            return [self.t("log_no_details")]
        pad = max(len(self.t(k)) for k in found) + 2
        return [f"  {self.t(k)+':':<{pad}} {v}" for k, v in found.items()]

    # ──────────────────────────────────────────────────────
    #  HISTORY
    # ──────────────────────────────────────────────────────
    def add_hist(self, key, lst, val):
        if val not in lst:
            lst.insert(0, val); lst[:] = lst[:10]
            self.settings.setValue(key, lst)


# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = SignToolGUI()
    w.show()
    sys.exit(app.exec())
