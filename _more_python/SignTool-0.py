import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel,
    QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QCompleter
)
from PyQt6.QtCore import Qt, QSettings


class SignToolGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SignTool GUI")
        self.setMinimumSize(650, 350)

        # Ustawienia (Windows → rejestr)
        self.settings = QSettings("polsoftITS", "SignToolGUI")

        # Listy historii
        self.history_files = self.settings.value("history_files", [])
        self.history_certs = self.settings.value("history_certs", [])
        self.history_passwords = self.settings.value("history_passwords", [])

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # --- Plik do podpisu ---
        file_layout = QHBoxLayout()
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("Plik do podpisu...")
        self.file_edit.setCompleter(QCompleter(self.history_files))

        btn_file = QPushButton("Wybierz plik")
        btn_file.clicked.connect(self.choose_file)

        file_layout.addWidget(QLabel("Plik:"))
        file_layout.addWidget(self.file_edit)
        file_layout.addWidget(btn_file)

        # --- Certyfikat (PFX) ---
        cert_layout = QHBoxLayout()
        self.cert_edit = QLineEdit()
        self.cert_edit.setPlaceholderText("Certyfikat PFX...")
        self.cert_edit.setCompleter(QCompleter(self.history_certs))

        btn_cert = QPushButton("Wybierz certyfikat")
        btn_cert.clicked.connect(self.choose_cert)

        cert_layout.addWidget(QLabel("Certyfikat:"))
        cert_layout.addWidget(self.cert_edit)
        cert_layout.addWidget(btn_cert)

        # --- Hasło ---
        pass_layout = QHBoxLayout()
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_edit.setPlaceholderText("Hasło do PFX...")
        self.pass_edit.setCompleter(QCompleter(self.history_passwords))

        pass_layout.addWidget(QLabel("Hasło:"))
        pass_layout.addWidget(self.pass_edit)

        # --- Przycisk podpisu ---
        btn_sign = QPushButton("Podpisz")
        btn_sign.clicked.connect(self.sign_file)
        btn_sign.setStyleSheet("font-weight: bold; padding: 6px;")

        # --- Log ---
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        # Layout
        main_layout.addLayout(file_layout)
        main_layout.addLayout(cert_layout)
        main_layout.addLayout(pass_layout)
        main_layout.addWidget(btn_sign)
        main_layout.addWidget(self.log)

        self.setLayout(main_layout)

    # ------------------------------
    # WYBÓR PLIKÓW
    # ------------------------------

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz plik", "", "Wszystkie pliki (*.*)"
        )
        if file_path:
            self.file_edit.setText(file_path)
            self.add_to_history("history_files", self.history_files, file_path)

    def choose_cert(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz certyfikat PFX", "", "Certyfikaty (*.pfx *.p12)"
        )
        if file_path:
            self.cert_edit.setText(file_path)
            self.add_to_history("history_certs", self.history_certs, file_path)

    # ------------------------------
    # PODPISYWANIE
    # ------------------------------

    def sign_file(self):
        file_path = self.file_edit.text().strip()
        cert_path = self.cert_edit.text().strip()
        password = self.pass_edit.text().strip()

        if not file_path:
            self.append_log("❗ Podaj plik do podpisu.")
            return
        if not cert_path:
            self.append_log("❗ Podaj certyfikat PFX.")
            return

        # Zapamiętaj ostatnie dane
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

        self.append_log(f"Uruchamiam: {' '.join(cmd)}\n")

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, shell=False
            )

            if result.stdout:
                self.append_log("=== STDOUT ===")
                self.append_log(result.stdout)
            if result.stderr:
                self.append_log("=== STDERR ===")
                self.append_log(result.stderr)

            if result.returncode == 0:
                self.append_log("✅ Podpis zakończony sukcesem.\n")
            else:
                self.append_log(f"❌ Błąd podpisywania: {result.returncode}\n")

        except Exception as e:
            self.append_log(f"❌ Wyjątek: {e}")

    # ------------------------------
    # HISTORIA / PODPOWIEDZI
    # ------------------------------

    def add_to_history(self, key, history_list, value):
        if value not in history_list:
            history_list.insert(0, value)
            history_list[:] = history_list[:10]  # max 10 pozycji
            self.settings.setValue(key, history_list)

    # ------------------------------

    def append_log(self, text):
        self.log.append(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignToolGUI()
    window.show()
    sys.exit(app.exec())