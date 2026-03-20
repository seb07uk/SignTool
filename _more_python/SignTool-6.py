import sys
import subprocess
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QLabel,
    QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QCompleter,
    QFrame, QStackedWidget, QComboBox, QDialog, QSizePolicy
)
from PyQt6.QtCore import Qt, QSettings, QTimer, QThread, pyqtSignal, QUrl
from PyQt6.QtGui import (
    QColor, QPainter, QPainterPath, QBrush, QPen,
    QLinearGradient, QRadialGradient, QIcon, QDesktopServices, QFont
)
import os

# ══════════════════════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════════════════════
TR = {
    "en": {
        "window_title":     "SignTool  ·  Sign  ·  Verify  ·  Install",
        "header_sub":       "Sign · Verify · Install  ·  SHA-256  ·  DigiCert",
        "tab_sign":         "▶  Sign",
        "tab_verify":       "🔍  Verify",
        "tab_install":      "📥  Install",
        "tab_cert_mgr":     "🔐  Certificates",
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
        # Certificate dialog
        "cert_dlg_title":       "Certificate Manager",
        "cert_tab_self":        "Self-Signed",
        "cert_tab_csr":         "CSR / CA-Signed",
        "cert_tab_pfx":         "Export / PFX",
        "cert_lbl_cn":          "Common Name (CN)",
        "cert_ph_cn":           "e.g. My App  /  company.com",
        "cert_lbl_org":         "Organization (O)",
        "cert_ph_org":          "e.g. polsoft.ITS Group",
        "cert_lbl_ou":          "Unit (OU)",
        "cert_ph_ou":           "e.g. Development",
        "cert_lbl_country":     "Country (C)",
        "cert_ph_country":      "e.g. PL",
        "cert_lbl_days":        "Valid (days)",
        "cert_lbl_keysize":     "Key size (bits)",
        "cert_lbl_out_dir":     "Output folder",
        "cert_ph_out_dir":      "path/to/output/folder",
        "cert_lbl_base":        "Base name",
        "cert_ph_base":         "e.g. my_cert",
        "cert_lbl_pass":        "PFX password",
        "cert_ph_pass":         "leave blank = no password",
        "cert_btn_gen_self":    "GENERATE  SELF-SIGNED",
        "cert_lbl_csr_key":     "Existing private key  (optional)",
        "cert_ph_csr_key":      "leave blank = generate new key",
        "cert_btn_gen_csr":     "GENERATE  CSR",
        "cert_lbl_pfx_cert":    "Certificate  (.cer / .crt / .pem)",
        "cert_ph_pfx_cert":     "path/to/certificate.cer",
        "cert_lbl_pfx_key":     "Private key  (.key / .pem)",
        "cert_ph_pfx_key":      "path/to/private.key",
        "cert_lbl_pfx_chain":   "CA chain  (optional)",
        "cert_ph_pfx_chain":    "path/to/ca-bundle.pem",
        "cert_btn_gen_pfx":     "EXPORT  TO  PFX",
        "cert_lbl_log":         "Certificate Log",
        "cert_btn_close":       "CLOSE",
        "cert_btn_browse":      "Browse",
        "cert_warn_openssl":    "\u26a0  openssl not found in PATH",
        "cert_ok_self":         "\n  \u2714  Self-signed certificate generated.\n",
        "cert_ok_csr":          "\n  \u2714  CSR and key generated.\n",
        "cert_ok_pfx":          "\n  \u2714  PFX exported successfully.\n",
        "cert_fail":            "\n  \u2716  Failed (exit {code})\n",
        "cert_no_cn":           "  \u26a0  Common Name (CN) is required.",
        "cert_no_outdir":       "  \u26a0  Output folder is required.",
        "cert_no_cert":         "  \u26a0  Certificate file is required.",
        "cert_no_key":          "  \u26a0  Private key file is required.",
        "cert_running":         "  \u27f3  Generating...",
        "cert_files":           "  Files written:\n",
        "btn_cert_mgr":         "Certificates",
        "cert_tab_page_desc":   "Generate self-signed certificates, create CSR requests\nand export to PFX format using OpenSSL.",
        "cert_tab_page_btn":    "🔐   OPEN  CERTIFICATE  MANAGER",
        # Theme toggle
        "theme_dark":       "DARK",
        "theme_light":      "LIGHT",
        # Lang toggle
        "lang_btn":         "PL",
    },
    "pl": {
        "window_title":     "SignTool  ·  Podpisz  ·  Weryfikuj  ·  Instaluj",
        "header_sub":       "Podpisz · Weryfikuj · Instaluj  ·  SHA-256  ·  DigiCert",
        "tab_sign":         "▶  Podpisz",
        "tab_verify":       "🔍  Weryfikuj",
        "tab_install":      "📥  Instaluj",
        "tab_cert_mgr":     "🔐  Certyfikaty",
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
        # Certificate dialog
        "cert_dlg_title":       "Menedzer certyfikatow",
        "cert_tab_self":        "Samopodpisany",
        "cert_tab_csr":         "CSR / Podpisany CA",
        "cert_tab_pfx":         "Eksport / PFX",
        "cert_lbl_cn":          "Nazwa pospolita (CN)",
        "cert_ph_cn":           "np. Moja Apka  /  firma.com",
        "cert_lbl_org":         "Organizacja (O)",
        "cert_ph_org":          "np. polsoft.ITS Group",
        "cert_lbl_ou":          "Jednostka (OU)",
        "cert_ph_ou":           "np. Development",
        "cert_lbl_country":     "Kraj (C)",
        "cert_ph_country":      "np. PL",
        "cert_lbl_days":        "Waznosc (dni)",
        "cert_lbl_keysize":     "Rozmiar klucza (bity)",
        "cert_lbl_out_dir":     "Folder wyjsciowy",
        "cert_ph_out_dir":      "sciezka/do/folderu",
        "cert_lbl_base":        "Nazwa bazowa",
        "cert_ph_base":         "np. moj_cert",
        "cert_lbl_pass":        "Haslo PFX",
        "cert_ph_pass":         "pozostaw puste = brak hasla",
        "cert_btn_gen_self":    "GENERUJ  SAMOPODPISANY",
        "cert_lbl_csr_key":     "Istniejacy klucz prywatny (opcja)",
        "cert_ph_csr_key":      "puste = wygeneruj nowy klucz",
        "cert_btn_gen_csr":     "GENERUJ  CSR",
        "cert_lbl_pfx_cert":    "Certyfikat  (.cer / .crt / .pem)",
        "cert_ph_pfx_cert":     "sciezka/do/certyfikatu.cer",
        "cert_lbl_pfx_key":     "Klucz prywatny  (.key / .pem)",
        "cert_ph_pfx_key":      "sciezka/do/klucza.key",
        "cert_lbl_pfx_chain":   "Lancuch CA  (opcjonalnie)",
        "cert_ph_pfx_chain":    "sciezka/do/ca-bundle.pem",
        "cert_btn_gen_pfx":     "EKSPORTUJ  DO  PFX",
        "cert_lbl_log":         "Dziennik certyfikatow",
        "cert_btn_close":       "ZAMKNIJ",
        "cert_btn_browse":      "Wybierz",
        "cert_warn_openssl":    "\u26a0  openssl nie znaleziony w PATH",
        "cert_ok_self":         "\n  \u2714  Certyfikat samopodpisany wygenerowany.\n",
        "cert_ok_csr":          "\n  \u2714  CSR i klucz wygenerowane.\n",
        "cert_ok_pfx":          "\n  \u2714  PFX wyeksportowany pomyslnie.\n",
        "cert_fail":            "\n  \u2716  Blad (exit {code})\n",
        "cert_no_cn":           "  \u26a0  Nazwa pospolita (CN) jest wymagana.",
        "cert_no_outdir":       "  \u26a0  Folder wyjsciowy jest wymagany.",
        "cert_no_cert":         "  \u26a0  Plik certyfikatu jest wymagany.",
        "cert_no_key":          "  \u26a0  Plik klucza prywatnego jest wymagany.",
        "cert_running":         "  \u27f3  Generowanie...",
        "cert_files":           "  Zapisano pliki:\n",
        "btn_cert_mgr":         "Certyfikaty",
        "cert_tab_page_desc":   "Generuj certyfikaty samopodpisane, twórz żądania CSR\ni eksportuj do formatu PFX przy użyciu OpenSSL.",
        "cert_tab_page_btn":    "🔐   OTWÓRZ  MENEDŻER  CERTYFIKATÓW",
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
        "bg_base":      QColor(3, 8, 24),
        "orb1":         (20, 60, 200, 25),
        "orb2":         (0, 110, 230, 25),
        "orb3":         (100, 30, 210, 22),
        "orb4":         (0, 180, 200, 15),
        "grid":         QColor(50, 100, 220, 6),
        "vign":         QColor(0, 0, 10, 25),
        "panel_fill":   QColor(180, 210, 255, 15),
        "panel_accent": QColor(25, 65, 180, 25),
        "gloss":        QColor(255, 255, 255, 21),
        "gloss2":       QColor(100, 180, 255, 12),
        "border_top":   QColor(140, 200, 255, 25),
        "border_mid":   QColor(80, 150, 255, 25),
        "border_bot":   QColor(50, 110, 220, 25),
        "inner_glow":   QColor(60, 140, 255, 18),
    },
    "light": {
        "bg_base":      QColor(210, 228, 255),
        "orb1":         (90, 150, 255, 25),
        "orb2":         (50, 170, 240, 22),
        "orb3":         (140, 90, 245, 17),
        "orb4":         (0, 200, 220, 12),
        "grid":         QColor(70, 120, 220, 9),
        "vign":         QColor(160, 185, 235, 25),
        "panel_fill":   QColor(255, 255, 255, 25),
        "panel_accent": QColor(210, 228, 255, 25),
        "gloss":        QColor(255, 255, 255, 25),
        "gloss2":       QColor(200, 225, 255, 25),
        "border_top":   QColor(110, 170, 255, 25),
        "border_mid":   QColor(80, 130, 225, 25),
        "border_bot":   QColor(60, 110, 205, 25),
        "inner_glow":   QColor(100, 160, 255, 25),
    },
}

STYLE_DARK = """
QWidget{font-family:'Segoe UI','Arial',sans-serif;font-size:12px;color:#ddeeff;}
QLineEdit{
  background-color:rgba(8,20,55,0.10);
  border:1px solid rgba(80,150,255,0.10);
  border-radius:7px;padding:7px 11px;color:#cce4ff;font-size:12px;
  selection-background-color:rgba(60,140,255,0.10);}
QLineEdit:focus{border:1px solid rgba(90,170,255,0.10);background-color:rgba(12,28,70,0.10);}
QLineEdit:hover{border:1px solid rgba(90,160,255,0.10);background-color:rgba(10,24,62,0.10);}
QComboBox{
  background-color:rgba(8,20,55,0.10);
  border:1px solid rgba(80,150,255,0.10);
  border-radius:7px;padding:7px 11px;color:#cce4ff;font-size:12px;}
QComboBox:focus{border:1px solid rgba(90,170,255,0.10);}
QComboBox::drop-down{border:none;width:22px;}
QComboBox::down-arrow{image:none;border-left:4px solid transparent;border-right:4px solid transparent;border-top:5px solid rgba(100,170,255,0.10);margin-right:7px;}
QComboBox QAbstractItemView{background-color:rgba(8,20,55,0.10);border:1px solid rgba(80,150,255,0.10);color:#b8d8ff;selection-background-color:rgba(40,110,230,0.10);}
QPushButton{
  background-color:rgba(30,70,180,0.10);
  border:1px solid rgba(90,160,255,0.10);
  border-radius:7px;padding:6px 14px;color:#90c4ff;font-size:12px;font-weight:bold;}
QPushButton:hover{background-color:rgba(50,110,230,0.10);border:1px solid rgba(120,190,255,0.10);color:#c8e4ff;}
QPushButton:pressed{background-color:rgba(30,80,200,0.10);color:#7ab4ff;}
#ActionButton{
  background:qlineargradient(x1:0,y1:0,x2:0,y2:1,
    stop:0 rgba(40,120,255,0.10),stop:0.3 rgba(30,100,240,0.10),
    stop:0.7 rgba(20,75,215,0.10),stop:1 rgba(10,55,190,0.10));
  border:1px solid rgba(100,190,255,0.10);
  border-radius:9px;color:#c8e8ff;font-size:13px;font-weight:bold;letter-spacing:2px;padding:11px 20px;}
#ActionButton:hover{
  background:qlineargradient(x1:0,y1:0,x2:0,y2:1,
    stop:0 rgba(60,150,255,0.10),stop:1 rgba(20,80,210,0.10));
  border:1px solid rgba(140,210,255,0.10);color:#e8f6ff;}
#ActionButton:pressed{background:rgba(20,80,210,0.10);color:#7ab4ff;}
#ActionButton:disabled{background:rgba(20,50,120,0.10);border:1px solid rgba(60,110,200,0.10);color:rgba(120,180,255,0.10);}
QTextEdit{
  background-color:rgba(4,10,30,0.10);
  border:1px solid rgba(50,120,220,0.10);
  border-radius:7px;color:#5aacff;
  font-family:'Consolas','Courier New',monospace;font-size:11px;padding:9px;
  selection-background-color:rgba(50,130,255,0.10);}
QScrollBar:vertical{background:transparent;width:5px;border-radius:2px;}
QScrollBar::handle:vertical{background:rgba(80,150,255,0.10);border-radius:2px;min-height:16px;}
QScrollBar::handle:vertical:hover{background:rgba(110,180,255,0.10);}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0px;}
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:none;}
QAbstractItemView{background-color:rgba(8,20,55,0.10);border:1px solid rgba(80,150,255,0.10);color:#b0d4ff;selection-background-color:rgba(40,110,230,0.10);font-size:12px;}
"""

STYLE_LIGHT = """
QWidget{font-family:'Segoe UI','Arial',sans-serif;font-size:12px;color:#162040;}
QLineEdit{
  background-color:rgba(255,255,255,0.10);
  border:1px solid rgba(90,140,215,0.10);
  border-radius:7px;padding:7px 11px;color:#162040;font-size:12px;
  selection-background-color:rgba(80,150,255,0.10);}
QLineEdit:focus{border:1px solid rgba(60,120,225,0.10);background-color:rgba(255,255,255,0.10);}
QLineEdit:hover{border:1px solid rgba(80,135,220,0.10);background-color:rgba(255,255,255,0.10);}
QComboBox{
  background-color:rgba(255,255,255,0.10);
  border:1px solid rgba(90,140,215,0.10);
  border-radius:7px;padding:7px 11px;color:#162040;font-size:12px;}
QComboBox:focus{border:1px solid rgba(60,120,225,0.10);}
QComboBox::drop-down{border:none;width:22px;}
QComboBox::down-arrow{image:none;border-left:4px solid transparent;border-right:4px solid transparent;border-top:5px solid rgba(60,100,210,0.10);margin-right:7px;}
QComboBox QAbstractItemView{background-color:rgba(245,250,255,0.10);border:1px solid rgba(80,130,215,0.10);color:#162040;selection-background-color:rgba(100,160,255,0.10);}
QPushButton{
  background-color:rgba(100,150,230,0.10);
  border:1px solid rgba(90,135,215,0.10);
  border-radius:7px;padding:6px 14px;color:#1e3a80;font-size:12px;font-weight:bold;}
QPushButton:hover{background-color:rgba(90,140,230,0.10);border:1px solid rgba(60,115,210,0.10);color:#122868;}
QPushButton:pressed{background-color:rgba(70,120,210,0.10);color:#0a2060;}
#ActionButton{
  background:qlineargradient(x1:0,y1:0,x2:0,y2:1,
    stop:0 rgba(70,140,255,0.10),stop:0.35 rgba(55,118,245,0.10),
    stop:0.65 rgba(40,95,230,0.10),stop:1 rgba(30,80,215,0.10));
  border:1px solid rgba(80,155,255,0.10);
  border-radius:9px;color:#ffffff;font-size:13px;font-weight:bold;letter-spacing:2px;padding:11px 20px;}
#ActionButton:hover{
  background:qlineargradient(x1:0,y1:0,x2:0,y2:1,
    stop:0 rgba(90,160,255,0.10),stop:1 rgba(40,95,230,0.10));
  border:1px solid rgba(110,175,255,0.10);color:#ffffff;}
#ActionButton:pressed{background:rgba(40,95,230,0.10);color:#d0e8ff;}
#ActionButton:disabled{background:rgba(100,140,215,0.10);border:1px solid rgba(90,130,210,0.10);color:rgba(80,120,210,0.10);}
QTextEdit{
  background-color:rgba(240,247,255,0.10);
  border:1px solid rgba(90,135,215,0.10);
  border-radius:7px;color:#1a3a70;
  font-family:'Consolas','Courier New',monospace;font-size:11px;padding:9px;
  selection-background-color:rgba(80,150,255,0.10);}
QScrollBar:vertical{background:transparent;width:5px;border-radius:2px;}
QScrollBar::handle:vertical{background:rgba(90,135,225,0.10);border-radius:2px;min-height:16px;}
QScrollBar::handle:vertical:hover{background:rgba(70,115,210,0.10);}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0px;}
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:none;}
QAbstractItemView{background-color:rgba(245,250,255,0.10);border:1px solid rgba(80,130,215,0.10);color:#162040;selection-background-color:rgba(100,160,255,0.10);font-size:12px;}
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

# ══════════════════════════════════════════════════════════
#  APP METADATA
# ══════════════════════════════════════════════════════════
APP_META = {
    "name":       "SignTool",
    "version":    "1.0.0",
    "author":     "Sebastian Januchowski",
    "company":    "polsoft.ITS™ Group",
    "email":      "polsoft.its@fastservice.com",
    "github":     "https://github.com/seb07uk",
    "copyright":  "2026 © Sebastian Januchowski & polsoft.ITS™",
    "description_en": (
        "A professional code-signing utility for Windows.\n"
        "Sign, verify and install digital certificates\n"
        "using Microsoft SignTool & CertUtil."
    ),
    "description_pl": (
        "Profesjonalne narzędzie do podpisywania kodu.\n"
        "Podpisuj, weryfikuj i instaluj certyfikaty cyfrowe\n"
        "za pomocą Microsoft SignTool i CertUtil."
    ),
}


# ══════════════════════════════════════════════════════════
#  ABOUT DIALOG
# ══════════════════════════════════════════════════════════
class AboutDialog(QDialog):
    def __init__(self, parent=None, theme="dark", lang="en"):
        super().__init__(parent)
        self._theme = theme
        self._lang  = lang
        self.setWindowTitle("About  —  SignTool")
        self.setFixedSize(400, 430)
        self.setModal(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self._build()
        self._apply_theme(theme)

    # ── drag to move ──────────────────────────────────────
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton and hasattr(self, '_drag_pos'):
            self.move(e.globalPosition().toPoint() - self._drag_pos)

    # ── build ─────────────────────────────────────────────
    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Glass container
        self._glass = GlassPanel(accent=True)
        self._glass.set_theme(self._theme)
        inner = QVBoxLayout(self._glass)
        inner.setContentsMargins(28, 24, 28, 24)
        inner.setSpacing(10)

        # ── Logo row ──
        logo_row = QHBoxLayout()
        logo_row.setSpacing(14)
        _icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Icon_for_SignTool.ico")
        self._logo_lbl = QLabel()
        self._logo_lbl.setFixedSize(56, 56)
        self._logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._logo_lbl.setStyleSheet("background:transparent;")
        if os.path.isfile(_icon_path):
            self._logo_lbl.setPixmap(QIcon(_icon_path).pixmap(56, 56))

        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        self._app_name_lbl = QLabel(APP_META["name"])
        self._app_ver_lbl  = QLabel(f"v{APP_META['version']}")
        self._app_name_lbl.setStyleSheet("font-size:22px;font-weight:bold;letter-spacing:3px;background:transparent;")
        self._app_ver_lbl.setStyleSheet("font-size:11px;letter-spacing:2px;background:transparent;")
        title_col.addWidget(self._app_name_lbl)
        title_col.addWidget(self._app_ver_lbl)
        title_col.addStretch()

        logo_row.addWidget(self._logo_lbl)
        logo_row.addLayout(title_col)
        logo_row.addStretch()
        inner.addLayout(logo_row)

        # ── Divider ──
        self._div1 = QFrame(); self._div1.setFrameShape(QFrame.Shape.HLine)
        inner.addWidget(self._div1)

        # ── Description ──
        desc_key = "description_pl" if self._lang == "pl" else "description_en"
        self._desc_lbl = QLabel(APP_META[desc_key])
        self._desc_lbl.setWordWrap(True)
        self._desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._desc_lbl.setStyleSheet("font-size:11px;line-height:160%;background:transparent;")
        inner.addWidget(self._desc_lbl)

        # ── Divider ──
        self._div2 = QFrame(); self._div2.setFrameShape(QFrame.Shape.HLine)
        inner.addWidget(self._div2)

        # ── Info grid ──
        def _info_row(label, value, clickable_url=None):
            row = QHBoxLayout(); row.setSpacing(8)
            lbl_k = QLabel(label)
            lbl_k.setFixedWidth(80)
            lbl_k.setStyleSheet("font-size:10px;font-weight:bold;letter-spacing:1px;background:transparent;")
            lbl_v = QLabel(value)
            lbl_v.setWordWrap(True)
            lbl_v.setStyleSheet("font-size:11px;background:transparent;")
            if clickable_url:
                lbl_v.setCursor(Qt.CursorShape.PointingHandCursor)
                lbl_v.setStyleSheet("font-size:11px;background:transparent;text-decoration:underline;")
                lbl_v.mousePressEvent = lambda _e, url=clickable_url: QDesktopServices.openUrl(QUrl(url))
            row.addWidget(lbl_k)
            row.addWidget(lbl_v, 1)
            return row

        self._rows_widget = QWidget()
        self._rows_widget.setStyleSheet("background:transparent;")
        rows_lay = QVBoxLayout(self._rows_widget)
        rows_lay.setContentsMargins(0, 0, 0, 0)
        rows_lay.setSpacing(6)

        author_lbl = "Autor" if self._lang == "pl" else "Author"
        company_lbl = "Firma" if self._lang == "pl" else "Company"
        email_lbl = "E-mail"
        github_lbl = "GitHub"

        rows_lay.addLayout(_info_row(author_lbl,  APP_META["author"]))
        rows_lay.addLayout(_info_row(company_lbl, APP_META["company"]))
        rows_lay.addLayout(_info_row(email_lbl,   APP_META["email"],  "mailto:" + APP_META["email"]))
        rows_lay.addLayout(_info_row(github_lbl,  APP_META["github"],  APP_META["github"]))
        inner.addWidget(self._rows_widget)

        # ── Divider ──
        self._div3 = QFrame(); self._div3.setFrameShape(QFrame.Shape.HLine)
        inner.addWidget(self._div3)

        # ── Copyright ──
        self._copy_lbl = QLabel(APP_META["copyright"])
        self._copy_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._copy_lbl.setStyleSheet("font-size:10px;letter-spacing:1px;background:transparent;")
        inner.addWidget(self._copy_lbl)

        inner.addStretch()

        # ── Close button ──
        self._close_btn = QPushButton("✕  CLOSE" if self._lang == "en" else "✕  ZAMKNIJ")
        self._close_btn.setObjectName("ActionButton")
        self._close_btn.setMinimumHeight(38)
        self._close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._close_btn.clicked.connect(self.accept)
        inner.addWidget(self._close_btn)

        root.addWidget(self._glass)

    def _apply_theme(self, theme):
        self._theme = theme
        self._glass.set_theme(theme)
        is_dark = theme == "dark"

        if is_dark:
            name_c   = "#a8d8ff"
            ver_c    = "rgba(120,190,255,0.55)"
            desc_c   = "rgba(160,200,255,0.75)"
            key_c    = "rgba(120,190,255,0.55)"
            val_c    = "#cce4ff"
            link_c   = "#60b4ff"
            copy_c   = "rgba(120,170,255,0.45)"
            div_c    = "rgba(80,150,255,0.18)"
        else:
            name_c   = "#1a3a80"
            ver_c    = "rgba(50,100,200,0.6)"
            desc_c   = "rgba(30,70,180,0.8)"
            key_c    = "rgba(50,100,200,0.6)"
            val_c    = "#162040"
            link_c   = "#1a60cc"
            copy_c   = "rgba(40,80,180,0.5)"
            div_c    = "rgba(80,130,220,0.25)"

        self._app_name_lbl.setStyleSheet(f"font-size:22px;font-weight:bold;letter-spacing:3px;background:transparent;color:{name_c};")
        self._app_ver_lbl.setStyleSheet(f"font-size:11px;letter-spacing:2px;background:transparent;color:{ver_c};")
        self._desc_lbl.setStyleSheet(f"font-size:11px;line-height:160%;background:transparent;color:{desc_c};")
        self._copy_lbl.setStyleSheet(f"font-size:10px;letter-spacing:1px;background:transparent;color:{copy_c};")

        div_style = f"background:transparent;color:{div_c};border:none;border-top:1px solid {div_c};"
        for div in (self._div1, self._div2, self._div3):
            div.setStyleSheet(div_style)

        # Re-style all info rows
        for row_w in self._rows_widget.findChildren(QLabel):
            if row_w.minimumWidth() == 80 or row_w.maximumWidth() == 80:
                row_w.setStyleSheet(f"font-size:10px;font-weight:bold;letter-spacing:1px;background:transparent;color:{key_c};")
            else:
                is_link = "underline" in row_w.styleSheet()
                if is_link:
                    row_w.setStyleSheet(f"font-size:11px;background:transparent;text-decoration:underline;color:{link_c};")
                else:
                    row_w.setStyleSheet(f"font-size:11px;background:transparent;color:{val_c};")

        btn_style = (
            f"QPushButton{{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f"stop:0 rgba(40,120,255,0.55),stop:1 rgba(10,55,190,0.45));"
            f"border:1px solid rgba(100,190,255,0.65);border-radius:9px;"
            f"color:#c8e8ff;font-size:12px;font-weight:bold;letter-spacing:2px;padding:9px 20px;}}"
            f"QPushButton:hover{{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f"stop:0 rgba(60,150,255,0.65),stop:1 rgba(20,80,210,0.55));"
            f"border:1px solid rgba(140,210,255,0.85);color:#e8f6ff;}}"
            f"QPushButton:pressed{{background:rgba(20,80,210,0.5);color:#7ab4ff;}}"
        ) if is_dark else (
            f"QPushButton{{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f"stop:0 rgba(70,140,255,0.7),stop:1 rgba(30,80,215,0.65));"
            f"border:1px solid rgba(80,155,255,0.75);border-radius:9px;"
            f"color:#ffffff;font-size:12px;font-weight:bold;letter-spacing:2px;padding:9px 20px;}}"
            f"QPushButton:hover{{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f"stop:0 rgba(90,160,255,0.82),stop:1 rgba(40,95,230,0.75));"
            f"border:1px solid rgba(110,175,255,0.95);color:#ffffff;}}"
            f"QPushButton:pressed{{background:rgba(40,95,230,0.7);color:#d0e8ff;}}"
        )
        self._close_btn.setStyleSheet(btn_style)


# ══════════════════════════════════════════════════════════
#  CERTIFICATE MANAGER DIALOG
# ══════════════════════════════════════════════════════════
class CertManagerDialog(QDialog):
    """Full-featured certificate generation popup:
       Tab 1 – Self-Signed  (openssl req -x509)
       Tab 2 – CSR          (openssl req)
       Tab 3 – Export PFX   (openssl pkcs12)
    """

    def __init__(self, parent=None, theme="dark", lang="en", tr_fn=None):
        super().__init__(parent)
        self._theme  = theme
        self._lang   = lang
        self._tr     = tr_fn if tr_fn else lambda k, **kw: k
        self._workers = []

        self.setWindowTitle(self._tr("cert_dlg_title"))
        self.setMinimumSize(560, 640)
        self.resize(580, 660)
        self.setModal(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self._panels = []
        self._build()
        self._apply_theme(theme)

    # ── drag ─────────────────────────────────────────────
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton and hasattr(self, '_drag_pos'):
            self.move(e.globalPosition().toPoint() - self._drag_pos)

    # ── helpers ──────────────────────────────────────────
    def _slbl(self, text=""):
        l = QLabel(text)
        l.setStyleSheet("font-size:10px;font-weight:bold;letter-spacing:2px;background:transparent;")
        return l

    def _le(self, ph="", pw=False):
        e = QLineEdit()
        e.setPlaceholderText(ph)
        if pw:
            e.setEchoMode(QLineEdit.EchoMode.Password)
        return e

    def _browse_btn(self, edit, folder=False):
        btn = QPushButton(self._tr("cert_btn_browse"))
        btn.setFixedWidth(76)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if folder:
            btn.clicked.connect(lambda: self._pick_folder(edit))
        else:
            btn.clicked.connect(lambda: self._pick_file(edit))
        return btn

    def _row(self, edit, folder=False):
        h = QHBoxLayout(); h.setSpacing(6)
        h.addWidget(edit); h.addWidget(self._browse_btn(edit, folder))
        return h

    def _pick_folder(self, edit):
        p = QFileDialog.getExistingDirectory(self, self._tr("cert_lbl_out_dir"))
        if p: edit.setText(p)

    def _pick_file(self, edit):
        p, _ = QFileDialog.getOpenFileName(self, "Select file", "", "All Files (*.*)")
        if p: edit.setText(p)

    def _action_btn(self, text, cb):
        b = QPushButton(text)
        b.setObjectName("ActionButton")
        b.setMinimumHeight(40)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(cb)
        return b

    def _panel(self, accent=False):
        pn = GlassPanel(accent=accent)
        pn.set_theme(self._theme)
        self._panels.append(pn)
        return pn

    # ── build ─────────────────────────────────────────────
    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        outer = self._panel(accent=True)
        main  = QVBoxLayout(outer)
        main.setContentsMargins(16, 14, 16, 16)
        main.setSpacing(8)

        # ── Header row ──
        hdr_row = QHBoxLayout()
        self._title_lbl = QLabel("🔐  " + self._tr("cert_dlg_title"))
        self._title_lbl.setStyleSheet(
            "font-size:15px;font-weight:bold;letter-spacing:2px;background:transparent;")
        hdr_row.addWidget(self._title_lbl)
        hdr_row.addStretch()
        x_btn = QPushButton("✕")
        x_btn.setFixedSize(24, 24)
        x_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        x_btn.clicked.connect(self.reject)
        self._x_btn = x_btn
        hdr_row.addWidget(x_btn)
        main.addLayout(hdr_row)

        # ── openssl warning ──
        self._warn_lbl = QLabel(self._tr("cert_warn_openssl"))
        self._warn_lbl.setVisible(not self._openssl_ok())
        self._warn_lbl.setWordWrap(True)
        self._warn_lbl.setStyleSheet(
            "color:rgba(255,180,60,0.85);font-size:10px;background:transparent;")
        main.addWidget(self._warn_lbl)

        # ── Tab bar ──
        self._tab_bar = TabBar()
        self._tab_bar.set_theme(self._theme)
        self._tab_bar.set_labels([
            self._tr("cert_tab_self"),
            self._tr("cert_tab_csr"),
            self._tr("cert_tab_pfx"),
        ])
        main.addWidget(self._tab_bar)

        # ── Stacked pages ──
        self._stack = QStackedWidget()
        self._stack.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._stack.addWidget(self._page_self())
        self._stack.addWidget(self._page_csr())
        self._stack.addWidget(self._page_pfx())
        self._tab_bar.tab_changed.connect(self._stack.setCurrentIndex)
        main.addWidget(self._stack, stretch=1)

        # ── Log ──
        log_card = self._panel()
        ll = QVBoxLayout(log_card)
        ll.setContentsMargins(10, 7, 10, 10)
        ll.setSpacing(4)
        self._log_lbl = self._slbl(self._tr("cert_lbl_log").upper())
        ll.addWidget(self._log_lbl)
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFixedHeight(110)
        ll.addWidget(self._log)
        main.addWidget(log_card)

        root.addWidget(outer)

    # ── Page: Self-Signed ────────────────────────────────
    def _page_self(self):
        pg = QWidget(); pg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        vb = QVBoxLayout(pg); vb.setContentsMargins(0,0,0,0); vb.setSpacing(6)

        card = self._panel()
        cl = QVBoxLayout(card); cl.setContentsMargins(12,10,12,12); cl.setSpacing(6)

        # Subject fields
        self._self_cn    = self._le(self._tr("cert_ph_cn"))
        self._self_org   = self._le(self._tr("cert_ph_org"))
        self._self_ou    = self._le(self._tr("cert_ph_ou"))
        self._self_c     = self._le(self._tr("cert_ph_country")); self._self_c.setMaximumWidth(80)
        self._self_days  = QLineEdit("365"); self._self_days.setMaximumWidth(80)
        self._self_key   = QComboBox()
        self._self_key.addItems(["2048", "3072", "4096"])
        self._self_key.setMaximumWidth(90)

        for lbl_key, widget, is_row in [
            ("cert_lbl_cn",      self._self_cn,   False),
            ("cert_lbl_org",     self._self_org,  False),
            ("cert_lbl_ou",      self._self_ou,   False),
        ]:
            cl.addWidget(self._slbl(self._tr(lbl_key).upper()))
            cl.addWidget(widget)

        # Country + days + keysize on one row
        tiny = QHBoxLayout(); tiny.setSpacing(10)
        col_c = QVBoxLayout(); col_c.setSpacing(3)
        col_c.addWidget(self._slbl(self._tr("cert_lbl_country").upper()))
        col_c.addWidget(self._self_c)
        col_d = QVBoxLayout(); col_d.setSpacing(3)
        col_d.addWidget(self._slbl(self._tr("cert_lbl_days").upper()))
        col_d.addWidget(self._self_days)
        col_k = QVBoxLayout(); col_k.setSpacing(3)
        col_k.addWidget(self._slbl(self._tr("cert_lbl_keysize").upper()))
        col_k.addWidget(self._self_key)
        tiny.addLayout(col_c); tiny.addLayout(col_d); tiny.addLayout(col_k); tiny.addStretch()
        cl.addLayout(tiny)

        # Output dir + base name + password
        self._self_outdir = self._le(self._tr("cert_ph_out_dir"))
        self._self_base   = self._le(self._tr("cert_ph_base"))
        self._self_pass   = self._le(self._tr("cert_ph_pass"), pw=True)

        cl.addWidget(self._slbl(self._tr("cert_lbl_out_dir").upper()))
        cl.addLayout(self._row(self._self_outdir, folder=True))
        row2 = QHBoxLayout(); row2.setSpacing(10)
        col_b = QVBoxLayout(); col_b.setSpacing(3)
        col_b.addWidget(self._slbl(self._tr("cert_lbl_base").upper()))
        col_b.addWidget(self._self_base)
        col_p = QVBoxLayout(); col_p.setSpacing(3)
        col_p.addWidget(self._slbl(self._tr("cert_lbl_pass").upper()))
        col_p.addWidget(self._self_pass)
        row2.addLayout(col_b, 1); row2.addLayout(col_p, 1)
        cl.addLayout(row2)

        vb.addWidget(card)
        self._btn_self = self._action_btn(
            "🔐   " + self._tr("cert_btn_gen_self"), self._do_self_signed)
        vb.addWidget(self._btn_self)
        vb.addStretch()
        return pg

    # ── Page: CSR ────────────────────────────────────────
    def _page_csr(self):
        pg = QWidget(); pg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        vb = QVBoxLayout(pg); vb.setContentsMargins(0,0,0,0); vb.setSpacing(6)

        card = self._panel()
        cl = QVBoxLayout(card); cl.setContentsMargins(12,10,12,12); cl.setSpacing(6)

        self._csr_cn   = self._le(self._tr("cert_ph_cn"))
        self._csr_org  = self._le(self._tr("cert_ph_org"))
        self._csr_ou   = self._le(self._tr("cert_ph_ou"))
        self._csr_c    = self._le(self._tr("cert_ph_country")); self._csr_c.setMaximumWidth(80)
        self._csr_key  = QComboBox()
        self._csr_key.addItems(["2048", "3072", "4096"]); self._csr_key.setMaximumWidth(90)

        for lbl_key, widget in [
            ("cert_lbl_cn",  self._csr_cn),
            ("cert_lbl_org", self._csr_org),
            ("cert_lbl_ou",  self._csr_ou),
        ]:
            cl.addWidget(self._slbl(self._tr(lbl_key).upper()))
            cl.addWidget(widget)

        tiny = QHBoxLayout(); tiny.setSpacing(10)
        col_c = QVBoxLayout(); col_c.setSpacing(3)
        col_c.addWidget(self._slbl(self._tr("cert_lbl_country").upper()))
        col_c.addWidget(self._csr_c)
        col_k = QVBoxLayout(); col_k.setSpacing(3)
        col_k.addWidget(self._slbl(self._tr("cert_lbl_keysize").upper()))
        col_k.addWidget(self._csr_key)
        tiny.addLayout(col_c); tiny.addLayout(col_k); tiny.addStretch()
        cl.addLayout(tiny)

        self._csr_existing_key = self._le(self._tr("cert_ph_csr_key"))
        self._csr_outdir       = self._le(self._tr("cert_ph_out_dir"))
        self._csr_base         = self._le(self._tr("cert_ph_base"))

        cl.addWidget(self._slbl(self._tr("cert_lbl_csr_key").upper()))
        cl.addLayout(self._row(self._csr_existing_key))
        cl.addWidget(self._slbl(self._tr("cert_lbl_out_dir").upper()))
        cl.addLayout(self._row(self._csr_outdir, folder=True))
        cl.addWidget(self._slbl(self._tr("cert_lbl_base").upper()))
        cl.addWidget(self._csr_base)

        vb.addWidget(card)
        self._btn_csr = self._action_btn(
            "📋   " + self._tr("cert_btn_gen_csr"), self._do_csr)
        vb.addWidget(self._btn_csr)
        vb.addStretch()
        return pg

    # ── Page: Export PFX ────────────────────────────────
    def _page_pfx(self):
        pg = QWidget(); pg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        vb = QVBoxLayout(pg); vb.setContentsMargins(0,0,0,0); vb.setSpacing(6)

        card = self._panel()
        cl = QVBoxLayout(card); cl.setContentsMargins(12,10,12,12); cl.setSpacing(6)

        self._pfx_cert  = self._le(self._tr("cert_ph_pfx_cert"))
        self._pfx_key   = self._le(self._tr("cert_ph_pfx_key"))
        self._pfx_chain = self._le(self._tr("cert_ph_pfx_chain"))
        self._pfx_out   = self._le(self._tr("cert_ph_out_dir"))
        self._pfx_base  = self._le(self._tr("cert_ph_base"))
        self._pfx_pass  = self._le(self._tr("cert_ph_pass"), pw=True)

        for lbl_key, widget, folder in [
            ("cert_lbl_pfx_cert",  self._pfx_cert,  False),
            ("cert_lbl_pfx_key",   self._pfx_key,   False),
            ("cert_lbl_pfx_chain", self._pfx_chain, False),
            ("cert_lbl_out_dir",   self._pfx_out,   True),
        ]:
            cl.addWidget(self._slbl(self._tr(lbl_key).upper()))
            cl.addLayout(self._row(widget, folder=folder))

        row2 = QHBoxLayout(); row2.setSpacing(10)
        col_b = QVBoxLayout(); col_b.setSpacing(3)
        col_b.addWidget(self._slbl(self._tr("cert_lbl_base").upper()))
        col_b.addWidget(self._pfx_base)
        col_p = QVBoxLayout(); col_p.setSpacing(3)
        col_p.addWidget(self._slbl(self._tr("cert_lbl_pass").upper()))
        col_p.addWidget(self._pfx_pass)
        row2.addLayout(col_b, 1); row2.addLayout(col_p, 1)
        cl.addLayout(row2)

        vb.addWidget(card)
        self._btn_pfx = self._action_btn(
            "📦   " + self._tr("cert_btn_gen_pfx"), self._do_pfx)
        vb.addWidget(self._btn_pfx)
        vb.addStretch()
        return pg

    # ── openssl check ────────────────────────────────────
    @staticmethod
    def _openssl_ok():
        import shutil
        return shutil.which("openssl") is not None

    # ── log helper ───────────────────────────────────────
    def _log_line(self, text):
        self._log.append(text)

    # ── run openssl in thread ────────────────────────────
    def _run_openssl(self, cmd, btn, ok_key, file_list=None):
        btn.setEnabled(False)
        btn.setText(self._tr("cert_running"))
        label_orig = btn.text()

        def _work():
            import subprocess as sp
            try:
                r = sp.run(cmd, capture_output=True, text=True, shell=False)
                return r.returncode, r.stdout, r.stderr
            except FileNotFoundError:
                return -1, "", "openssl not found in PATH"
            except Exception as ex:
                return -1, "", str(ex)

        class _W(QThread):
            done = pyqtSignal(int, str, str)
            def __init__(s, fn): super().__init__(); s._fn = fn
            def run(s): s.done.emit(*s._fn())

        w = _W(_work)
        self._workers.append(w)

        def _on_done(code, out, err):
            if out and out.strip():
                self._log_line("── stdout ──\n" + out.strip())
            if err and err.strip():
                self._log_line("── stderr ──\n" + err.strip())
            if code == 0:
                self._log_line(self._tr(ok_key))
                if file_list:
                    self._log_line(self._tr("cert_files") + "\n".join(f"  📄 {f}" for f in file_list))
            else:
                self._log_line(self._tr("cert_fail", code=code))
            btn.setEnabled(True)
            btn.setText(btn.property("orig_label"))

        btn.setProperty("orig_label", btn.text())
        w.done.connect(_on_done)
        w.start()

    # ── Actions ──────────────────────────────────────────
    def _do_self_signed(self):
        cn     = self._self_cn.text().strip()
        org    = self._self_org.text().strip()
        ou     = self._self_ou.text().strip()
        c      = self._self_c.text().strip() or "XX"
        days   = self._self_days.text().strip() or "365"
        bits   = self._self_key.currentText()
        outdir = self._self_outdir.text().strip()
        base   = self._self_base.text().strip() or "certificate"
        pw     = self._self_pass.text().strip()

        if not cn:     return self._log_line(self._tr("cert_no_cn"))
        if not outdir: return self._log_line(self._tr("cert_no_outdir"))

        os.makedirs(outdir, exist_ok=True)
        subj   = f"/CN={cn}/O={org}/OU={ou}/C={c}"
        key_f  = os.path.join(outdir, base + ".key")
        cer_f  = os.path.join(outdir, base + ".cer")
        pfx_f  = os.path.join(outdir, base + ".pfx") if pw else None

        cmd_cert = [
            "openssl", "req", "-x509", "-newkey", f"rsa:{bits}",
            "-keyout", key_f, "-out", cer_f,
            "-days", days, "-nodes", "-subj", subj
        ]
        self._log_line(f"\n  ╔═  SELF-SIGNED\n  »  {' '.join(cmd_cert)}\n")
        files = [key_f, cer_f]

        if pfx_f:
            files.append(pfx_f)
            # chain two commands via thread sequence
            def _after_cert(code, out, err):
                if code != 0: return
                cmd_pfx = [
                    "openssl", "pkcs12", "-export",
                    "-inkey", key_f, "-in", cer_f,
                    "-out", pfx_f, "-passout", f"pass:{pw}"
                ]
                self._run_openssl(cmd_pfx, self._btn_self, "cert_ok_self", files)

            import subprocess as sp
            class _W2(QThread):
                done2 = pyqtSignal(int, str, str)
                def __init__(s, c): super().__init__(); s._c = c
                def run(s):
                    try:
                        r = sp.run(s._c, capture_output=True, text=True, shell=False)
                        s.done2.emit(r.returncode, r.stdout, r.stderr)
                    except Exception as ex:
                        s.done2.emit(-1, "", str(ex))
            w2 = _W2(cmd_cert)
            self._workers.append(w2)
            self._btn_self.setEnabled(False)
            self._btn_self.setText(self._tr("cert_running"))
            self._btn_self.setProperty("orig_label", "🔐   " + self._tr("cert_btn_gen_self"))
            def _d2(c, o, e):
                if o and o.strip(): self._log_line("── stdout ──\n" + o.strip())
                if e and e.strip(): self._log_line("── stderr ──\n" + e.strip())
                if c == 0: _after_cert(c, o, e)
                else:
                    self._log_line(self._tr("cert_fail", code=c))
                    self._btn_self.setEnabled(True)
                    self._btn_self.setText(self._btn_self.property("orig_label"))
            w2.done2.connect(_d2); w2.start()
        else:
            self._run_openssl(cmd_cert, self._btn_self, "cert_ok_self", files)

    def _do_csr(self):
        cn     = self._csr_cn.text().strip()
        org    = self._csr_org.text().strip()
        ou     = self._csr_ou.text().strip()
        c      = self._csr_c.text().strip() or "XX"
        bits   = self._csr_key.currentText()
        outdir = self._csr_outdir.text().strip()
        base   = self._csr_base.text().strip() or "request"
        exkey  = self._csr_existing_key.text().strip()

        if not cn:     return self._log_line(self._tr("cert_no_cn"))
        if not outdir: return self._log_line(self._tr("cert_no_outdir"))

        os.makedirs(outdir, exist_ok=True)
        subj  = f"/CN={cn}/O={org}/OU={ou}/C={c}"
        csr_f = os.path.join(outdir, base + ".csr")
        key_f = os.path.join(outdir, base + ".key")
        files = [csr_f]

        if exkey:
            cmd = ["openssl", "req", "-new", "-key", exkey, "-out", csr_f, "-subj", subj]
        else:
            cmd = ["openssl", "req", "-new", "-newkey", f"rsa:{bits}",
                   "-keyout", key_f, "-out", csr_f, "-nodes", "-subj", subj]
            files.append(key_f)

        self._log_line(f"\n  ╔═  CSR\n  »  {' '.join(cmd)}\n")
        self._run_openssl(cmd, self._btn_csr, "cert_ok_csr", files)

    def _do_pfx(self):
        cert   = self._pfx_cert.text().strip()
        key    = self._pfx_key.text().strip()
        chain  = self._pfx_chain.text().strip()
        outdir = self._pfx_out.text().strip()
        base   = self._pfx_base.text().strip() or "exported"
        pw     = self._pfx_pass.text().strip()

        if not cert:   return self._log_line(self._tr("cert_no_cert"))
        if not key:    return self._log_line(self._tr("cert_no_key"))
        if not outdir: return self._log_line(self._tr("cert_no_outdir"))

        os.makedirs(outdir, exist_ok=True)
        pfx_f = os.path.join(outdir, base + ".pfx")
        cmd = ["openssl", "pkcs12", "-export",
               "-inkey", key, "-in", cert,
               "-out", pfx_f,
               "-passout", f"pass:{pw}" if pw else "pass:"]
        if chain:
            cmd += ["-certfile", chain]

        self._log_line(f"\n  ╔═  EXPORT PFX\n  »  {' '.join(cmd)}\n")
        self._run_openssl(cmd, self._btn_pfx, "cert_ok_pfx", [pfx_f])

    # ── Theme ─────────────────────────────────────────────
    def _apply_theme(self, theme):
        self._theme = theme
        is_dark = theme == "dark"
        for pn in self._panels:
            pn.set_theme(theme)
        self._tab_bar.set_theme(theme)

        if is_dark:
            title_c  = "#a8d8ff"
            log_c    = "rgba(120,190,255,0.7)"
            x_style  = ("QPushButton{background:rgba(30,60,150,0.3);border:1px solid rgba(80,140,255,0.3);"
                         "border-radius:5px;color:#80b4ff;font-weight:bold;}"
                         "QPushButton:hover{background:rgba(180,40,40,0.5);color:#ffc8c8;border-color:rgba(255,80,80,0.5);}")
            log_bg   = ("QTextEdit{background:rgba(4,10,30,0.65);border:1px solid rgba(50,120,220,0.22);"
                         "border-radius:7px;color:#5aacff;font-family:'Consolas','Courier New',monospace;"
                         "font-size:11px;padding:9px;}")
        else:
            title_c  = "#1a3a80"
            log_c    = "rgba(40,90,180,0.75)"
            x_style  = ("QPushButton{background:rgba(200,215,255,0.5);border:1px solid rgba(80,130,210,0.35);"
                         "border-radius:5px;color:#2040a0;font-weight:bold;}"
                         "QPushButton:hover{background:rgba(220,60,60,0.25);color:#a01010;border-color:rgba(200,50,50,0.5);}")
            log_bg   = ("QTextEdit{background:rgba(240,247,255,0.88);border:1px solid rgba(90,135,215,0.3);"
                         "border-radius:7px;color:#1a3a70;font-family:'Consolas','Courier New',monospace;"
                         "font-size:11px;padding:9px;}")

        self._title_lbl.setStyleSheet(
            f"font-size:15px;font-weight:bold;letter-spacing:2px;background:transparent;color:{title_c};")
        self._log_lbl.setStyleSheet(
            f"font-size:10px;font-weight:bold;letter-spacing:2px;background:transparent;color:{log_c};")
        self._x_btn.setStyleSheet(x_style)
        self._log.setStyleSheet(log_bg)

        # restyle all _slbl labels inside panels
        lbl_color = "rgba(120,190,255,0.7)" if is_dark else "rgba(40,90,180,0.75)"
        for pn in self._panels:
            for child in pn.findChildren(QLabel):
                if child is not self._title_lbl and child is not self._warn_lbl:
                    child.setStyleSheet(
                        f"font-size:10px;font-weight:bold;letter-spacing:2px;"
                        f"background:transparent;color:{lbl_color};")


# ══════════════════════════════════════════════════════════
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
        w, h = r.width(), r.height()
        th = THEMES[self._theme]
        rad = 11

        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, rad, rad)

        # Base fill
        p.fillPath(path, th["panel_accent"] if self.accent else th["panel_fill"])

        # Inner glow at bottom
        ig = QLinearGradient(0, h * 0.6, 0, h)
        ig.setColorAt(0, QColor(0, 0, 0, 0))
        ig.setColorAt(1, th["inner_glow"])
        p.fillPath(path, QBrush(ig))

        # Top gloss — primary (wide)
        gloss1 = QPainterPath()
        gloss1.addRoundedRect(1, 1, w - 2, h * 0.45, rad - 1, rad - 1)
        gg1 = QLinearGradient(0, 0, 0, h * 0.45)
        gg1.setColorAt(0.0, th["gloss"])
        gg1.setColorAt(0.5, th["gloss2"])
        gg1.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(gloss1, QBrush(gg1))

        # Top gloss — secondary narrow bright band
        gloss2 = QPainterPath()
        gloss2.addRoundedRect(2, 1, w - 4, h * 0.12, rad - 2, rad - 2)
        gg2 = QLinearGradient(0, 0, 0, h * 0.12)
        gg2.setColorAt(0, QColor(255, 255, 255, 28 if self._theme == "dark" else 70))
        gg2.setColorAt(1, QColor(255, 255, 255, 0))
        p.fillPath(gloss2, QBrush(gg2))

        # Border gradient
        bg = QLinearGradient(0, 0, 0, h)
        bg.setColorAt(0,   th["border_top"])
        bg.setColorAt(0.4, th["border_mid"])
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
        for i in range(4):
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
        is_dark = self._theme == "dark"

        # Base fill
        p.fillRect(0, 0, w, h, th["bg_base"])

        def orb(cx, cy, rad, rgba, sharp=0.0):
            r, g, b, a = rgba
            gr = QRadialGradient(cx, cy, rad)
            gr.setColorAt(0,          QColor(r, g, b, a))
            if sharp > 0:
                gr.setColorAt(sharp,  QColor(r, g, b, int(a * 0.6)))
            gr.setColorAt(1,          QColor(r // 4, g // 4, b // 4, 0))
            p.setBrush(QBrush(gr))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx - rad), int(cy - rad), rad * 2, rad * 2)

        o = self._off
        # 4 animated orbs — richer palette
        orb(w * .28 + math.sin(math.radians(o * .65)) * 55,
            h * .22 + math.cos(math.radians(o * .50)) * 28, 260, th["orb1"], 0.35)
        orb(w * .78 + math.cos(math.radians(o * .55)) * 45,
            h * .62 + math.sin(math.radians(o * .75)) * 38, 210, th["orb2"], 0.3)
        orb(w * .12 + math.sin(math.radians(o * .38 + 90)) * 38,
            h * .80, 175, th["orb3"], 0.25)
        orb(w * .88 + math.cos(math.radians(o * .45 + 45)) * 30,
            h * .18 + math.sin(math.radians(o * .60)) * 22, 140, th["orb4"])

        # Stars / dust (dark only)
        if is_dark:
            import random; rng = random.Random(42)
            p.setPen(Qt.PenStyle.NoPen)
            for _ in range(55):
                sx = rng.randint(0, w)
                sy = rng.randint(0, h)
                pulse = int(30 + 25 * math.sin(math.radians(o * 2.1 + sx)))
                p.setBrush(QColor(180, 210, 255, pulse))
                sz = rng.choice([1, 1, 1, 2])
                p.drawEllipse(sx, sy, sz, sz)

        # Grid — subtle dots at intersections instead of full lines
        gc = th["grid"]
        pen = QPen(gc); pen.setWidth(1); p.setPen(pen)
        step = 40
        p.setBrush(QColor(gc.red(), gc.green(), gc.blue(), gc.alpha() * 2))
        for x in range(0, w, step):
            for y in range(0, h, step):
                p.drawEllipse(x - 1, y - 1, 2, 2)
        # Faint grid lines (lighter than before)
        pen2 = QPen(QColor(gc.red(), gc.green(), gc.blue(), max(1, gc.alpha() // 2)))
        pen2.setWidth(1)
        p.setPen(pen2)
        p.setBrush(Qt.BrushStyle.NoBrush)
        for x in range(0, w, step): p.drawLine(x, 0, x, h)
        for y in range(0, h, step): p.drawLine(0, y, w, y)

        # Edge glow — subtle inner frame
        if is_dark:
            eg = QPainterPath()
            eg.addRect(0, 0, w, h)
            egp = QPen(QColor(80, 150, 255, 18), 8)
            p.setPen(egp); p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRect(0, 0, w, h)

        # Bottom vignette
        vgn = QLinearGradient(0, h * .55, 0, h)
        vgn.setColorAt(0, QColor(0, 0, 0, 0))
        vgn.setColorAt(1, th["vign"])
        p.setBrush(QBrush(vgn)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(0, int(h * .55), w, h)

        # Top vignette (darker)
        if is_dark:
            tvgn = QLinearGradient(0, 0, 0, h * .18)
            tvgn.setColorAt(0, QColor(0, 0, 8, 80))
            tvgn.setColorAt(1, QColor(0, 0, 0, 0))
            p.setBrush(QBrush(tvgn))
            p.drawRect(0, 0, w, int(h * .18))

        p.end()


# ══════════════════════════════════════════════════════════
#  ABOUT BUTTON  (custom-painted glowing "i" badge)
# ══════════════════════════════════════════════════════════
class _AboutButton(QPushButton):
    def __init__(self, theme="dark", parent=None):
        super().__init__(parent)
        self._theme = theme
        self._hovered = False
        self._pressed = False
        self.setFixedSize(28, 28)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFlat(True)
        self.setStyleSheet("background:transparent;border:none;")

    def set_theme(self, t):
        self._theme = t
        self.update()

    def enterEvent(self, e):
        self._hovered = True; self.update(); super().enterEvent(e)

    def leaveEvent(self, e):
        self._hovered = False; self.update(); super().leaveEvent(e)

    def mousePressEvent(self, e):
        self._pressed = True; self.update(); super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self._pressed = False; self.update(); super().mouseReleaseEvent(e)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        is_dark = self._theme == "dark"

        # Outer glow when hovered
        if self._hovered:
            glow_r = 15
            glow = QRadialGradient(cx, cy, glow_r)
            glow.setColorAt(0, QColor(80, 180, 255, 55) if is_dark else QColor(60, 130, 230, 45))
            glow.setColorAt(1, QColor(0, 0, 0, 0))
            p.setBrush(QBrush(glow))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx - glow_r), int(cy - glow_r), glow_r * 2, glow_r * 2)

        # Circle background with radial gradient
        r = 12
        bg_grad = QRadialGradient(cx - 2, cy - 2, r * 1.4)
        if self._pressed:
            bg_grad.setColorAt(0, QColor(20,  80, 200, 200))
            bg_grad.setColorAt(1, QColor(10,  50, 160, 220))
        elif self._hovered:
            if is_dark:
                bg_grad.setColorAt(0, QColor(60,  160, 255, 190))
                bg_grad.setColorAt(1, QColor(20,   90, 210, 220))
            else:
                bg_grad.setColorAt(0, QColor(80,  150, 255, 200))
                bg_grad.setColorAt(1, QColor(40,  100, 220, 220))
        else:
            if is_dark:
                bg_grad.setColorAt(0, QColor(40,  110, 220, 140))
                bg_grad.setColorAt(1, QColor(15,   60, 180, 170))
            else:
                bg_grad.setColorAt(0, QColor(100, 160, 240, 180))
                bg_grad.setColorAt(1, QColor(60,  110, 210, 200))

        circ = QPainterPath()
        circ.addEllipse(cx - r, cy - r, r * 2, r * 2)
        p.setBrush(QBrush(bg_grad))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPath(circ)

        # Top gloss
        gloss = QPainterPath()
        gloss.addEllipse(cx - r + 2, cy - r + 2, r * 2 - 4, r - 2)
        gg = QLinearGradient(0, cy - r, 0, cy)
        gg.setColorAt(0, QColor(255, 255, 255, 55 if is_dark else 90))
        gg.setColorAt(1, QColor(255, 255, 255, 0))
        p.setBrush(QBrush(gg))
        p.drawPath(gloss)

        # Border ring
        ring_col = (QColor(140, 200, 255, 180 if self._hovered else 100)
                    if is_dark else QColor(80, 140, 230, 190 if self._hovered else 120))
        p.setPen(QPen(ring_col, 1.0))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(int(cx - r), int(cy - r), r * 2, r * 2)

        # "i" glyph — dot + stem
        glyph_col = QColor(220, 240, 255, 240) if is_dark else QColor(255, 255, 255, 240)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(glyph_col)
        p.drawEllipse(int(cx - 1.5), int(cy - 5.5), 3, 3)   # dot
        stem = QPainterPath()
        stem.addRoundedRect(cx - 1.5, cy - 1.5, 3.0, 6.5, 1.2, 1.2)
        p.drawPath(stem)

        p.end()


# ══════════════════════════════════════════════════════════
#  MAIN WINDOW
# ══════════════════════════════════════════════════════════
class SignToolGUI(AeroBackground):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(620, 520)
        self.resize(640, 540)

        # ── Window icon from .ico file ──
        _icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Icon_for_SignTool.ico")
        if os.path.isfile(_icon_path):
            _app_icon = QIcon(_icon_path)
            self.setWindowIcon(_app_icon)
            QApplication.instance().setWindowIcon(_app_icon)

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

        self._title_lbl = QLabel("◈  SignTool")
        self._sub_lbl   = QLabel()
        self._title_lbl.setStyleSheet("color:#a8d8ff;font-size:16px;font-weight:bold;letter-spacing:2px;background:transparent;")
        self._sub_lbl.setStyleSheet("color:rgba(140,190,255,0.5);font-size:10px;letter-spacing:2px;background:transparent;")

        # ── Header icon ──
        _icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Icon_for_SignTool.ico")
        self._icon_lbl = QLabel()
        self._icon_lbl.setStyleSheet("background:transparent;")
        if os.path.isfile(_icon_path):
            self._icon_lbl.setPixmap(QIcon(_icon_path).pixmap(28, 28))

        self.theme_toggle = ThemeToggle()
        self.theme_toggle.set_light(self._theme == "light")
        self.theme_toggle.toggled.connect(self._on_theme)

        self._theme_lbl = QLabel()
        self._theme_lbl.setStyleSheet("color:rgba(140,190,255,0.6);font-size:10px;letter-spacing:1px;background:transparent;")

        self.lang_btn = LangButton()
        self.lang_btn.set_lang(self._lang)
        self.lang_btn.set_theme(self._theme)
        self.lang_btn.toggled.connect(self._on_lang)

        # ── About button ── (custom painted for richer look)
        self.about_btn = _AboutButton(theme=self._theme)
        self.about_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.about_btn.setToolTip("About / O programie")
        self.about_btn.clicked.connect(self._show_about)

        hl.addWidget(self._icon_lbl)
        hl.addWidget(self._title_lbl)
        hl.addStretch()
        hl.addWidget(self._sub_lbl)
        hl.addSpacing(12)
        hl.addWidget(self._theme_lbl)
        hl.addWidget(self.theme_toggle)
        hl.addSpacing(8)
        hl.addWidget(self.lang_btn)
        hl.addSpacing(6)
        hl.addWidget(self.about_btn)
        root.addWidget(hdr)

        # ── Tabs ──
        self.tabs = TabBar()
        self.tabs.set_theme(self._theme)
        self.tabs.tab_changed.connect(self._on_tab_changed)
        root.addWidget(self.tabs)

        # ── Pages ──
        self.stack = QStackedWidget()
        self.stack.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.stack.addWidget(self._page_sign())
        self.stack.addWidget(self._page_verify())
        self.stack.addWidget(self._page_install())
        self.stack.addWidget(self._page_cert_mgr())
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
        self.tabs.set_labels([self.t("tab_sign"), self.t("tab_verify"), self.t("tab_install"), self.t("tab_cert_mgr")])

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

        # Cert manager page
        self._cert_tab_lbl.setText(self.t("cert_tab_page_desc"))
        self._open_cert_btn.setText(self.t("cert_tab_page_btn"))

        # Style refresh
        self._refresh_label_styles(is_light)

    def _on_lang(self, lang):
        self._apply_lang(lang)

    # ──────────────────────────────────────────────────────
    #  ABOUT DIALOG
    # ──────────────────────────────────────────────────────
    def _show_about(self):
        dlg = AboutDialog(self, theme=self._theme, lang=self._lang)
        dlg.exec()

    def _show_cert_mgr(self):
        dlg = CertManagerDialog(self, theme=self._theme, lang=self._lang, tr_fn=self.t)
        dlg.exec()

    def _on_tab_changed(self, idx):
        self.stack.setCurrentIndex(idx)

    # ──────────────────────────────────────────────────────
    #  CERT MANAGER EMBEDDED PAGE (tab 3)
    # ──────────────────────────────────────────────────────
    def _page_cert_mgr(self):
        """Thin wrapper — clicking the tab opens the CertManagerDialog."""
        pg = self._tw()
        vb = QVBoxLayout(pg)
        vb.setContentsMargins(0, 0, 0, 0)
        vb.setSpacing(8)

        card = self._panel()
        cl = QVBoxLayout(card)
        cl.setContentsMargins(14, 20, 14, 20)
        cl.setSpacing(12)

        icon_lbl = QLabel("🔐")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("font-size:36px;background:transparent;")
        cl.addWidget(icon_lbl)

        self._cert_tab_lbl = QLabel()
        self._cert_tab_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._cert_tab_lbl.setWordWrap(True)
        self._cert_tab_lbl.setStyleSheet(
            "font-size:12px;color:rgba(160,200,255,0.75);background:transparent;")
        cl.addWidget(self._cert_tab_lbl)

        self._open_cert_btn = self._action_btn(self._show_cert_mgr)
        vb.addWidget(card)
        vb.addWidget(self._open_cert_btn)
        vb.addStretch()
        return pg

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
        self.about_btn.set_theme(name)
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
