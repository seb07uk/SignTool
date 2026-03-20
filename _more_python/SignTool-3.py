import sys
import subprocess
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel,
    QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QCompleter,
    QFrame, QStackedWidget, QSizePolicy
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
    font-size: 13px;
    color: #e8f0ff;
}
QLineEdit {
    background-color: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(120, 180, 255, 0.25);
    border-radius: 8px;
    padding: 9px 14px;
    color: #ddeeff;
    font-size: 13px;
    selection-background-color: rgba(80, 160, 255, 0.5);
}
QLineEdit:focus {
    border: 1px solid rgba(100, 180, 255, 0.7);
    background-color: rgba(255, 255, 255, 0.11);
}
QLineEdit:hover {
    border: 1px solid rgba(120, 180, 255, 0.45);
    background-color: rgba(255, 255, 255, 0.09);
}
QPushButton {
    background-color: rgba(80, 140, 220, 0.18);
    border: 1px solid rgba(120, 180, 255, 0.35);
    border-radius: 8px;
    padding: 9px 18px;
    color: #a8d4ff;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 0.5px;
}
QPushButton:hover {
    background-color: rgba(100, 170, 255, 0.28);
    border: 1px solid rgba(150, 210, 255, 0.6);
    color: #cce8ff;
}
QPushButton:pressed {
    background-color: rgba(60, 120, 200, 0.35);
    border: 1px solid rgba(100, 180, 255, 0.5);
    color: #88bbff;
}
#ActionButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(60,140,255,0.45), stop:0.45 rgba(40,110,230,0.35),
        stop:0.5 rgba(20,80,200,0.25), stop:1 rgba(10,60,180,0.35));
    border: 1px solid rgba(120, 200, 255, 0.6);
    border-radius: 10px;
    color: #b8e0ff;
    font-size: 15px;
    font-weight: bold;
    letter-spacing: 3px;
    padding: 13px 28px;
}
#ActionButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(80,160,255,0.55), stop:0.45 rgba(60,130,245,0.45),
        stop:0.5 rgba(40,100,210,0.35), stop:1 rgba(20,80,195,0.45));
    border: 1px solid rgba(160, 220, 255, 0.8);
    color: #ddf0ff;
}
#ActionButton:pressed {
    background: rgba(30, 90, 200, 0.4);
    border: 1px solid rgba(100, 180, 255, 0.5);
    color: #88c4ff;
}
#ActionButton:disabled {
    background: rgba(30, 60, 120, 0.2);
    border: 1px solid rgba(80, 120, 200, 0.2);
    color: rgba(150, 200, 255, 0.3);
}
QTextEdit {
    background-color: rgba(0, 10, 30, 0.55);
    border: 1px solid rgba(80, 140, 220, 0.25);
    border-radius: 8px;
    color: #7ac4ff;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    padding: 10px;
    selection-background-color: rgba(80, 160, 255, 0.4);
}
QScrollBar:vertical {
    background: transparent; width: 6px; border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: rgba(100, 160, 255, 0.3); border-radius: 3px; min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: rgba(130, 190, 255, 0.55); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
QAbstractItemView {
    background-color: rgba(10, 25, 60, 0.92);
    border: 1px solid rgba(100, 160, 255, 0.3);
    color: #c0dcff;
    selection-background-color: rgba(60, 130, 230, 0.5);
    font-size: 12px;
}
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
        path.addRoundedRect(0, 0, r.width(), r.height(), 12, 12)

        fill = QColor(30, 80, 180, 28) if self.accent else QColor(200, 220, 255, 14)
        p.fillPath(path, fill)

        gloss = QPainterPath()
        gloss.addRoundedRect(1, 1, r.width() - 2, r.height() // 2, 11, 11)
        gg = QLinearGradient(0, 0, 0, r.height() // 2)
        gg.setColorAt(0, QColor(255, 255, 255, 22))
        gg.setColorAt(1, QColor(255, 255, 255, 0))
        p.fillPath(gloss, QBrush(gg))

        bg = QLinearGradient(0, 0, 0, r.height())
        bg.setColorAt(0, QColor(160, 210, 255, 80))
        bg.setColorAt(0.5, QColor(100, 170, 255, 45))
        bg.setColorAt(1, QColor(80, 140, 220, 30))
        p.setPen(QPen(QBrush(bg), 1))
        p.drawPath(path)
        p.end()


# ══════════════════════════════════════════════════════════
#  TAB BAR
# ══════════════════════════════════════════════════════════
class TabBar(QWidget):
    tab_changed = pyqtSignal(int)

    def __init__(self, tabs, parent=None):
        super().__init__(parent)
        self._tabs = tabs
        self._current = 0
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(44)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._buttons = []
        for i, label in enumerate(tabs):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setChecked(i == 0)
            idx = i
            btn.clicked.connect(lambda _, x=idx: self._select(x))
            self._buttons.append(btn)
            layout.addWidget(btn)
        layout.addStretch()
        self._style_buttons()

    def _select(self, idx):
        self._current = idx
        self._style_buttons()
        self.tab_changed.emit(idx)

    def _style_buttons(self):
        for i, btn in enumerate(self._buttons):
            if i == self._current:
                btn.setStyleSheet(
                    "QPushButton { background: rgba(60,140,255,0.35); border: 1px solid rgba(120,200,255,0.6);"
                    " border-radius: 8px; color: #cce8ff; font-weight: bold; padding: 8px 22px; font-size: 13px; letter-spacing: 1px; }"
                )
                btn.setChecked(True)
            else:
                btn.setStyleSheet(
                    "QPushButton { background: rgba(255,255,255,0.05); border: 1px solid rgba(100,160,255,0.2);"
                    " border-radius: 8px; color: rgba(160,200,255,0.55); font-weight: normal; padding: 8px 22px;"
                    " font-size: 13px; letter-spacing: 1px; }"
                    "QPushButton:hover { background: rgba(80,140,220,0.15); border-color: rgba(120,180,255,0.4); color: #a0ccff; }"
                )
                btn.setChecked(False)


# ══════════════════════════════════════════════════════════
#  WORKER THREAD
# ══════════════════════════════════════════════════════════
class Worker(QThread):
    result_ready = pyqtSignal(int, str, str)   # returncode, stdout, stderr

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
        self._offset = 0
        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(40)

    def _tick(self):
        self._offset = (self._offset + 1) % 360
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, QColor(4, 12, 35))

        def orb(cx, cy, radius, r, g, b, alpha):
            grad = QRadialGradient(cx, cy, radius)
            grad.setColorAt(0, QColor(r, g, b, alpha))
            grad.setColorAt(1, QColor(r // 3, g // 3, b // 3, 0))
            p.setBrush(QBrush(grad))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx - radius), int(cy - radius), radius * 2, radius * 2)

        off = self._offset
        orb(w * 0.3 + math.sin(math.radians(off * 0.7)) * 60,
            h * 0.25 + math.cos(math.radians(off * 0.5)) * 30, 280, 30, 80, 200, 60)
        orb(w * 0.75 + math.cos(math.radians(off * 0.6)) * 50,
            h * 0.65 + math.sin(math.radians(off * 0.8)) * 40, 220, 0, 140, 220, 50)
        orb(w * 0.15 + math.sin(math.radians(off * 0.4 + 90)) * 40,
            h * 0.82, 180, 80, 40, 180, 40)

        pen = QPen(QColor(60, 120, 220, 8))
        pen.setWidth(1)
        p.setPen(pen)
        for x in range(0, w, 40):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, 40):
            p.drawLine(0, y, w, y)

        vgn = QLinearGradient(0, h * 0.6, 0, h)
        vgn.setColorAt(0, QColor(0, 0, 0, 0))
        vgn.setColorAt(1, QColor(0, 5, 20, 100))
        p.setBrush(QBrush(vgn))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(0, int(h * 0.6), w, h)
        p.end()


# ══════════════════════════════════════════════════════════
#  MAIN WINDOW
# ══════════════════════════════════════════════════════════
class SignToolGUI(AeroBackground):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SignTool  ·  Code Signing & Verification")
        self.setMinimumSize(740, 640)

        self.settings = QSettings("polsoftITS", "SignToolGUI")
        self.history_files  = self.settings.value("history_files", [])
        self.history_certs  = self.settings.value("history_certs", [])
        self.history_passwords = self.settings.value("history_passwords", [])

        self.setStyleSheet(STYLE)
        self._worker = None
        self.init_ui()

    # ──────────────────────────────────────────────────────
    #  LAYOUT
    # ──────────────────────────────────────────────────────
    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 24)
        root.setSpacing(13)

        # Header
        hdr = GlassPanel(accent=True)
        hl = QVBoxLayout(hdr)
        hl.setContentsMargins(20, 13, 20, 13)
        hl.setSpacing(3)
        t = QLabel("✦  SignTool  GUI")
        t.setStyleSheet("color:#a8d8ff;font-size:20px;font-weight:bold;letter-spacing:2px;background:transparent;")
        s = QLabel("Code Signing & Verification  ·  SHA-256  ·  DigiCert Timestamp  ·  PFX / P12")
        s.setStyleSheet("color:rgba(140,190,255,0.55);font-size:10px;letter-spacing:2px;background:transparent;")
        hl.addWidget(t)
        hl.addWidget(s)
        root.addWidget(hdr)

        # Tab bar
        self.tabs = TabBar(["▶  Sign", "🔍  Verify"])
        self.tabs.tab_changed.connect(self._on_tab)
        root.addWidget(self.tabs)

        # Stacked pages
        self.stack = QStackedWidget()
        self.stack.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.stack.addWidget(self._build_sign_page())
        self.stack.addWidget(self._build_verify_page())
        root.addWidget(self.stack, stretch=1)

        # Log
        log_panel = GlassPanel()
        ll = QVBoxLayout(log_panel)
        ll.setContentsMargins(14, 10, 14, 14)
        ll.setSpacing(6)
        ll.addWidget(self._slabel("Output Log"))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(160)
        self.log.setPlaceholderText("// awaiting command...")
        ll.addWidget(self.log)
        root.addWidget(log_panel)

    def _on_tab(self, idx):
        self.stack.setCurrentIndex(idx)

    # ──────────────────────────────────────────────────────
    #  SIGN PAGE
    # ──────────────────────────────────────────────────────
    def _build_sign_page(self):
        page = QWidget()
        page.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        vbox = QVBoxLayout(page)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(10)

        card = GlassPanel()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(18, 15, 18, 18)
        cl.setSpacing(10)

        cl.addWidget(self._slabel("Target File"))
        self.sign_file_edit = QLineEdit()
        self.sign_file_edit.setPlaceholderText("path/to/application.exe")
        self.sign_file_edit.setCompleter(QCompleter(self.history_files))
        cl.addLayout(self._browse_row(self.sign_file_edit, self._choose_sign_file))

        cl.addWidget(self._slabel("Certificate  (PFX / P12)"))
        self.cert_edit = QLineEdit()
        self.cert_edit.setPlaceholderText("path/to/certificate.pfx")
        self.cert_edit.setCompleter(QCompleter(self.history_certs))
        cl.addLayout(self._browse_row(self.cert_edit, self._choose_cert))

        cl.addWidget(self._slabel("Password"))
        pass_row = QHBoxLayout()
        pass_row.setSpacing(8)
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_edit.setPlaceholderText("••••••••")
        self.pass_edit.setCompleter(QCompleter(self.history_passwords))
        self.toggle_btn = QPushButton("Show")
        self.toggle_btn.setFixedWidth(95)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.toggled.connect(self._toggle_pass)
        pass_row.addWidget(self.pass_edit)
        pass_row.addWidget(self.toggle_btn)
        cl.addLayout(pass_row)

        vbox.addWidget(card)

        self.btn_sign = QPushButton("▶   SIGN  FILE")
        self.btn_sign.setObjectName("ActionButton")
        self.btn_sign.setMinimumHeight(50)
        self.btn_sign.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_sign.clicked.connect(self.do_sign)
        vbox.addWidget(self.btn_sign)
        vbox.addStretch()
        return page

    # ──────────────────────────────────────────────────────
    #  VERIFY PAGE
    # ──────────────────────────────────────────────────────
    def _build_verify_page(self):
        page = QWidget()
        page.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        vbox = QVBoxLayout(page)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(10)

        card = GlassPanel()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(18, 15, 18, 18)
        cl.setSpacing(10)

        cl.addWidget(self._slabel("File to Verify"))
        self.verify_file_edit = QLineEdit()
        self.verify_file_edit.setPlaceholderText("path/to/signed_file.exe")
        self.verify_file_edit.setCompleter(QCompleter(self.history_files))
        cl.addLayout(self._browse_row(self.verify_file_edit, self._choose_verify_file))

        # Options row
        cl.addWidget(self._slabel("Options"))
        opt_row = QHBoxLayout()
        opt_row.setSpacing(8)

        self.btn_deep = QPushButton("⚙  Deep Check")
        self.btn_deep.setCheckable(True)
        self.btn_deep.setChecked(True)
        self.btn_deep.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_deep.setToolTip("Weryfikuje całą kaskadę certyfikatów aż do root CA")
        self.btn_deep.toggled.connect(self._style_opt_btns)

        self.btn_timestamp = QPushButton("🕐  Require Timestamp")
        self.btn_timestamp.setCheckable(True)
        self.btn_timestamp.setChecked(False)
        self.btn_timestamp.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_timestamp.setToolTip("Wymaga, aby plik był opatrzony znacznikiem czasu")
        self.btn_timestamp.toggled.connect(self._style_opt_btns)

        opt_row.addWidget(self.btn_deep)
        opt_row.addWidget(self.btn_timestamp)
        opt_row.addStretch()
        cl.addLayout(opt_row)
        self._style_opt_btns()

        vbox.addWidget(card)

        self.btn_verify = QPushButton("🔍   VERIFY  SIGNATURE")
        self.btn_verify.setObjectName("ActionButton")
        self.btn_verify.setMinimumHeight(50)
        self.btn_verify.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_verify.clicked.connect(self.do_verify)
        vbox.addWidget(self.btn_verify)
        vbox.addStretch()
        return page

    # ──────────────────────────────────────────────────────
    #  HELPERS — UI
    # ──────────────────────────────────────────────────────
    def _slabel(self, text):
        lbl = QLabel(text.upper())
        lbl.setStyleSheet(
            "color:rgba(120,190,255,0.75);font-size:10px;font-weight:bold;"
            "letter-spacing:2px;background:transparent;"
        )
        return lbl

    def _browse_row(self, edit, callback):
        row = QHBoxLayout()
        row.setSpacing(8)
        btn = QPushButton("Browse")
        btn.setFixedWidth(95)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(callback)
        row.addWidget(edit)
        row.addWidget(btn)
        return row

    def _style_opt_btns(self):
        for btn in (self.btn_deep, self.btn_timestamp):
            if btn.isChecked():
                btn.setStyleSheet(
                    "QPushButton{background:rgba(40,120,220,0.35);border:1px solid rgba(120,200,255,0.6);"
                    "border-radius:8px;color:#cce8ff;font-weight:bold;padding:8px 16px;}"
                )
            else:
                btn.setStyleSheet(
                    "QPushButton{background:rgba(255,255,255,0.05);border:1px solid rgba(100,160,255,0.2);"
                    "border-radius:8px;color:rgba(160,200,255,0.5);padding:8px 16px;}"
                    "QPushButton:hover{background:rgba(80,140,220,0.15);border-color:rgba(120,180,255,0.4);color:#a0ccff;}"
                )

    # ──────────────────────────────────────────────────────
    #  FILE CHOOSERS
    # ──────────────────────────────────────────────────────
    def _choose_sign_file(self):
        p, _ = QFileDialog.getOpenFileName(self, "Select File to Sign", "", "All Files (*.*)")
        if p:
            self.sign_file_edit.setText(p)
            self.add_to_history("history_files", self.history_files, p)

    def _choose_cert(self):
        p, _ = QFileDialog.getOpenFileName(self, "Select Certificate", "", "Certificates (*.pfx *.p12)")
        if p:
            self.cert_edit.setText(p)
            self.add_to_history("history_certs", self.history_certs, p)

    def _choose_verify_file(self):
        p, _ = QFileDialog.getOpenFileName(self, "Select File to Verify", "", "All Files (*.*)")
        if p:
            self.verify_file_edit.setText(p)
            self.add_to_history("history_files", self.history_files, p)

    def _toggle_pass(self, checked):
        self.pass_edit.setEchoMode(
            QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        )
        self.toggle_btn.setText("Hide" if checked else "Show")

    # ──────────────────────────────────────────────────────
    #  SIGN
    # ──────────────────────────────────────────────────────
    def do_sign(self):
        fp = self.sign_file_edit.text().strip()
        cp = self.cert_edit.text().strip()
        pw = self.pass_edit.text().strip()

        if not fp:
            self.log_line("  ⚠  No target file specified.")
            return
        if not cp:
            self.log_line("  ⚠  No certificate specified.")
            return

        self.add_to_history("history_files", self.history_files, fp)
        self.add_to_history("history_certs", self.history_certs, cp)
        if pw:
            self.add_to_history("history_passwords", self.history_passwords, pw)

        cmd = [
            "signtool.exe", "sign",
            "/f", cp, "/p", pw,
            "/fd", "sha256",
            "/tr", "http://timestamp.digicert.com",
            "/td", "sha256",
            fp
        ]
        self.log_line(f"\n  ╔═  SIGN  ═══════════════════════════════")
        self.log_line(f"  »  {' '.join(cmd)}\n")
        self._run_cmd(cmd, self.btn_sign, "▶   SIGN  FILE", self._on_sign_done)

    def _on_sign_done(self, code, out, err):
        self._print_output(out, err)
        if code == 0:
            self.log_line("\n  ✔  Signing successful.\n")
        else:
            self.log_line(f"\n  ✖  Signing failed  (exit {code})\n")

    # ──────────────────────────────────────────────────────
    #  VERIFY
    # ──────────────────────────────────────────────────────
    def do_verify(self):
        fp = self.verify_file_edit.text().strip()
        if not fp:
            self.log_line("  ⚠  No file specified for verification.")
            return

        self.add_to_history("history_files", self.history_files, fp)

        # signtool verify
        cmd_verify = ["signtool.exe", "verify", "/pa"]
        if self.btn_deep.isChecked():
            cmd_verify.append("/all")
        if self.btn_timestamp.isChecked():
            cmd_verify.append("/tw")
        cmd_verify.append(fp)

        # signtool dump — szczegółowe info o certyfikacie
        cmd_dump = ["signtool.exe", "verify", "/pa", "/v", fp]

        self.log_line(f"\n  ╔═  VERIFY  ═══════════════════════════════")
        self.log_line(f"  »  {' '.join(cmd_verify)}\n")

        self._run_cmd(cmd_verify, self.btn_verify, "🔍   VERIFY  SIGNATURE",
                      lambda code, out, err: self._on_verify_done(code, out, err, cmd_dump, fp))

    def _on_verify_done(self, code, out, err, cmd_dump, fp):
        self._print_output(out, err)

        if code == 0:
            self.log_line("\n  ✔  Signature is VALID.\n")
        else:
            self.log_line(f"\n  ✖  Signature INVALID or not found  (exit {code})\n")
            self.btn_verify.setEnabled(True)
            self.btn_verify.setText("🔍   VERIFY  SIGNATURE")
            return

        # Jeśli podpis ważny — pobierz szczegóły
        self.log_line("  ─── Certificate Details ───────────────────\n")
        self._run_cmd(cmd_dump, self.btn_verify, "🔍   VERIFY  SIGNATURE",
                      self._on_dump_done, restore=True)

    def _on_dump_done(self, code, out, err):
        if out:
            details = self._parse_cert_details(out)
            for line in details:
                self.log_line(line)
        self.log_line("")

    def _parse_cert_details(self, raw: str) -> list[str]:
        """Wyciąga i formatuje kluczowe pola z signtool /v output."""
        lines = []
        fields = {
            "Issued to":      None,
            "Issued by":      None,
            "Expires":        None,
            "SHA1 hash":      None,
            "Signing time":   None,
            "Hash of file":   None,
            "Number of signatures": None,
        }

        for line in raw.splitlines():
            s = line.strip()
            for key in fields:
                if s.lower().startswith(key.lower()):
                    value = s[len(key):].lstrip(": ").strip()
                    if value:
                        fields[key] = value

        # Fallback — wypisz przefiltrowane linie
        useful = [l.strip() for l in raw.splitlines()
                  if any(k in l for k in ("Issued", "Expires", "SHA1", "Signing time",
                                           "Timestamp", "hash", "Subject", "Signer", "Number"))]

        if any(v for v in fields.values()):
            pad = max(len(k) for k in fields) + 2
            for k, v in fields.items():
                if v:
                    lines.append(f"  {'  ' + k + ':' :<{pad+2}} {v}")
        elif useful:
            lines = [f"  {l}" for l in useful[:20]]
        else:
            lines = ["  (no parseable detail found — see raw output above)"]

        return lines

    # ──────────────────────────────────────────────────────
    #  GENERIC RUNNER
    # ──────────────────────────────────────────────────────
    def _run_cmd(self, cmd, btn, restore_label, callback, restore=True):
        btn.setEnabled(False)
        btn.setText("  ⟳  Running...")

        def _done(code, out, err):
            callback(code, out, err)
            if restore:
                btn.setEnabled(True)
                btn.setText(restore_label)

        self._worker = Worker(cmd)
        self._worker.result_ready.connect(_done)
        self._worker.start()

    # ──────────────────────────────────────────────────────
    #  OUTPUT HELPERS
    # ──────────────────────────────────────────────────────
    def _print_output(self, out, err):
        if out and out.strip():
            self.log_line("── stdout ──")
            self.log_line(out.strip())
        if err and err.strip():
            self.log_line("── stderr ──")
            self.log_line(err.strip())

    def log_line(self, text):
        self.log.append(text)

    # ──────────────────────────────────────────────────────
    #  HISTORY
    # ──────────────────────────────────────────────────────
    def add_to_history(self, key, lst, value):
        if value not in lst:
            lst.insert(0, value)
            lst[:] = lst[:10]
            self.settings.setValue(key, lst)


# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = SignToolGUI()
    w.show()
    sys.exit(app.exec())
