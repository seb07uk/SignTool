import sys
import subprocess
import math
import ctypes
import ctypes.wintypes
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
#  STYLESHEET
# ══════════════════════════════════════════════════════════
STYLE = """
QWidget {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 12px;
    color: #e8f0ff;
}
QLineEdit {
    background-color: rgba(255,255,255,0.07);
    border: 1px solid rgba(120,180,255,0.25);
    border-radius: 6px;
    padding: 6px 10px;
    color: #ddeeff;
    font-size: 12px;
    selection-background-color: rgba(80,160,255,0.5);
}
QLineEdit:focus { border: 1px solid rgba(100,180,255,0.7); background-color: rgba(255,255,255,0.11); }
QLineEdit:hover { border: 1px solid rgba(120,180,255,0.45); background-color: rgba(255,255,255,0.09); }
QComboBox {
    background-color: rgba(255,255,255,0.07);
    border: 1px solid rgba(120,180,255,0.25);
    border-radius: 6px;
    padding: 6px 10px;
    color: #ddeeff;
    font-size: 12px;
}
QComboBox:focus { border: 1px solid rgba(100,180,255,0.7); }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox::down-arrow { image: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid rgba(120,180,255,0.6); margin-right: 6px; }
QComboBox QAbstractItemView { background-color: rgba(10,25,60,0.97); border: 1px solid rgba(100,160,255,0.3); color: #c0dcff; selection-background-color: rgba(60,130,230,0.5); }
QPushButton {
    background-color: rgba(80,140,220,0.18);
    border: 1px solid rgba(120,180,255,0.35);
    border-radius: 6px;
    padding: 6px 14px;
    color: #a8d4ff;
    font-size: 12px;
    font-weight: bold;
}
QPushButton:hover { background-color: rgba(100,170,255,0.28); border: 1px solid rgba(150,210,255,0.6); color: #cce8ff; }
QPushButton:pressed { background-color: rgba(60,120,200,0.35); color: #88bbff; }
#ActionButton {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 rgba(60,140,255,0.45), stop:0.45 rgba(40,110,230,0.35),
        stop:0.5 rgba(20,80,200,0.25), stop:1 rgba(10,60,180,0.35));
    border: 1px solid rgba(120,200,255,0.6);
    border-radius: 8px;
    color: #b8e0ff;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 2px;
    padding: 10px 20px;
}
#ActionButton:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 rgba(80,160,255,0.55),stop:1 rgba(20,80,195,0.45)); border: 1px solid rgba(160,220,255,0.8); color: #ddf0ff; }
#ActionButton:pressed { background: rgba(30,90,200,0.4); color: #88c4ff; }
#ActionButton:disabled { background: rgba(30,60,120,0.2); border: 1px solid rgba(80,120,200,0.2); color: rgba(150,200,255,0.3); }
QTextEdit {
    background-color: rgba(0,10,30,0.55);
    border: 1px solid rgba(80,140,220,0.25);
    border-radius: 6px;
    color: #7ac4ff;
    font-family: 'Consolas','Courier New',monospace;
    font-size: 11px;
    padding: 8px;
    selection-background-color: rgba(80,160,255,0.4);
}
QScrollBar:vertical { background: transparent; width: 5px; border-radius: 2px; }
QScrollBar::handle:vertical { background: rgba(100,160,255,0.3); border-radius: 2px; min-height: 16px; }
QScrollBar::handle:vertical:hover { background: rgba(130,190,255,0.55); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
QAbstractItemView { background-color: rgba(10,25,60,0.92); border: 1px solid rgba(100,160,255,0.3); color: #c0dcff; selection-background-color: rgba(60,130,230,0.5); font-size: 12px; }
"""

# ══════════════════════════════════════════════════════════
#  GLASS PANEL
# ══════════════════════════════════════════════════════════
class GlassPanel(QFrame):
    def __init__(self, parent=None, accent=False):
        super().__init__(parent)
        self.accent = accent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect()
        path = QPainterPath()
        path.addRoundedRect(0, 0, r.width(), r.height(), 10, 10)
        fill = QColor(30,80,180,28) if self.accent else QColor(200,220,255,13)
        p.fillPath(path, fill)
        gloss = QPainterPath()
        gloss.addRoundedRect(1, 1, r.width()-2, r.height()//2, 9, 9)
        gg = QLinearGradient(0, 0, 0, r.height()//2)
        gg.setColorAt(0, QColor(255,255,255,18))
        gg.setColorAt(1, QColor(255,255,255,0))
        p.fillPath(gloss, QBrush(gg))
        bg = QLinearGradient(0, 0, 0, r.height())
        bg.setColorAt(0, QColor(160,210,255,75))
        bg.setColorAt(0.5, QColor(100,170,255,40))
        bg.setColorAt(1, QColor(80,140,220,25))
        p.setPen(QPen(QBrush(bg), 1))
        p.drawPath(path)
        p.end()

# ══════════════════════════════════════════════════════════
#  TAB BAR
# ══════════════════════════════════════════════════════════
class TabBar(QWidget):
    tab_changed = pyqtSignal(int)

    ACTIVE = ("QPushButton{background:rgba(60,140,255,0.35);border:1px solid rgba(120,200,255,0.6);"
              "border-radius:6px;color:#cce8ff;font-weight:bold;padding:6px 16px;font-size:12px;}")
    INACTIVE = ("QPushButton{background:rgba(255,255,255,0.05);border:1px solid rgba(100,160,255,0.18);"
                "border-radius:6px;color:rgba(160,200,255,0.5);padding:6px 16px;font-size:12px;}"
                "QPushButton:hover{background:rgba(80,140,220,0.15);color:#a0ccff;}")

    def __init__(self, tabs, parent=None):
        super().__init__(parent)
        self._current = 0
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(36)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        lay.setSpacing(5)
        self._btns = []
        for i, label in enumerate(tabs):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, x=i: self._select(x))
            self._btns.append(btn)
            lay.addWidget(btn)
        lay.addStretch()
        self._restyle()

    def _select(self, idx):
        self._current = idx
        self._restyle()
        self.tab_changed.emit(idx)

    def _restyle(self):
        for i, b in enumerate(self._btns):
            b.setStyleSheet(self.ACTIVE if i == self._current else self.INACTIVE)

# ══════════════════════════════════════════════════════════
#  WORKER
# ══════════════════════════════════════════════════════════
class Worker(QThread):
    result_ready = pyqtSignal(int, str, str)

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        try:
            r = subprocess.run(self.cmd, capture_output=True, text=True, shell=False)
            self.result_ready.emit(r.returncode, r.stdout, r.stderr)
        except Exception as e:
            self.result_ready.emit(-1, "", str(e))

# ══════════════════════════════════════════════════════════
#  AERO BACKGROUND
# ══════════════════════════════════════════════════════════
class AeroBackground(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._off = 0
        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(40)

    def _tick(self):
        self._off = (self._off + 1) % 360
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, QColor(4,12,35))

        def orb(cx, cy, rad, r, g, b, a):
            gr = QRadialGradient(cx, cy, rad)
            gr.setColorAt(0, QColor(r,g,b,a))
            gr.setColorAt(1, QColor(r//3,g//3,b//3,0))
            p.setBrush(QBrush(gr))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx-rad), int(cy-rad), rad*2, rad*2)

        o = self._off
        orb(w*.3+math.sin(math.radians(o*.7))*50, h*.25+math.cos(math.radians(o*.5))*25, 240, 30,80,200,55)
        orb(w*.75+math.cos(math.radians(o*.6))*40, h*.65+math.sin(math.radians(o*.8))*35, 190, 0,140,220,45)
        orb(w*.15+math.sin(math.radians(o*.4+90))*35, h*.82, 160, 80,40,180,35)

        pen = QPen(QColor(60,120,220,7)); pen.setWidth(1); p.setPen(pen)
        for x in range(0,w,38): p.drawLine(x,0,x,h)
        for y in range(0,h,38): p.drawLine(0,y,w,y)

        vgn = QLinearGradient(0,h*.65,0,h)
        vgn.setColorAt(0, QColor(0,0,0,0)); vgn.setColorAt(1, QColor(0,5,20,90))
        p.setBrush(QBrush(vgn)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(0, int(h*.65), w, h)
        p.end()

# ══════════════════════════════════════════════════════════
#  CERT STORES (Windows)
# ══════════════════════════════════════════════════════════
CERT_STORES = [
    ("My  — Personal",            "My"),
    ("Root  — Trusted Root CAs",  "Root"),
    ("CA  — Intermediate CAs",    "CA"),
    ("TrustedPublisher",          "TrustedPublisher"),
    ("AuthRoot",                  "AuthRoot"),
]

def install_cert_certutil(cert_path: str, store: str, password: str) -> tuple[int,str,str]:
    """Instaluje certyfikat przez certutil.exe (działa dla PFX, CER, CRT, P12)."""
    ext = cert_path.lower().split(".")[-1]
    if ext in ("pfx", "p12"):
        cmd = ["certutil", "-f", "-importpfx", store, cert_path]
        if password:
            cmd = ["certutil", "-f", "-p", password, "-importpfx", store, cert_path]
    else:
        cmd = ["certutil", "-f", "-addstore", store, cert_path]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -1, "", str(e)

# ══════════════════════════════════════════════════════════
#  MAIN WINDOW
# ══════════════════════════════════════════════════════════
class SignToolGUI(AeroBackground):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SignTool  ·  Sign · Verify · Install")
        self.setMinimumSize(620, 520)
        self.resize(640, 540)

        self.settings = QSettings("polsoftITS", "SignToolGUI")
        self.history_files = self.settings.value("history_files", [])
        self.history_certs = self.settings.value("history_certs", [])
        self.history_passwords = self.settings.value("history_passwords", [])
        self._workers = []

        self.setStyleSheet(STYLE)
        self._init_ui()

    # ──────────────────────────────────────────────────────
    #  ROOT LAYOUT
    # ──────────────────────────────────────────────────────
    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 14, 16, 16)
        root.setSpacing(9)

        # Header
        hdr = GlassPanel(accent=True)
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(14, 9, 14, 9)
        t = QLabel("✦  SignTool GUI")
        t.setStyleSheet("color:#a8d8ff;font-size:16px;font-weight:bold;letter-spacing:2px;background:transparent;")
        s = QLabel("Sign · Verify · Install  ·  SHA-256  ·  DigiCert")
        s.setStyleSheet("color:rgba(140,190,255,0.5);font-size:10px;letter-spacing:2px;background:transparent;")
        hl.addWidget(t)
        hl.addStretch()
        hl.addWidget(s)
        root.addWidget(hdr)

        # Tabs
        self.tabs = TabBar(["▶  Sign", "🔍  Verify", "📥  Install"])
        self.tabs.tab_changed.connect(self._on_tab)
        root.addWidget(self.tabs)

        # Pages
        self.stack = QStackedWidget()
        self.stack.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.stack.addWidget(self._page_sign())
        self.stack.addWidget(self._page_verify())
        self.stack.addWidget(self._page_install())
        root.addWidget(self.stack, stretch=1)

        # Log
        lp = GlassPanel()
        ll = QVBoxLayout(lp)
        ll.setContentsMargins(12, 8, 12, 12)
        ll.setSpacing(5)
        ll.addWidget(self._slbl("Output Log"))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(120)
        self.log.setPlaceholderText("// awaiting command...")
        ll.addWidget(self.log)
        root.addWidget(lp)

    def _on_tab(self, idx):
        self.stack.setCurrentIndex(idx)

    # ──────────────────────────────────────────────────────
    #  SIGN PAGE
    # ──────────────────────────────────────────────────────
    def _page_sign(self):
        pg = self._transparent_widget()
        vb = QVBoxLayout(pg); vb.setContentsMargins(0,0,0,0); vb.setSpacing(8)
        card = GlassPanel()
        cl = QVBoxLayout(card); cl.setContentsMargins(14,12,14,14); cl.setSpacing(8)

        cl.addWidget(self._slbl("Target File"))
        self.sign_file_edit = self._lineedit("path/to/application.exe", self.history_files)
        cl.addLayout(self._browse_row(self.sign_file_edit, self._choose_sign_file))

        cl.addWidget(self._slbl("Certificate (PFX / P12)"))
        self.cert_edit = self._lineedit("path/to/certificate.pfx", self.history_certs)
        cl.addLayout(self._browse_row(self.cert_edit, self._choose_cert))

        cl.addWidget(self._slbl("Password"))
        pr = QHBoxLayout(); pr.setSpacing(6)
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_edit.setPlaceholderText("••••••••")
        self.toggle_btn = QPushButton("Show")
        self.toggle_btn.setFixedWidth(72)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.toggled.connect(lambda c: (
            self.pass_edit.setEchoMode(QLineEdit.EchoMode.Normal if c else QLineEdit.EchoMode.Password),
            self.toggle_btn.setText("Hide" if c else "Show")
        ))
        pr.addWidget(self.pass_edit); pr.addWidget(self.toggle_btn)
        cl.addLayout(pr)
        vb.addWidget(card)

        self.btn_sign = self._action_btn("▶   SIGN  FILE", self.do_sign)
        vb.addWidget(self.btn_sign)
        vb.addStretch()
        return pg

    # ──────────────────────────────────────────────────────
    #  VERIFY PAGE
    # ──────────────────────────────────────────────────────
    def _page_verify(self):
        pg = self._transparent_widget()
        vb = QVBoxLayout(pg); vb.setContentsMargins(0,0,0,0); vb.setSpacing(8)
        card = GlassPanel()
        cl = QVBoxLayout(card); cl.setContentsMargins(14,12,14,14); cl.setSpacing(8)

        cl.addWidget(self._slbl("File to Verify"))
        self.verify_file_edit = self._lineedit("path/to/signed_file.exe", self.history_files)
        cl.addLayout(self._browse_row(self.verify_file_edit, self._choose_verify_file))

        cl.addWidget(self._slbl("Options"))
        opt_row = QHBoxLayout(); opt_row.setSpacing(6)
        self.btn_deep = self._toggle_opt("⚙  Deep Check", True)
        self.btn_ts   = self._toggle_opt("🕐  Require Timestamp", False)
        self.btn_deep.toggled.connect(lambda _: self._restyle_opt(self.btn_deep))
        self.btn_ts.toggled.connect(lambda _: self._restyle_opt(self.btn_ts))
        opt_row.addWidget(self.btn_deep); opt_row.addWidget(self.btn_ts); opt_row.addStretch()
        cl.addLayout(opt_row)
        vb.addWidget(card)

        self.btn_verify = self._action_btn("🔍   VERIFY  SIGNATURE", self.do_verify)
        vb.addWidget(self.btn_verify)
        vb.addStretch()
        return pg

    # ──────────────────────────────────────────────────────
    #  INSTALL PAGE
    # ──────────────────────────────────────────────────────
    def _page_install(self):
        pg = self._transparent_widget()
        vb = QVBoxLayout(pg); vb.setContentsMargins(0,0,0,0); vb.setSpacing(8)
        card = GlassPanel()
        cl = QVBoxLayout(card); cl.setContentsMargins(14,12,14,14); cl.setSpacing(8)

        cl.addWidget(self._slbl("Certificate File  (PFX / P12 / CER / CRT)"))
        self.inst_file_edit = self._lineedit("path/to/certificate.pfx", self.history_certs)
        cl.addLayout(self._browse_row(self.inst_file_edit, self._choose_inst_file))

        cl.addWidget(self._slbl("Password  (PFX only)"))
        ip = QHBoxLayout(); ip.setSpacing(6)
        self.inst_pass_edit = QLineEdit()
        self.inst_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.inst_pass_edit.setPlaceholderText("leave blank for CER / CRT")
        self.inst_toggle = QPushButton("Show")
        self.inst_toggle.setFixedWidth(72)
        self.inst_toggle.setCheckable(True)
        self.inst_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.inst_toggle.toggled.connect(lambda c: (
            self.inst_pass_edit.setEchoMode(QLineEdit.EchoMode.Normal if c else QLineEdit.EchoMode.Password),
            self.inst_toggle.setText("Hide" if c else "Show")
        ))
        ip.addWidget(self.inst_pass_edit); ip.addWidget(self.inst_toggle)
        cl.addLayout(ip)

        cl.addWidget(self._slbl("Target Store"))
        self.store_combo = QComboBox()
        self.store_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        for label, _ in CERT_STORES:
            self.store_combo.addItem(label)
        cl.addWidget(self.store_combo)

        # Info label
        info = QLabel("⚠  Installation may require Administrator privileges.")
        info.setStyleSheet("color:rgba(255,200,80,0.65);font-size:11px;background:transparent;")
        info.setWordWrap(True)
        cl.addWidget(info)

        vb.addWidget(card)
        self.btn_install = self._action_btn("📥   INSTALL  CERTIFICATE", self.do_install)
        vb.addWidget(self.btn_install)
        vb.addStretch()
        return pg

    # ──────────────────────────────────────────────────────
    #  ACTIONS
    # ──────────────────────────────────────────────────────
    def do_sign(self):
        fp = self.sign_file_edit.text().strip()
        cp = self.cert_edit.text().strip()
        pw = self.pass_edit.text().strip()
        if not fp: return self.log_line("  ⚠  No target file.")
        if not cp: return self.log_line("  ⚠  No certificate.")
        self.add_hist("history_files", self.history_files, fp)
        self.add_hist("history_certs", self.history_certs, cp)
        if pw: self.add_hist("history_passwords", self.history_passwords, pw)
        cmd = ["signtool.exe","sign","/f",cp,"/p",pw,"/fd","sha256",
               "/tr","http://timestamp.digicert.com","/td","sha256",fp]
        self.log_line(f"\n  ╔═  SIGN\n  »  {' '.join(cmd)}\n")
        self._run(cmd, self.btn_sign, "▶   SIGN  FILE",
                  lambda c,o,e: (self._out(o,e), self.log_line("\n  ✔  Done.\n" if c==0 else f"\n  ✖  Exit {c}\n")))

    def do_verify(self):
        fp = self.verify_file_edit.text().strip()
        if not fp: return self.log_line("  ⚠  No file to verify.")
        self.add_hist("history_files", self.history_files, fp)
        cmd = ["signtool.exe","verify","/pa"]
        if self.btn_deep.isChecked(): cmd.append("/all")
        if self.btn_ts.isChecked():   cmd.append("/tw")
        cmd.append(fp)
        cmd_v = ["signtool.exe","verify","/pa","/v",fp]
        self.log_line(f"\n  ╔═  VERIFY\n  »  {' '.join(cmd)}\n")
        def _after(code,out,err):
            self._out(out,err)
            if code == 0:
                self.log_line("\n  ✔  Signature VALID.\n")
                self.log_line("  ─── Details ───\n")
                self._run(cmd_v, self.btn_verify, "🔍   VERIFY  SIGNATURE",
                          lambda c,o,e: [self.log_line(l) for l in self._parse_cert(o)],
                          restore=True)
            else:
                self.log_line(f"\n  ✖  INVALID  (exit {code})\n")
                self.btn_verify.setEnabled(True)
                self.btn_verify.setText("🔍   VERIFY  SIGNATURE")
        self._run(cmd, self.btn_verify, "🔍   VERIFY  SIGNATURE", _after, restore=False)

    def do_install(self):
        fp   = self.inst_file_edit.text().strip()
        pw   = self.inst_pass_edit.text().strip()
        store_label = self.store_combo.currentText()
        store = next(s for l,s in CERT_STORES if l == store_label)

        if not fp: return self.log_line("  ⚠  No certificate file specified.")

        self.add_hist("history_certs", self.history_certs, fp)
        self.log_line(f"\n  ╔═  INSTALL\n  »  certutil  →  store: {store}\n  »  file: {fp}\n")

        self.btn_install.setEnabled(False)
        self.btn_install.setText("  ⟳  Installing...")

        def _run_install():
            code, out, err = install_cert_certutil(fp, store, pw)
            self._out(out, err)
            if code == 0:
                self.log_line(f"\n  ✔  Certificate installed to '{store}' store successfully.\n")
            else:
                self.log_line(f"\n  ✖  Installation failed  (exit {code})\n")
                if "access" in (out+err).lower() or code == 5:
                    self.log_line("  ⚠  Try running the application as Administrator.\n")
            self.btn_install.setEnabled(True)
            self.btn_install.setText("📥   INSTALL  CERTIFICATE")

        w = Worker.__new__(Worker)
        QThread.__init__(w)
        w.cmd = None
        w._fn = _run_install

        class InstWorker(QThread):
            done = pyqtSignal()
            def __init__(self, fn): super().__init__(); self._fn = fn
            def run(self): self._fn()

        worker = InstWorker(_run_install)
        self._workers.append(worker)
        worker.start()

    # ──────────────────────────────────────────────────────
    #  HELPERS — UI
    # ──────────────────────────────────────────────────────
    def _slbl(self, text):
        l = QLabel(text.upper())
        l.setStyleSheet("color:rgba(120,190,255,0.7);font-size:10px;font-weight:bold;letter-spacing:2px;background:transparent;")
        return l

    def _lineedit(self, ph, hist):
        e = QLineEdit()
        e.setPlaceholderText(ph)
        e.setCompleter(QCompleter(hist))
        return e

    def _browse_row(self, edit, cb):
        row = QHBoxLayout(); row.setSpacing(6)
        btn = QPushButton("Browse")
        btn.setFixedWidth(72)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(cb)
        row.addWidget(edit); row.addWidget(btn)
        return row

    def _action_btn(self, label, cb):
        b = QPushButton(label)
        b.setObjectName("ActionButton")
        b.setMinimumHeight(42)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(cb)
        return b

    def _toggle_opt(self, label, checked):
        b = QPushButton(label)
        b.setCheckable(True)
        b.setChecked(checked)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        self._restyle_opt(b)
        return b

    def _restyle_opt(self, btn):
        if btn.isChecked():
            btn.setStyleSheet("QPushButton{background:rgba(40,120,220,0.35);border:1px solid rgba(120,200,255,0.6);border-radius:6px;color:#cce8ff;font-weight:bold;padding:6px 14px;}")
        else:
            btn.setStyleSheet("QPushButton{background:rgba(255,255,255,0.05);border:1px solid rgba(100,160,255,0.18);border-radius:6px;color:rgba(160,200,255,0.5);padding:6px 14px;}"
                              "QPushButton:hover{background:rgba(80,140,220,0.15);color:#a0ccff;}")

    def _transparent_widget(self):
        w = QWidget()
        w.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        return w

    # ──────────────────────────────────────────────────────
    #  FILE CHOOSERS
    # ──────────────────────────────────────────────────────
    def _choose_sign_file(self):
        p,_ = QFileDialog.getOpenFileName(self,"Select File to Sign","","All Files (*.*)")
        if p: self.sign_file_edit.setText(p); self.add_hist("history_files",self.history_files,p)

    def _choose_cert(self):
        p,_ = QFileDialog.getOpenFileName(self,"Select Certificate","","Certificates (*.pfx *.p12)")
        if p: self.cert_edit.setText(p); self.add_hist("history_certs",self.history_certs,p)

    def _choose_verify_file(self):
        p,_ = QFileDialog.getOpenFileName(self,"Select File to Verify","","All Files (*.*)")
        if p: self.verify_file_edit.setText(p); self.add_hist("history_files",self.history_files,p)

    def _choose_inst_file(self):
        p,_ = QFileDialog.getOpenFileName(self,"Select Certificate","","Certificates (*.pfx *.p12 *.cer *.crt)")
        if p: self.inst_file_edit.setText(p); self.add_hist("history_certs",self.history_certs,p)

    # ──────────────────────────────────────────────────────
    #  CMD RUNNER
    # ──────────────────────────────────────────────────────
    def _run(self, cmd, btn, label, cb, restore=True):
        btn.setEnabled(False); btn.setText("  ⟳  Running...")
        def _done(c,o,e):
            cb(c,o,e)
            if restore: btn.setEnabled(True); btn.setText(label)
        w = Worker(cmd)
        self._workers.append(w)
        w.result_ready.connect(_done)
        w.start()

    # ──────────────────────────────────────────────────────
    #  OUTPUT
    # ──────────────────────────────────────────────────────
    def _out(self, out, err):
        if out and out.strip(): self.log_line("── stdout ──\n"+out.strip())
        if err and err.strip(): self.log_line("── stderr ──\n"+err.strip())

    def log_line(self, text):
        self.log.append(text)

    def _parse_cert(self, raw):
        fields = {"Issued to":None,"Issued by":None,"Expires":None,
                  "SHA1 hash":None,"Signing time":None}
        for line in raw.splitlines():
            s = line.strip()
            for k in fields:
                if s.lower().startswith(k.lower()):
                    v = s[len(k):].lstrip(": ").strip()
                    if v: fields[k] = v
        pad = max(len(k) for k in fields)+2
        result = []
        for k,v in fields.items():
            if v: result.append(f"  {k+':':<{pad}} {v}")
        return result or ["  (no details found)"]

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
