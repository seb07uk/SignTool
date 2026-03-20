import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel,
    QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QCompleter,
    QFrame
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QColor, QFont


STYLE = """
/* ── Global ── */
QWidget {
    background-color: #0f1117;
    color: #e2e8f0;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
}

/* ── Card panels ── */
#Card {
    background-color: #161b27;
    border: 1px solid #1e2a3a;
    border-radius: 8px;
}

/* ── Section labels ── */
#SectionLabel {
    color: #4a9eff;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 2px;
}

/* ── Input fields ── */
QLineEdit {
    background-color: #0d1117;
    border: 1px solid #2a3548;
    border-radius: 6px;
    padding: 8px 12px;
    color: #c9d1d9;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    selection-background-color: #1f6feb;
}
QLineEdit:focus {
    border: 1px solid #4a9eff;
    color: #e2e8f0;
}
QLineEdit:hover {
    border: 1px solid #3a4d63;
}

/* ── Buttons ── */
QPushButton {
    background-color: #1a2332;
    border: 1px solid #2a3d52;
    border-radius: 6px;
    padding: 8px 16px;
    color: #7d9ab5;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 0.5px;
}
QPushButton:hover {
    background-color: #1f2d42;
    border: 1px solid #4a9eff;
    color: #4a9eff;
}
QPushButton:pressed {
    background-color: #0d1929;
    border: 1px solid #2171cc;
    color: #2171cc;
}

/* ── Sign button ── */
#SignButton {
    background-color: #0d2137;
    border: 1px solid #1f6feb;
    border-radius: 8px;
    color: #4a9eff;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 2px;
    padding: 12px 24px;
}
#SignButton:hover {
    background-color: #0f2d50;
    border: 1px solid #4a9eff;
    color: #7ab8ff;
}
#SignButton:pressed {
    background-color: #061524;
    color: #2171cc;
}
#SignButton:disabled {
    background-color: #0d1929;
    border: 1px solid #1a2d42;
    color: #2a4060;
}

/* ── Log area ── */
QTextEdit {
    background-color: #080c12;
    border: 1px solid #1a2535;
    border-radius: 6px;
    color: #58a6ff;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    padding: 10px;
    selection-background-color: #1f6feb;
}

/* ── Scrollbar ── */
QScrollBar:vertical {
    background: #0d1117;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #2a3d52;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #4a9eff;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }

/* ── Completer popup ── */
QAbstractItemView {
    background-color: #161b27;
    border: 1px solid #2a3548;
    color: #c9d1d9;
    selection-background-color: #1f6feb;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
}

/* ── Header ── */
#HeaderLabel {
    color: #4a9eff;
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 4px;
}
#SubHeaderLabel {
    color: #3a5070;
    font-size: 10px;
    letter-spacing: 3px;
}
#Divider {
    background-color: #1a2a3d;
    max-height: 1px;
}
"""


def make_card():
    frame = QFrame()
    frame.setObjectName("Card")
    return frame


class SignToolGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SignTool GUI  ·  v2.0")
        self.setMinimumSize(700, 520)

        self.settings = QSettings("polsoftITS", "SignToolGUI")
        self.history_files = self.settings.value("history_files", [])
        self.history_certs = self.settings.value("history_certs", [])
        self.history_passwords = self.settings.value("history_passwords", [])

        self.setStyleSheet(STYLE)
        self.init_ui()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        # ── Header ──
        title = QLabel("◈  SIGNTOOL  GUI")
        title.setObjectName("HeaderLabel")
        subtitle = QLabel("CODE SIGNING  ·  SHA-256  ·  DIGICERT TIMESTAMP")
        subtitle.setObjectName("SubHeaderLabel")
        root.addWidget(title)
        root.addWidget(subtitle)

        divider = QFrame()
        divider.setObjectName("Divider")
        divider.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(divider)
        root.addSpacing(4)

        # ── Input card ──
        card = make_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        card_layout.addWidget(self._section_label("TARGET FILE"))
        card_layout.addLayout(self._file_row())

        card_layout.addWidget(self._section_label("CERTIFICATE  (PFX)"))
        card_layout.addLayout(self._cert_row())

        card_layout.addWidget(self._section_label("PASSWORD"))
        card_layout.addLayout(self._pass_row())

        root.addWidget(card)

        # ── Sign button ──
        self.btn_sign = QPushButton("▶   SIGN FILE")
        self.btn_sign.setObjectName("SignButton")
        self.btn_sign.setMinimumHeight(46)
        self.btn_sign.clicked.connect(self.sign_file)
        root.addWidget(self.btn_sign)

        # ── Log ──
        root.addWidget(self._section_label("OUTPUT LOG"))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(130)
        self.log.setPlaceholderText("// ready...")
        root.addWidget(self.log)

    def _section_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("SectionLabel")
        return lbl

    def _file_row(self):
        row = QHBoxLayout()
        row.setSpacing(8)
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("path/to/file.exe")
        self.file_edit.setCompleter(QCompleter(self.history_files))
        btn = QPushButton("Browse")
        btn.setFixedWidth(90)
        btn.clicked.connect(self.choose_file)
        row.addWidget(self.file_edit)
        row.addWidget(btn)
        return row

    def _cert_row(self):
        row = QHBoxLayout()
        row.setSpacing(8)
        self.cert_edit = QLineEdit()
        self.cert_edit.setPlaceholderText("path/to/cert.pfx")
        self.cert_edit.setCompleter(QCompleter(self.history_certs))
        btn = QPushButton("Browse")
        btn.setFixedWidth(90)
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
        self.toggle_pass_btn = QPushButton("Show")
        self.toggle_pass_btn.setFixedWidth(90)
        self.toggle_pass_btn.setCheckable(True)
        self.toggle_pass_btn.toggled.connect(self._toggle_password)
        row.addWidget(self.pass_edit)
        row.addWidget(self.toggle_pass_btn)
        return row

    def _toggle_password(self, checked):
        if checked:
            self.pass_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_pass_btn.setText("Hide")
        else:
            self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_pass_btn.setText("Show")

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "All files (*.*)")
        if path:
            self.file_edit.setText(path)
            self.add_to_history("history_files", self.history_files, path)

    def choose_cert(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select PFX certificate", "", "Certificates (*.pfx *.p12)")
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
        self.btn_sign.setText("  SIGNING...")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=False)

            if result.stdout:
                self.append_log("── STDOUT ──")
                self.append_log(result.stdout.strip())
            if result.stderr:
                self.append_log("── STDERR ──")
                self.append_log(result.stderr.strip())

            if result.returncode == 0:
                self.append_log("\n  ✔  Signing successful.\n")
            else:
                self.append_log(f"\n  ✖  Error: exit code {result.returncode}\n")

        except Exception as e:
            self.append_log(f"\n  ✖  Exception: {e}\n")

        finally:
            self.btn_sign.setEnabled(True)
            self.btn_sign.setText("▶   SIGN FILE")

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
