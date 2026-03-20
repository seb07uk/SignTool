import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel,
    QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QCompleter,
    QFrame, QGraphicsBlurEffect
)
from PyQt6.QtCore import Qt, QSettings, QPoint, QRect, QTimer
from PyQt6.QtGui import (
    QColor, QFont, QPainter, QPainterPath, QBrush, QPen,
    QLinearGradient, QRadialGradient, QRegion, QPixmap
)


STYLE = """
QWidget {
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13px;
    color: #e8f0ff;
}

/* ── Input fields ── */
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

/* ── Standard buttons ── */
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

/* ── Sign button ── */
#SignButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(60,140,255,0.45),
        stop:0.45 rgba(40,110,230,0.35),
        stop:0.5 rgba(20,80,200,0.25),
        stop:1 rgba(10,60,180,0.35));
    border: 1px solid rgba(120, 200, 255, 0.6);
    border-radius: 10px;
    color: #b8e0ff;
    font-size: 15px;
    font-weight: bold;
    letter-spacing: 3px;
    padding: 13px 28px;
}
#SignButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(80,160,255,0.55),
        stop:0.45 rgba(60,130,245,0.45),
        stop:0.5 rgba(40,100,210,0.35),
        stop:1 rgba(20,80,195,0.45));
    border: 1px solid rgba(160, 220, 255, 0.8);
    color: #ddf0ff;
}
#SignButton:pressed {
    background: rgba(30, 90, 200, 0.4);
    border: 1px solid rgba(100, 180, 255, 0.5);
    color: #88c4ff;
}
#SignButton:disabled {
    background: rgba(30, 60, 120, 0.2);
    border: 1px solid rgba(80, 120, 200, 0.2);
    color: rgba(150, 200, 255, 0.3);
}

/* ── Log ── */
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

/* ── Scrollbar ── */
QScrollBar:vertical {
    background: transparent;
    width: 6px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: rgba(100, 160, 255, 0.3);
    border-radius: 3px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(130, 190, 255, 0.55);
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }

/* ── Completer popup ── */
QAbstractItemView {
    background-color: rgba(10, 25, 60, 0.92);
    border: 1px solid rgba(100, 160, 255, 0.3);
    color: #c0dcff;
    selection-background-color: rgba(60, 130, 230, 0.5);
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
}
"""


class GlassPanel(QFrame):
    """Przezroczysty panel z efektem szkła."""
    def __init__(self, parent=None, accent=False):
        super().__init__(parent)
        self.accent = accent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(0, 0, rect.width(), rect.height(), 12, 12)

        # Tło szkła
        if self.accent:
            fill = QColor(30, 80, 180, 28)
        else:
            fill = QColor(200, 220, 255, 14)
        painter.fillPath(path, fill)

        # Górny połysk (reflekcja)
        gloss = QPainterPath()
        gloss.addRoundedRect(1, 1, rect.width() - 2, rect.height() // 2, 11, 11)
        gloss_gradient = QLinearGradient(0, 0, 0, rect.height() // 2)
        gloss_gradient.setColorAt(0, QColor(255, 255, 255, 22))
        gloss_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        painter.fillPath(gloss, QBrush(gloss_gradient))

        # Obramowanie
        border_gradient = QLinearGradient(0, 0, 0, rect.height())
        border_gradient.setColorAt(0, QColor(160, 210, 255, 80))
        border_gradient.setColorAt(0.5, QColor(100, 170, 255, 45))
        border_gradient.setColorAt(1, QColor(80, 140, 220, 30))
        pen = QPen(QBrush(border_gradient), 1)
        painter.setPen(pen)
        painter.drawPath(path)

        painter.end()


class AeroBackground(QWidget):
    """Główne okno z tłem Aero."""
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._offset = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(40)

    def _animate(self):
        self._offset = (self._offset + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # Tło bazowe — głęboki granat
        painter.fillRect(0, 0, w, h, QColor(4, 12, 35))

        # Orb 1 — niebieski (animowany)
        import math
        ox = w * 0.3 + math.sin(math.radians(self._offset * 0.7)) * 60
        oy = h * 0.25 + math.cos(math.radians(self._offset * 0.5)) * 30
        r1 = QRadialGradient(ox, oy, 280)
        r1.setColorAt(0, QColor(30, 80, 200, 60))
        r1.setColorAt(1, QColor(10, 30, 100, 0))
        painter.setBrush(QBrush(r1))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(ox - 280), int(oy - 280), 560, 560)

        # Orb 2 — cyjan
        ox2 = w * 0.75 + math.cos(math.radians(self._offset * 0.6)) * 50
        oy2 = h * 0.65 + math.sin(math.radians(self._offset * 0.8)) * 40
        r2 = QRadialGradient(ox2, oy2, 220)
        r2.setColorAt(0, QColor(0, 140, 220, 50))
        r2.setColorAt(1, QColor(0, 60, 140, 0))
        painter.setBrush(QBrush(r2))
        painter.drawEllipse(int(ox2 - 220), int(oy2 - 220), 440, 440)

        # Orb 3 — purpura
        ox3 = w * 0.15 + math.sin(math.radians(self._offset * 0.4 + 90)) * 40
        oy3 = h * 0.8
        r3 = QRadialGradient(ox3, oy3, 180)
        r3.setColorAt(0, QColor(80, 40, 180, 40))
        r3.setColorAt(1, QColor(40, 20, 100, 0))
        painter.setBrush(QBrush(r3))
        painter.drawEllipse(int(ox3 - 180), int(oy3 - 180), 360, 360)

        # Siatka linii (subtelna)
        pen = QPen(QColor(60, 120, 220, 8))
        pen.setWidth(1)
        painter.setPen(pen)
        for x in range(0, w, 40):
            painter.drawLine(x, 0, x, h)
        for y in range(0, h, 40):
            painter.drawLine(0, y, w, y)

        # Dolny gradient — winietowanie
        vign = QLinearGradient(0, h * 0.6, 0, h)
        vign.setColorAt(0, QColor(0, 0, 0, 0))
        vign.setColorAt(1, QColor(0, 5, 20, 100))
        painter.setBrush(QBrush(vign))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, int(h * 0.6), w, h)

        painter.end()


class SignToolGUI(AeroBackground):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SignTool  ·  Code Signing")
        self.setMinimumSize(720, 560)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)

        self.settings = QSettings("polsoftITS", "SignToolGUI")
        self.history_files = self.settings.value("history_files", [])
        self.history_certs = self.settings.value("history_certs", [])
        self.history_passwords = self.settings.value("history_passwords", [])

        self.setStyleSheet(STYLE)
        self.init_ui()

    # ── UI ────────────────────────────────────────────────────

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 24)
        root.setSpacing(14)

        # ── Header ──
        header_panel = GlassPanel(accent=True)
        h_layout = QVBoxLayout(header_panel)
        h_layout.setContentsMargins(20, 14, 20, 14)
        h_layout.setSpacing(3)

        title = QLabel("✦  SignTool  GUI")
        title.setStyleSheet("color: #a8d8ff; font-size: 20px; font-weight: bold; letter-spacing: 2px; background: transparent;")
        sub = QLabel("Code Signing  ·  SHA-256  ·  DigiCert Timestamp  ·  PFX / P12")
        sub.setStyleSheet("color: rgba(140, 190, 255, 0.55); font-size: 10px; letter-spacing: 2px; background: transparent;")

        h_layout.addWidget(title)
        h_layout.addWidget(sub)
        root.addWidget(header_panel)

        # ── Input card ──
        card = GlassPanel()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 16, 18, 18)
        card_layout.setSpacing(11)

        card_layout.addWidget(self._section_label("Target File"))
        card_layout.addLayout(self._file_row())

        card_layout.addWidget(self._section_label("Certificate  (PFX / P12)"))
        card_layout.addLayout(self._cert_row())

        card_layout.addWidget(self._section_label("Password"))
        card_layout.addLayout(self._pass_row())

        root.addWidget(card)

        # ── Sign button ──
        self.btn_sign = QPushButton("▶   SIGN  FILE")
        self.btn_sign.setObjectName("SignButton")
        self.btn_sign.setMinimumHeight(50)
        self.btn_sign.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_sign.clicked.connect(self.sign_file)
        root.addWidget(self.btn_sign)

        # ── Log panel ──
        log_panel = GlassPanel()
        log_layout = QVBoxLayout(log_panel)
        log_layout.setContentsMargins(14, 10, 14, 14)
        log_layout.setSpacing(6)
        log_layout.addWidget(self._section_label("Output Log"))

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(130)
        self.log.setPlaceholderText("// awaiting command...")
        self.log.setStyleSheet(self.log.styleSheet() + "background: transparent;")
        log_layout.addWidget(self.log)
        root.addWidget(log_panel)

    def _section_label(self, text):
        lbl = QLabel(text.upper())
        lbl.setStyleSheet(
            "color: rgba(120, 190, 255, 0.75); font-size: 10px; font-weight: bold; "
            "letter-spacing: 2px; background: transparent;"
        )
        return lbl

    def _file_row(self):
        row = QHBoxLayout()
        row.setSpacing(8)
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("path/to/application.exe")
        self.file_edit.setCompleter(QCompleter(self.history_files))
        btn = QPushButton("Browse")
        btn.setFixedWidth(95)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self.choose_file)
        row.addWidget(self.file_edit)
        row.addWidget(btn)
        return row

    def _cert_row(self):
        row = QHBoxLayout()
        row.setSpacing(8)
        self.cert_edit = QLineEdit()
        self.cert_edit.setPlaceholderText("path/to/certificate.pfx")
        self.cert_edit.setCompleter(QCompleter(self.history_certs))
        btn = QPushButton("Browse")
        btn.setFixedWidth(95)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self.choose_cert)
        row.addWidget(self.cert_edit)
        row.addWidget(btn)
        return row

    def _pass_row(self):
        row = QHBoxLayout()
        row.setSpacing(8)
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_edit.setPlaceholderText("••••••••")
        self.pass_edit.setCompleter(QCompleter(self.history_passwords))
        self.toggle_btn = QPushButton("Show")
        self.toggle_btn.setFixedWidth(95)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.toggled.connect(self._toggle_password)
        row.addWidget(self.pass_edit)
        row.addWidget(self.toggle_btn)
        return row

    # ── Handlers ──────────────────────────────────────────────

    def _toggle_password(self, checked):
        mode = QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        self.pass_edit.setEchoMode(mode)
        self.toggle_btn.setText("Hide" if checked else "Show")

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*.*)")
        if path:
            self.file_edit.setText(path)
            self.add_to_history("history_files", self.history_files, path)

    def choose_cert(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Certificate", "", "Certificates (*.pfx *.p12)")
        if path:
            self.cert_edit.setText(path)
            self.add_to_history("history_certs", self.history_certs, path)

    def sign_file(self):
        file_path = self.file_edit.text().strip()
        cert_path = self.cert_edit.text().strip()
        password = self.pass_edit.text().strip()

        if not file_path:
            self.append_log("  ⚠  No target file specified.")
            return
        if not cert_path:
            self.append_log("  ⚠  No certificate specified.")
            return

        self.add_to_history("history_files", self.history_files, file_path)
        self.add_to_history("history_certs", self.history_certs, cert_path)
        if password:
            self.add_to_history("history_passwords", self.history_passwords, password)

        cmd = [
            "signtool.exe", "sign",
            "/f", cert_path,
            "/p", password,
            "/fd", "sha256",
            "/tr", "http://timestamp.digicert.com",
            "/td", "sha256",
            file_path
        ]

        self.append_log(f"  »  {' '.join(cmd)}\n")
        self.btn_sign.setEnabled(False)
        self.btn_sign.setText("  ⟳  Signing...")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
            if result.stdout:
                self.append_log("── stdout ──")
                self.append_log(result.stdout.strip())
            if result.stderr:
                self.append_log("── stderr ──")
                self.append_log(result.stderr.strip())
            if result.returncode == 0:
                self.append_log("\n  ✔  Signing successful.\n")
            else:
                self.append_log(f"\n  ✖  Error: exit code {result.returncode}\n")
        except Exception as e:
            self.append_log(f"\n  ✖  Exception: {e}\n")
        finally:
            self.btn_sign.setEnabled(True)
            self.btn_sign.setText("▶   SIGN  FILE")

    # ── Helpers ───────────────────────────────────────────────

    def add_to_history(self, key, history_list, value):
        if value not in history_list:
            history_list.insert(0, value)
            history_list[:] = history_list[:10]
            self.settings.setValue(key, history_list)

    def append_log(self, text):
        self.log.append(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SignToolGUI()
    window.show()
    sys.exit(app.exec())
