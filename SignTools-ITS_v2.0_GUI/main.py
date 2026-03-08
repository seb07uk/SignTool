#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SignTool's-ITS GUI v2.0 (Microsoft & OpenSSL) - Graficzny interfejs podpisywania kodu i generowania certyfikatow
Obsługuje wszystkie komendy: sign, timestamp, verify, catdb, remove
WERSJA 2.0:
- Auto-wykrywanie signtool.exe i openssl.exe przy starcie (przeszukuje dyski)
- Dialog podsumowania z wynikami wykrywania
- Powiadomienie o brakujących narzędziach z możliwością ręcznego wskazania

──────────────────────────────────────────────────────────────────────────────
 Project Manager : Sebastian Januchowski
 Firma           : polsoft.ITS™ Group
 Kontakt         : polsoft.its@fastservice.com
 GitHub          : https://github.com/seb07uk
 Copyright       : 2026© polsoft.ITS™. All rights reserved.
──────────────────────────────────────────────────────────────────────────────
"""

__author__    = "Sebastian Januchowski"
__company__   = "polsoft.ITS™ Group"
__email__     = "polsoft.its@fastservice.com"
__github__    = "https://github.com/seb07uk"
__copyright__ = "2026© polsoft.ITS™. All rights reserved."
__version__   = "2.0"
__license__   = "Proprietary"

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import sys
import json
from pathlib import Path
import threading
import tempfile
import base64

# ── Wymuszenie UTF-8 (polskie znaki w EXE / Windows) ─────────────────────────
# Bez tego Windows może użyć cp1250/cp852 i zepsuć polskie litery w GUI.
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception as _e:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception as _e:
        pass
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# ── Wbudowany system tłumaczeń PL/EN (bez zewnętrznego pluginu) ──────────────
_LANG = "pl"

_TR = {
    # App / Window
    "app_title":            {"pl": "SignTool's-ITS GUI v2.0 (Microsoft & OpenSSL) - Graficzny interfejs podpisywania i certyfikatow",
                             "en": "SignTool's-ITS GUI v2.0 (Microsoft & OpenSSL) - Code Signing & Certificate GUI"},
    "header_subtitle":      {"pl": "Podpisywanie kodu & Generowanie certyfikatow | v2.0",
                             "en": "Code Signing & Certificate Generation | v2.0"},
    "status_ready":         {"pl": "Gotowy | v2.0",         "en": "Ready | v2.0"},
    "status_ready_ok":      {"pl": "Gotowy - Sukces | v2.0","en": "Ready - Success | v2.0"},
    "status_error":         {"pl": "Blad | v2.0",           "en": "Error | v2.0"},
    "status_running":       {"pl": "Wykonywanie...",        "en": "Running..."},
    "status_cancelled":     {"pl": "Operacja anulowana.",   "en": "Operation cancelled."},

    # Tabs
    "tab_sign":             {"pl": "Sign - Podpisz",        "en": "Sign"},
    "tab_ts_verify":        {"pl": "Timestamp / Verify",    "en": "Timestamp / Verify"},
    "tab_catdb_remove":     {"pl": "CatDB / Remove",        "en": "CatDB / Remove"},
    "tab_batch":            {"pl": "Batch - Wsadowe",       "en": "Batch"},
    "tab_certgen":          {"pl": "\U0001f511 Generuj certyfikat", "en": "\U0001f511 Generate Certificate"},
    "tab_options":          {"pl": "Opcje",                 "en": "Options"},
    "tab_result":           {"pl": "Wynik",                 "en": "Output"},

    # Common
    "btn_add_files":        {"pl": "Dodaj pliki",           "en": "Add files"},
    "btn_remove_selected":  {"pl": "Usun zaznaczone",       "en": "Remove selected"},
    "btn_clear":            {"pl": "Wyczysc",               "en": "Clear"},
    "lbl_files":            {"pl": "Pliki",                 "en": "Files"},
    "lbl_options":          {"pl": "Opcje",                 "en": "Options"},
    "lbl_verbose":          {"pl": "Tryb szczegolowy (/v)", "en": "Verbose mode (/v)"},
    "lbl_rfc3161_only":     {"pl": "(tylko RFC3161)",       "en": "(RFC3161 only)"},

    # Sign tab
    "sign_files_frame":     {"pl": "Pliki do podpisania",   "en": "Files to Sign"},
    "cert_frame":           {"pl": "Certyfikat",            "en": "Certificate"},
    "cert_method_label":    {"pl": "Metoda:",               "en": "Method:"},
    "cert_from_store":      {"pl": "Z magazynu certyfikatow","en": "From certificate store"},
    "cert_from_file":       {"pl": "Z pliku PFX",           "en": "From PFX file"},
    "cert_name_label":      {"pl": "Nazwa certyfikatu (/n):","en": "Certificate name (/n):"},
    "cert_sha1_label":      {"pl": "SHA1 certyfikatu (/sha1):","en": "Certificate SHA1 (/sha1):"},
    "cert_file_label":      {"pl": "Plik certyfikatu (/f):","en": "Certificate file (/f):"},
    "cert_password_label":  {"pl": "Haslo (/p):",           "en": "Password (/p):"},
    "cert_additional_label":{"pl": "Dodatkowy cert (/ac):", "en": "Additional cert (/ac):"},
    "cert_additional_info": {"pl": "\u2139\ufe0f Dodatkowy certyfikat dla cross-certification",
                             "en": "\u2139\ufe0f Additional cert for cross-certification"},
    "sign_options_frame":   {"pl": "Opcje podpisywania",    "en": "Signing Options"},
    "hash_alg_label":       {"pl": "Algorytm hash (/fd):",  "en": "Hash algorithm (/fd):"},
    "desc_label":           {"pl": "Opis (/d):",            "en": "Description (/d):"},
    "url_label":            {"pl": "URL (/du):",            "en": "URL (/du):"},
    "timestamp_server_label":{"pl": "Serwer timestamp:",   "en": "Timestamp server:"},
    "ts_rfc3161":           {"pl": "RFC3161 (/tr) - Nowoczesny","en": "RFC3161 (/tr) - Modern"},
    "ts_authenticode":      {"pl": "Authenticode (/t) - Legacy","en": "Authenticode (/t) - Legacy"},
    "ts_info":              {"pl": "\u2139\ufe0f RFC3161 zalecany, Authenticode dla starszych systemow",
                             "en": "\u2139\ufe0f RFC3161 recommended, Authenticode for legacy systems"},
    "ts_hash_label":        {"pl": "Timestamp hash (/td):", "en": "Timestamp hash (/td):"},
    "sign_append":          {"pl": "Dolacz podpis (/as)",   "en": "Append signature (/as)"},
    "sign_debug":           {"pl": "Debug (/debug)",        "en": "Debug (/debug)"},
    "btn_sign":             {"pl": "\U0001f512 Podpisz",    "en": "\U0001f512 Sign"},
    "btn_show_cmd":         {"pl": "Pokaz komende",         "en": "Show command"},

    # Timestamp / Verify tab
    "ts_frame":             {"pl": "Timestamp",             "en": "Timestamp"},
    "ts_output_frame":      {"pl": "Wynik Timestamp",       "en": "Timestamp Output"},
    "verify_output_frame":  {"pl": "Wynik Verify",          "en": "Verify Output"},
    "ts_server_label":      {"pl": "Serwer:",               "en": "Server:"},
    "ts_hash_short":        {"pl": "Hash (/td):",           "en": "Hash (/td):"},
    "btn_add_timestamp":    {"pl": "Dodaj timestamp",       "en": "Add timestamp"},
    "verify_frame":         {"pl": "Verify",                "en": "Verify"},
    "verify_pa":            {"pl": "Weryfikuj wszystkie podpisy (/pa)","en": "Verify all signatures (/pa)"},
    "verify_pg":            {"pl": "Weryfikuj podpis strony (/pg)","en": "Verify page signature (/pg)"},
    "catalog_label":        {"pl": "Plik katalogu (/c):",   "en": "Catalog file (/c):"},
    "btn_verify":           {"pl": "Weryfikuj",             "en": "Verify"},

    # CatDB / Remove tab
    "catdb_frame":          {"pl": "CatDB",                 "en": "CatDB"},
    "catdb_output_frame":   {"pl": "Wynik CatDB",           "en": "CatDB Output"},
    "remove_output_frame":  {"pl": "Wynik Remove",          "en": "Remove Output"},
    "catdb_desc":           {"pl": "Dodaj/usun pliki katalogu z bazy katalogów systemu.",
                             "en": "Add/remove catalog files from the catalog database."},
    "catdb_file_label":     {"pl": "Plik katalogu:",        "en": "Catalog file:"},
    "catdb_action_label":   {"pl": "Akcja:",                "en": "Action:"},
    "btn_exec_catdb":       {"pl": "Wykonaj CatDB",         "en": "Execute CatDB"},
    "remove_frame":         {"pl": "Remove - Usun podpisy", "en": "Remove - Strip Signatures"},
    "remove_sig_cb":        {"pl": "Usun podpisy Authenticode (/s) - wymagane",
                             "en": "Remove Authenticode signatures (/s) - required"},
    "remove_sig_info":      {"pl": "\u2139\ufe0f signtool remove zawsze wymaga flagi /s",
                             "en": "\u2139\ufe0f signtool remove always requires the /s flag"},
    "btn_remove_sigs":      {"pl": "Usun podpisy",          "en": "Remove signatures"},

    # Batch tab
    "batch_info_frame":     {"pl": "Info",                  "en": "Info"},
    "batch_editor_frame":   {"pl": "Plik odpowiedzi",       "en": "Response File"},
    "btn_load_file":        {"pl": "Wczytaj plik",          "en": "Load file"},
    "btn_save_file":        {"pl": "Zapisz plik",           "en": "Save file"},
    "btn_exec_batch":       {"pl": "Wykonaj plik odpowiedzi","en": "Execute response file"},

    # CertGen tab
    "certgen_method_frame": {"pl": "Metoda generowania",    "en": "Generation method"},
    "certgen_ossl":         {"pl": "OpenSSL  (cross-platform, zalecany)",
                             "en": "OpenSSL  (cross-platform, recommended)"},
    "certgen_ps":           {"pl": "PowerShell  New-SelfSignedCertificate  (tylko Windows, eksport do PFX)",
                             "en": "PowerShell  New-SelfSignedCertificate  (Windows only, exports to PFX)"},
    "certgen_ossl_path":    {"pl": "Sciezka openssl:",      "en": "OpenSSL path:"},
    "certgen_type_frame":   {"pl": "Typ certyfikatu",       "en": "Certificate type"},
    "certgen_self":         {"pl": "Self-signed  (samopodpisany, do testow)",
                             "en": "Self-signed  (for testing)"},
    "certgen_ca":           {"pl": "Root CA  (urzad certyfikacji)",
                             "en": "Root CA  (certification authority)"},
    "certgen_signed":       {"pl": "Podpisany przez CA  (wymaga Root CA)",
                             "en": "Signed by CA  (requires Root CA)"},
    "certgen_subj_frame":   {"pl": "Dane certyfikatu (Subject)",
                             "en": "Certificate data (Subject)"},
    "certgen_crypto_frame": {"pl": "Parametry kryptograficzne",
                             "en": "Cryptographic parameters"},
    "certgen_key_alg":      {"pl": "Algorytm klucza:",      "en": "Key algorithm:"},
    "certgen_key_size":     {"pl": "Rozmiar klucza RSA:",   "en": "RSA key size:"},
    "certgen_ec_curve":     {"pl": "Krzywa EC:",            "en": "EC curve:"},
    "certgen_hash_alg":     {"pl": "Algorytm hash (sig):",  "en": "Hash algorithm (sig):"},
    "certgen_validity":     {"pl": "Waznosc (dni):",        "en": "Validity (days):"},
    "certgen_san_frame":    {"pl": "Subject Alternative Names (SAN) - opcjonalne",
                             "en": "Subject Alternative Names (SAN) - optional"},
    "certgen_dns":          {"pl": "DNS names:",            "en": "DNS names:"},
    "certgen_dns_hint":     {"pl": "(jedna na linie, np. localhost)",
                             "en": "(one per line, e.g. localhost)"},
    "certgen_ip":           {"pl": "IP addresses:",         "en": "IP addresses:"},
    "certgen_ip_hint":      {"pl": "(jedna na linie, np. 127.0.0.1)",
                             "en": "(one per line, e.g. 127.0.0.1)"},
    "certgen_ca_frame":     {"pl": "Certyfikat CA (tylko dla trybu Podpisany przez CA)",
                             "en": "CA Certificate (only for Signed by CA mode)"},
    "certgen_ca_cert":      {"pl": "Plik CA cert (.crt/.pem):",
                             "en": "CA cert file (.crt/.pem):"},
    "certgen_ca_key":       {"pl": "Plik CA klucza (.key/.pem):",
                             "en": "CA key file (.key/.pem):"},
    "certgen_ca_pass":      {"pl": "Haslo klucza CA:",      "en": "CA key password:"},
    "certgen_out_frame":    {"pl": "Pliki wyjsciowe",       "en": "Output files"},
    "certgen_out_dir":      {"pl": "Folder wyjsciowy:",     "en": "Output folder:"},
    "certgen_base_name":    {"pl": "Nazwa bazowa plikow:",  "en": "Base file name:"},
    "certgen_pfx_pass":     {"pl": "Haslo do PFX:",         "en": "PFX password:"},
    "certgen_pfx_hint":     {"pl": "(puste = brak hasla)",  "en": "(empty = no password)"},
    "certgen_export_pfx":   {"pl": "Eksportuj PFX (klucz + certyfikat razem)",
                             "en": "Export PFX (key + certificate together)"},
    "certgen_install":      {"pl": "Zainstaluj certyfikat w magazynie Windows (wymaga uprawnien admina)",
                             "en": "Install certificate in Windows store (requires admin)"},
    "btn_generate":         {"pl": "Generuj certyfikat",    "en": "Generate certificate"},
    "btn_show_cmds":        {"pl": "Pokaz komendy",         "en": "Show commands"},
    "certgen_success_status":{"pl": "Gotowy - Certyfikat wygenerowany | v2.0",
                              "en": "Ready - Certificate generated | v2.0"},
    "certgen_error_status": {"pl": "Blad generowania certyfikatu | v2.0",
                             "en": "Certificate generation error | v2.0"},

    # Dialogs
    "dlg_select_files":     {"pl": "Wybierz pliki",         "en": "Select files"},
    "dlg_select_cert":      {"pl": "Wybierz certyfikat PFX","en": "Select PFX certificate"},
    "dlg_select_catalog":   {"pl": "Wybierz plik katalogu", "en": "Select catalog file"},
    "dlg_select_folder":    {"pl": "Wybierz folder",        "en": "Select folder"},
    "dlg_all_files":        {"pl": "Wszystkie pliki",       "en": "All files"},
    "dlg_cert_files":       {"pl": "Pliki certyfikatow",    "en": "Certificate files"},
    "dlg_cat_files":        {"pl": "Pliki katalogu",        "en": "Catalog files"},
    "dlg_text_files":       {"pl": "Pliki tekstowe",        "en": "Text files"},
    "dlg_response_files":   {"pl": "Wczytaj plik odpowiedzi","en": "Load response file"},
    "dlg_save_response":    {"pl": "Zapisz plik odpowiedzi","en": "Save response file"},

    # Messages
    "msg_select_cert":      {"pl": "Wybierz certyfikat i pliki do podpisania.",
                             "en": "Please select a certificate and files to sign."},
    "msg_select_ts":        {"pl": "Wybierz pliki do opatrzenia znacznikiem czasu.",
                             "en": "Please select files for timestamping."},
    "msg_select_verify":    {"pl": "Wybierz pliki do weryfikacji.",
                             "en": "Please select files to verify."},
    "msg_select_catdb":     {"pl": "Wybierz plik katalogu.",
                             "en": "Please select a catalog file."},
    "msg_select_remove":    {"pl": "Wybierz pliki do usuniecia podpisow.",
                             "en": "Please select files to remove signatures from."},
    "msg_batch_empty":      {"pl": "Edytor jest pusty.",    "en": "Editor is empty."},
    "msg_error":            {"pl": "Blad",                  "en": "Error"},
    "msg_success":          {"pl": "Sukces",                "en": "Success"},
    "msg_file_saved":       {"pl": "Plik zapisany.",        "en": "File saved."},
    "msg_load_fail":        {"pl": "Nie mozna wczytac pliku: {e}",
                             "en": "Cannot load file: {e}"},
    "msg_save_fail":        {"pl": "Nie mozna zapisac pliku: {e}",
                             "en": "Cannot save file: {e}"},
    "msg_no_openssl":       {"pl": "Nie znaleziono openssl.exe",
                             "en": "openssl.exe not found"},
    "msg_fill_fields":      {"pl": "Wypelnij wymagane pola (CN, folder wyjsciowy, nazwa pliku).",
                             "en": "Please fill required fields (CN, output folder, file name)."},

    # Output headers
    "out_cmd_header":       {"pl": "\n--- Wygenerowana komenda ---\n",
                             "en": "\n--- Generated command ---\n"},
    "out_cmd_footer":       {"pl": "----------------------------\n",
                             "en": "----------------------------\n"},

    # Language switcher
    "lang_label":           {"pl": "Jezyk / Language:",     "en": "Jezyk / Language:"},
    "lang_switched":        {"pl": "Jezyk zmieniony na: Polski",
                             "en": "Language changed to: English"},

    # Batch info text
    "batch_info_text":      {"pl": "Tryb wsadowy: jeden argument na linie, pierwsza linia to komenda.\n"
                                   "Przyklad:  sign  /n \"Moj Cert\"  /fd SHA256  plik.exe",
                             "en": "Batch mode: one argument per line, first line is the command.\n"
                                   "Example:  sign  /n \"My Cert\"  /fd SHA256  file.exe"},

    # CertGen subject field labels
    "certgen_lbl_cn":       {"pl": "Nazwa (CN):",           "en": "Name (CN):"},
    "certgen_lbl_org":      {"pl": "Organizacja (O):",      "en": "Organization (O):"},
    "certgen_lbl_country":  {"pl": "Kraj (C, 2 litery):",   "en": "Country (C, 2 chars):"},
    "certgen_lbl_city":     {"pl": "Miejscowosc (L):",      "en": "City (L):"},
    "certgen_lbl_state":    {"pl": "Wojewodztwo (ST):",     "en": "State (ST):"},
    "certgen_lbl_email":    {"pl": "E-mail:",               "en": "E-mail:"},

    # Detection dialog
    "detect_searching":     {"pl": "Szukam narzedzi...",    "en": "Searching for tools..."},
    "detect_title":         {"pl": "Automatyczne wykrywanie narzedzi",
                             "en": "Automatic tool detection results"},
    "detect_cancel":        {"pl": "Anuluj",                "en": "Cancel"},
    "detect_apply":         {"pl": "Zastosuj i zamknij",    "en": "Apply and close"},
    "detect_close":         {"pl": "Zamknij",               "en": "Close"},
    "detect_retry":         {"pl": "\U0001f504 Skanuj ponownie", "en": "\U0001f504 Retry scan"},
    "detect_all_ok":        {"pl": "\u2705  Wszystkie narzedzia wykryte pomyslnie.",
                             "en": "\u2705  All tools detected successfully."},
    # ── Brakujące klucze – certgen / validation ──────────────────────────────
    "certgen_gen_status":      {"pl": "Generowanie certyfikatu (OpenSSL)...", "en": "Generating certificate (OpenSSL)..."},
    "certgen_gen_ps_status":   {"pl": "Generowanie certyfikatu (PowerShell)...", "en": "Generating certificate (PowerShell)..."},
    "msg_no_cert":             {"pl": "Brak certyfikatu",        "en": "No certificate"},
    "msg_no_cert_body":        {"pl": "Nie podano certyfikatu. Kontynuowac bez certyfikatu?",
                                "en": "No certificate provided. Continue without a certificate?"},
    "msg_no_cn":               {"pl": "Pole Nazwa (CN) jest wymagane.",
                                "en": "The Name (CN) field is required."},
    "msg_no_outdir":           {"pl": "Brak katalogu wyjsciowego",
                                "en": "Missing output directory"},
    "msg_outdir_missing":      {"pl": "Podany katalog wyjsciowy nie istnieje. Wybierz istniejacy folder.",
                                "en": "The specified output directory does not exist. Please select an existing folder."},

    # ── Tooltip keys (49 unikalnych) ─────────────────────────────────────────
    "tip_sign_files":          {"pl": "Kliknij 'Dodaj pliki', aby wybrac pliki do podpisania (EXE, DLL, SYS, MSI, CAT, PS1...)",
                                "en": "Click 'Add files' to select files to sign (EXE, DLL, SYS, MSI, CAT, PS1...)"},
    "tip_sign_cert_store":     {"pl": "Podpisz uzywajac certyfikatu z magazynu Windows",
                                "en": "Sign using a certificate from the Windows certificate store"},
    "tip_sign_cert_name":      {"pl": "Czesc nazwy certyfikatu do wyszukania w magazynie Windows (/n)",
                                "en": "Substring of the certificate name to search in the Windows store (/n)"},
    "tip_sign_cert_sha1":      {"pl": "Pelny odcisk SHA1 (40 znakow hex) certyfikatu w magazynie Windows (/sha1)",
                                "en": "Full SHA1 thumbprint (40 hex chars) of the certificate in the Windows store (/sha1)"},
    "tip_sign_pfx_file":       {"pl": "Sciezka do pliku certyfikatu PFX na dysku (/f)",
                                "en": "Path to the PFX certificate file on disk (/f)"},
    "tip_sign_pfx_pass":       {"pl": "Haslo do pliku PFX (/p). Nigdy nie jest zapisywane na dysk.",
                                "en": "Password for the PFX file (/p). Never saved to disk."},
    "tip_sign_cert_file":      {"pl": "Sciezka do pliku certyfikatu (/f)",
                                "en": "Path to the certificate file (/f)"},
    "tip_sign_addl_cert":      {"pl": "Dodatkowy certyfikat do cross-certyfikacji (/ac)",
                                "en": "Additional certificate for cross-certification (/ac)"},
    "tip_sign_hash":           {"pl": "Algorytm skrotu dla podpisu pliku (/fd). Zalecane: SHA256",
                                "en": "File digest hash algorithm (/fd). Recommended: SHA256"},
    "tip_sign_desc":           {"pl": "Opis osadzany w podpisie cyfrowym (/d)",
                                "en": "Description embedded in the digital signature (/d)"},
    "tip_sign_url":            {"pl": "URL osadzany w podpisie (Authenticode URL opisu) (/du)",
                                "en": "URL embedded in the signature (Authenticode description URL) (/du)"},
    "tip_sign_ts_server":      {"pl": "Adres serwera znacznika czasu (TSA). Np. http://timestamp.digicert.com",
                                "en": "Timestamp Authority (TSA) server URL. E.g. http://timestamp.digicert.com"},
    "tip_sign_ts_rfc3161":     {"pl": "Protokol RFC 3161 (zalecany) – nowoczesny, obsluguje SHA-256 (/tr)",
                                "en": "RFC 3161 protocol (recommended) – modern, supports SHA-256 (/tr)"},
    "tip_sign_ts_auth":        {"pl": "Protokol Authenticode (legacy) – kompatybilny z WinXP (/t)",
                                "en": "Authenticode protocol (legacy) – compatible with WinXP (/t)"},
    "tip_sign_ts_hash":        {"pl": "Algorytm skrotu znacznika czasu (tylko RFC 3161) (/td)",
                                "en": "Timestamp hash algorithm (RFC 3161 only) (/td)"},
    "tip_sign_append":         {"pl": "Dodaj drugi podpis bez usuwania istniejacego (dual-signing) (/as)",
                                "en": "Append a second signature without removing the existing one (dual-signing) (/as)"},
    "tip_sign_verbose":        {"pl": "Tryb szczegolowy – drukuje dodatkowe informacje o podpisywaniu (/v)",
                                "en": "Verbose mode – prints additional signing information (/v)"},
    "tip_sign_debug":          {"pl": "Tryb diagnostyczny – drukuje informacje debugowania (/debug)",
                                "en": "Debug mode – prints debugging information (/debug)"},
    "tip_btn_sign":            {"pl": "Uruchom signtool sign z aktualnymi ustawieniami",
                                "en": "Execute signtool sign with the current settings"},
    "tip_btn_show_cmd":        {"pl": "Pokaz pelne polecenie w oknie wyniku bez uruchamiania",
                                "en": "Show the full command in the output pane without executing"},
    "tip_ts_server":           {"pl": "Adres serwera TSA dla operacji znacznikowania czasu",
                                "en": "TSA server URL for the timestamping operation"},
    "tip_ts_hash":             {"pl": "Algorytm skrotu znacznika czasu (tylko RFC 3161)",
                                "en": "Timestamp hash algorithm (RFC 3161 only)"},
    "tip_verify_pa":           {"pl": "Weryfikuj uzywajac domyslnej polityki uwierzytelniania (/pa)",
                                "en": "Verify using the default authentication policy (/pa)"},
    "tip_verify_pg":           {"pl": "Weryfikuj skrot strony osadzony w podpisie (/pg)",
                                "en": "Verify the page hash embedded in the signature (/pg)"},
    "tip_verify_catalog":      {"pl": "Plik katalogu .cat do weryfikacji wzglem (/c)",
                                "en": "Catalog .cat file to verify against (/c)"},
    "tip_catdb_file":          {"pl": "Sciezka do pliku katalogu .cat",
                                "en": "Path to the .cat catalog file"},
    "tip_catdb_action":        {"pl": "Dodaj (/u) lub usun (/r) katalog z bazy katalogow Windows",
                                "en": "Add (/u) or remove (/r) the catalog from the Windows catalog database"},
    "tip_remove_files":        {"pl": "Pliki, z ktorych zostana usuniete podpisy Authenticode",
                                "en": "Files from which Authenticode signatures will be removed"},
    "tip_batch_editor":        {"pl": "Edytor pliku odpowiedzi – jeden argument signtool na wiersz",
                                "en": "Response file editor – one signtool argument per line"},
    "tip_batch_exec":          {"pl": "Uruchom signtool z zawartoscia edytora jako plik odpowiedzi (@file)",
                                "en": "Execute signtool with the editor content as a response file (@file)"},
    "tip_certgen_type_self":   {"pl": "Certyfikat samopodpisany – do testow i srodowisk deweloperskich",
                                "en": "Self-signed certificate – for testing and development environments"},
    "tip_certgen_type_ca":     {"pl": "Certyfikat Root CA – kotwica zaufania wewnetrznej hierarchii PKI",
                                "en": "Root CA certificate – trust anchor of an internal PKI hierarchy"},
    "tip_certgen_type_signed": {"pl": "Certyfikat podpisany przez CA – wymaga podania pliku cert i klucza CA",
                                "en": "CA-signed certificate – requires CA certificate and key files"},
    "tip_certgen_openssl":     {"pl": "Sciezka do pliku openssl.exe uzytego do generowania certyfikatu",
                                "en": "Path to openssl.exe used for certificate generation"},
    "tip_certgen_key_alg":     {"pl": "Algorytm klucza: RSA (universlana kompatybilnosc) lub EC (mniejszy klucz)",
                                "en": "Key algorithm: RSA (universal compatibility) or EC (smaller key)"},
    "tip_certgen_key_size":    {"pl": "Rozmiar klucza RSA w bitach. Minimum zalecane: 2048",
                                "en": "RSA key size in bits. Minimum recommended: 2048"},
    "tip_certgen_ec_curve":    {"pl": "Krzywa eliptyczna dla klucza EC (NIST P-256/P-384/P-521)",
                                "en": "Elliptic curve for the EC key (NIST P-256/P-384/P-521)"},
    "tip_certgen_hash":        {"pl": "Algorytm skrotu dla podpisu certyfikatu. Zalecane: sha256",
                                "en": "Hash algorithm for the certificate signature. Recommended: sha256"},
    "tip_certgen_days":        {"pl": "Okres waznosci certyfikatu w dniach",
                                "en": "Certificate validity period in days"},
    "tip_certgen_san_dns":     {"pl": "Nazwy DNS dla rozszerzenia SAN – jedna na wiersz (np. localhost)",
                                "en": "DNS names for the SAN extension – one per line (e.g. localhost)"},
    "tip_certgen_san_ip":      {"pl": "Adresy IP dla rozszerzenia SAN – jeden na wiersz (np. 127.0.0.1)",
                                "en": "IP addresses for the SAN extension – one per line (e.g. 127.0.0.1)"},
    "tip_certgen_pfx_pass":    {"pl": "Haslo do eksportowanego pliku PFX (puste = brak hasla). Nie jest zapisywane.",
                                "en": "Password for the exported PFX file (empty = no password). Never saved."},
    "tip_certgen_export_pfx":  {"pl": "Eksportuj wygenerowany certyfikat i klucz do pliku PFX (PKCS#12)",
                                "en": "Export the generated certificate and key to a PFX (PKCS#12) file"},
    "tip_certgen_install":     {"pl": "Zainstaluj certyfikat PFX w magazynie Cert:\\CurrentUser\\My (wymaga PowerShell)",
                                "en": "Install the PFX certificate into Cert:\\CurrentUser\\My store (requires PowerShell)"},
    "tip_certgen_generate":    {"pl": "Uruchom generowanie certyfikatu z aktualnymi ustawieniami",
                                "en": "Execute certificate generation with the current settings"},
    "tip_stop_btn":            {"pl": "Zatrzymaj aktualnie wykonywana operacje (kill procesu)",
                                "en": "Stop the currently running operation (kill the process)"},
    "tip_lang_btn":            {"pl": "Przelacz jezyk interfejsu (PL/EN) – bez restartu",
                                "en": "Switch UI language (PL/EN) – no restart required"},
    "tip_led_signtool":        {"pl": "Wskaznik dostepnosci signtool.exe (zielony = znaleziony)",
                                "en": "signtool.exe availability indicator (green = found)"},
    "tip_led_openssl":         {"pl": "Wskaznik dostepnosci openssl.exe (zielony = znaleziony)",
                                "en": "openssl.exe availability indicator (green = found)"},
}


def t(key: str, **kwargs) -> str:
    entry = _TR.get(key)
    if entry is None:
        return key
    text = entry.get(_LANG, entry.get("pl", key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception as _e:
            pass
    return text


def set_language(lang: str):
    global _LANG
    if lang in ("pl", "en"):
        _LANG = lang


def get_language() -> str:
    return _LANG

# Ikona aplikacji zakodowana w base64 (osadzona w skrypcie)

def _get_app_dir():
    """Folder obok uruchomionego exe / skryptu (priorytet dla narzędzi i zasobów)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

APP_TOOLS_DIR = _get_app_dir()   # folder ze skryptem / exe

def _asset_path(filename):
    """
    Ścieżka do zasobu:
      1. Folder obok exe / main.py  (umożliwia podmianę bez przebudowy)
      2. Folder _MEIPASS (PyInstaller – zasoby bundlowane w exe)
    """
    # 1) Obok exe / skryptu
    candidate = os.path.join(APP_TOOLS_DIR, filename)
    if os.path.isfile(candidate):
        return candidate
    # 2) Zasoby wyekstrahowane przez PyInstaller
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidate = os.path.join(meipass, filename)
        if os.path.isfile(candidate):
            return candidate
    # Fallback – zwróć ścieżkę w APP_TOOLS_DIR (do zapisu lub przy starcie)
    return os.path.join(APP_TOOLS_DIR, filename)

ICON_PATH = _asset_path("SignTool-ico.ico")
LOGO_PATH = _asset_path("logo.png")


# ── Katalogi aplikacji PolSoft ───────────────────────────────────────────────
APP_DIR   = os.path.join(os.path.expanduser("~"), ".polsoft", "software", "SignToolGUI")
CERT_DIR  = os.path.join(APP_DIR, "Certificates")
CONFIG_FILE = os.path.join(APP_DIR, "SignToolGUI.json")

def _ensure_app_dirs():
    """Utwórz strukturę katalogów aplikacji jeśli nie istnieje"""
    for d in (APP_DIR, CERT_DIR):
        os.makedirs(d, exist_ok=True)

_ensure_app_dirs()


# ── Grafika osadzona w base64 (nie wymaga plików zewnętrznych) ────────────────
_ICON_B64 = (
    "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"
    "jIqZbga5G/byJbkYovDJKn4ihSHcDpolqRiKljYzIvouuXIou/OoeKtQ9Vej5q9BPTAI9eAgNIKD"
    "0BmuQ2eo1jyGa8Vrl3htfz0IjUABdX8lat4KVD15VFzlSLkNMu1yIxJhLOUl2UJMJrg1hABbqdo0"
    "KFlGCHIEJfLBlYC5jq4G/13SQidlLXhc1oN7VC20RXWFH1aM0E0UpCXhdgYzEwLx6kqfLx1pWLyY"
    "c+mZvywaGhrc3mQyRlZEOF5o9IfLOz3BzDxPKHO17k/fqPmSy8iikJypZyRXokd1pbbK7tRuxZU+"
    "rLiTRyU9/jFZGZKRPCUZsdOSkfqD5KSNKKgwipQFKQ7KfyCFUTpoCY8sEjrSIMskagr1gKCnRD9L"
    "yshIFB1a5LRDi33m0KKnJC36sawljsuuyC8VI3ZI1qKvy3r4JckZeV73xh/T3LEfap747bo7eoPq"
    "jl1rBOKLdXdwumEEOnyxbJMvkh/k9aaitDIz8P/CMMx/wo29vSq5H4FsNuTwpSOUlBJM5nPh5OC6"
    "QKp2lC+UG+/0lrc4vck2akRhGOEpihGbqruj0xR3tFvRaQS7dXe0W/dFKWlqKr2vGKEuxR2bohiB"
    "dsUITHSGylt88UKjO1rV4AlVDTYCubzbHU15PPGE358Jhwtj/bm2+U7qsj3wGhmGYRiGYRiGYRiG"
    "YRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiG"
    "YRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiGYRiG"
    "YRiGYRiGYRiGYRiGYRiGYRiGYRiGYf5H+A+CG/5THIkQ9wAAAABJRU5ErkJggg=="
)
_LOGO_B64 = (
    "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"
)


def _safe_unlink(path):
    """Bezpiecznie usuń plik (ignoruje błędy)."""
    try:
        os.unlink(path)
    except Exception as _e:
        pass


class Tooltip:
    """
    Chmurka z podpowiedzią wyświetlana po 2 sekundach od najechania kursorem.
    Obsługuje tekst wieloliniowy i automatycznie chowa się przy opuszczeniu widgetu.
    """
    _BG       = "#fffbe6"
    _FG       = "#1a1a1a"
    _BORDER   = "#c8a800"
    _FONT     = ("Segoe UI", 9)
    _DELAY    = 2000   # ms

    def __init__(self, widget, text_or_func, delay=_DELAY):
        """
        widget       – Tkinter widget, do którego przypiąć tooltip
        text_or_func – str lub callable() → str (dla dynamicznych tekstów i18n)
        delay        – opóźnienie w ms (domyślnie 2000 = 2s)
        """
        self._widget     = widget
        self._source     = text_or_func
        self._delay      = delay
        self._after_id   = None
        self._tip_win    = None

        widget.bind("<Enter>",       self._on_enter,   add="+")
        widget.bind("<Leave>",       self._on_leave,   add="+")
        widget.bind("<ButtonPress>", self._on_leave,   add="+")
        widget.bind("<Destroy>",     self._on_destroy, add="+")

    # ── internals ──────────────────────────────────────────────────────────
    def _text(self):
        return self._source() if callable(self._source) else self._source

    def _on_enter(self, event=None):
        self._cancel()
        self._after_id = self._widget.after(self._delay, self._show)

    def _on_leave(self, event=None):
        self._cancel()
        self._hide()

    def _on_destroy(self, event=None):
        self._cancel()
        self._hide()

    def _cancel(self):
        if self._after_id is not None:
            try:
                self._widget.after_cancel(self._after_id)
            except Exception as _e:
                pass
            self._after_id = None

    def _show(self):
        text = self._text()
        if not text:
            return
        self._hide()

        # Pozycja: tuż pod lewym dolnym rogiem widgetu
        try:
            wx = self._widget.winfo_rootx()
            wy = self._widget.winfo_rooty()
            wh = self._widget.winfo_height()
        except Exception as _e:
            return

        tw = tk.Toplevel(self._widget)
        tw.wm_overrideredirect(True)          # brak ramki systemowej
        tw.wm_attributes("-topmost", True)
        tw.configure(bg=self._BORDER)

        # Ramka wewnętrzna (obramowanie przez padding)
        inner = tk.Frame(tw, bg=self._BG, padx=1, pady=1)
        inner.pack(padx=1, pady=1)

        lbl = tk.Label(
            inner, text=text,
            bg=self._BG, fg=self._FG,
            font=self._FONT,
            justify=tk.LEFT,
            padx=8, pady=5,
            wraplength=340,
        )
        lbl.pack()

        tw.update_idletasks()
        tw_w = tw.winfo_reqwidth()
        tw_h = tw.winfo_reqheight()

        # Sprawdź czy zmieści się pod widgetem, jeśli nie – pokaż nad nim
        screen_h = tw.winfo_screenheight()
        y = wy + wh + 4
        if y + tw_h > screen_h - 8:
            y = wy - tw_h - 4

        x = wx
        screen_w = tw.winfo_screenwidth()
        if x + tw_w > screen_w - 8:
            x = screen_w - tw_w - 8

        tw.wm_geometry(f"+{x}+{y}")
        self._tip_win = tw

    def _hide(self):
        if self._tip_win is not None:
            try:
                self._tip_win.destroy()
            except Exception as _e:
                pass
            self._tip_win = None


class SignToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SignTool's-ITS GUI v2.0 (Microsoft & OpenSSL)")
        self._apply_icon()
        # Wczytaj konfigurację (rozmiar okna, lock)
        self.config = self._load_config()
        w = self.config.get("width", 720)
        h = self.config.get("height", 807)
        self.root.geometry("720x807")
        self.root.resizable(False, False)

        # Rejestry widgetow do aktualizacji przy zmianie jezyka
        # (widget, klucz_tlumaczenia)
        self._lang_widgets = []   # Button, Label, Checkbutton, Radiobutton
        self._lang_frames  = []   # LabelFrame
        self._lang_tabs    = []   # (notebook, index, klucz)

        # Ustaw język z konfiguracji (domyślnie pl)
        saved_lang = self.config.get("language", "pl")
        set_language(saved_lang)
        self.root.title(t("app_title"))
        
        # Sprawdź czy signtool jest dostępny
        self.signtool_path = self.find_signtool()
        
        # Nagłówek z logo i tytułem
        self._build_header(root)

        # Główny notebook (zakładki)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Zakładki dla każdej komendy
        self.create_sign_tab()
        self.create_timestamp_verify_tab()
        self.create_catdb_remove_tab()
        self.create_batch_tab()
        self.create_certgen_tab()
        
        # Pasek statusu z przyciskiem lock
        status_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_bar = tk.Label(status_frame, text=t("status_ready"), anchor=tk.W)
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # ── Przycisk Stop ──
        self._stop_btn = tk.Button(
            status_frame,
            text="■ Stop",
            font=("TkDefaultFont", 7, "bold"),
            relief=tk.FLAT,
            bd=1,
            padx=4,
            pady=0,
            fg="#cc0000",
            cursor="hand2",
            command=self.stop_current_process,
        )
        self._stop_btn.pack(side=tk.LEFT, padx=(2, 6), pady=2)
        self._tip(self._stop_btn, "tip_stop_btn")


        # Separator
        tk.Frame(status_frame, width=1, bg="#aaaaaa").pack(side=tk.RIGHT, fill=tk.Y, padx=4, pady=2)

        # ── Przycisk PL/EN w status barze (prawy dolny róg) ──────────────────
        current_lang = get_language()
        self._lang_btn = tk.Button(
            status_frame,
            text="EN" if current_lang == "pl" else "PL",
            font=("TkDefaultFont", 7, "bold"),
            relief=tk.FLAT,
            bd=1,
            padx=6,
            pady=0,
            fg="#0a1a2e",
            bg="#c8dff0",
            activeforeground="#ffffff",
            activebackground="#1a3a5e",
            cursor="hand2",
            command=self._switch_language,
        )
        self._lang_btn.pack(side=tk.RIGHT, padx=(0, 2), pady=2)
        self._tip(self._lang_btn, "tip_lang_btn")

        # Separator przed przyciskiem języka
        tk.Frame(status_frame, width=1, bg="#aaaaaa").pack(side=tk.RIGHT, fill=tk.Y, padx=4, pady=2)

        # ── Wskazniki LED: openssl ──
        self._led_openssl_canvas = tk.Canvas(
            status_frame, width=12, height=12,
            bd=0, highlightthickness=0, bg=status_frame.cget("bg"))
        self._led_openssl_canvas.pack(side=tk.RIGHT, padx=(0, 1), pady=3)
        self._led_openssl_id = self._led_openssl_canvas.create_oval(
            1, 1, 11, 11, fill="#cc0000", outline="#880000")
        _openssl_lbl = tk.Label(status_frame, text="openssl",
                 font=("TkDefaultFont", 7))
        _openssl_lbl.pack(side=tk.RIGHT, padx=(4, 0))
        self._tip(self._led_openssl_canvas, "tip_led_openssl")
        self._tip(_openssl_lbl, "tip_led_openssl")

        # ── Wskazniki LED: signtool ──
        self._led_signtool_canvas = tk.Canvas(
            status_frame, width=12, height=12,
            bd=0, highlightthickness=0, bg=status_frame.cget("bg"))
        self._led_signtool_canvas.pack(side=tk.RIGHT, padx=(0, 1), pady=3)
        self._led_signtool_id = self._led_signtool_canvas.create_oval(
            1, 1, 11, 11, fill="#cc0000", outline="#880000")
        _signtool_lbl = tk.Label(status_frame, text="signtool",
                 font=("TkDefaultFont", 7))
        _signtool_lbl.pack(side=tk.RIGHT, padx=(8, 0))
        self._tip(self._led_signtool_canvas, "tip_led_signtool")
        self._tip(_signtool_lbl, "tip_led_signtool")
        
        # Auto-wykrywanie narzędzi po zaladowaniu UI
        self.root.after(200, self._auto_detect_tools)

        # Przywroc ostatnie ustawienia formularzy po zbudowaniu UI
        self.root.after(300, self._restore_form_state)

        # Zapisz ustawienia przy zamknieciu okna
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    
    def _apply_icon(self):
        """Ustaw ikonę okna – najpierw z osadzonego base64, fallback do pliku."""
        try:
            # Priorytet: osadzony base64 (działa zawsze, bez zewnętrznych plików)
            import tempfile as _tf
            ico_data = base64.b64decode(_ICON_B64)
            tmp_ico = _tf.NamedTemporaryFile(suffix='.ico', delete=False)
            tmp_ico.write(ico_data)
            tmp_ico.close()
            self.root.iconbitmap(tmp_ico.name)
            # Usuń plik tymczasowy po ustawieniu (daj chwilę Windows na odczyt)
            self.root.after(1000, lambda p=tmp_ico.name: _safe_unlink(p))
        except Exception as _e:
            # Fallback: plik obok exe
            try:
                if os.path.exists(ICON_PATH):
                    self.root.iconbitmap(ICON_PATH)
            except Exception as _e:
                pass

    def _load_logo(self):
        """Załaduj logo – z osadzonego base64 (64x64 PNG)."""
        try:
            import io as _io
            png_data = base64.b64decode(_LOGO_B64)
            # Próba z PIL (lepszy rendering)
            from PIL import Image as _Img, ImageTk as _ITk
            img = _Img.open(_io.BytesIO(png_data))
            self._logo_img = _ITk.PhotoImage(img)
            return self._logo_img
        except Exception as _e:
            try:
                import io as _io
                png_data = base64.b64decode(_LOGO_B64)
                self._logo_img = tk.PhotoImage(data=_LOGO_B64)
                return self._logo_img
            except Exception as _e:
                return None

    def _tip(self, widget, key):
        """Utwórz Tooltip dla widgetu używając klucza i18n (dynamiczny – reaguje na zmianę języka)."""
        Tooltip(widget, lambda k=key: t(k))

    def _build_header(self, root):
        """Buduje pasek nagłówka z logo, tytułem i przyciskiem języka (prawy róg)."""
        header = tk.Frame(root, bg='#0a1a2e', height=72)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)

        logo_img = self._load_logo()
        if logo_img:
            logo_lbl = tk.Label(header, image=logo_img, bg='#0a1a2e', bd=0)
            logo_lbl.pack(side='left', padx=(8, 4), pady=4)

        text_frame = tk.Frame(header, bg='#0a1a2e')
        text_frame.pack(side='left', pady=4)

        tk.Label(text_frame,
                 text="SignTool's-ITS GUI",
                 font=('Segoe UI', 16, 'bold'),
                 fg='#00cfff', bg='#0a1a2e').pack(anchor='w')
        tk.Label(text_frame,
                 text=t("header_subtitle"),
                 font=('Segoe UI', 8),
                 fg='#5599bb', bg='#0a1a2e').pack(anchor='w')

        # Przycisk jezyka przeniesiony do status bara (prawy dolny rog)
    def _load_config(self):
        """Wczytaj konfigurację z pliku JSON"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as _e:
            pass
        return {}
    
    def _save_config(self):
        """Zapisz konfigurację do pliku JSON"""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            messagebox.showwarning("Save Error", f"Cannot save configuration:\n{e}")
    
    def _on_close(self):
        """Zapisz stan formularzy i zamknij aplikacje."""
        self._save_form_state()
        self._save_config()
        self.root.destroy()

    def _switch_language(self):
        """Przelacz jezyk PL <-> EN. Zapisz stan, przebuduj zakladki, przywroc stan."""
        current = get_language()
        new_lang = "en" if current == "pl" else "pl"
        set_language(new_lang)
        self.config["language"] = new_lang
        try:
            self._lang_btn.config(text="EN" if new_lang == "pl" else "PL")
        except Exception as _e:
            pass
        self.root.title(t("app_title"))
        try:
            self._save_form_state()
        except Exception as _e:
            pass
        try:
            self._rebuild_tabs()
        except Exception as _e:
            pass
        try:
            self._restore_form_state()
        except Exception as _e:
            pass
        self._save_config()

    def _rebuild_tabs(self):
        """Zniszcz i przebuduj wszystkie zakladki z aktualnym jezykiem."""
        try:
            active_tab = self.notebook.index(self.notebook.select())
        except Exception as _e:
            active_tab = 0
        # Destroy old tab frames (forget alone nie niszczy widgetow)
        for tab_id in list(self.notebook.tabs()):
            try:
                widget = self.root.nametowidget(tab_id)
                widget.destroy()
            except Exception as _e:
                try:
                    self.notebook.forget(tab_id)
                except Exception as _e:
                    pass
        self.create_sign_tab()
        self.create_timestamp_verify_tab()
        self.create_catdb_remove_tab()
        self.create_batch_tab()
        self.create_certgen_tab()
        try:
            self.notebook.select(active_tab)
        except Exception as _e:
            pass

    def _save_form_state(self):
        """Zapisz wartosci wszystkich pol formularzy do self.config."""
        c = self.config

        # == SIGN ==
        try:
            c["sign_cert_method"]      = self.sign_cert_method.get()
            c["sign_cert_name"]        = self.sign_cert_name.get()
            c["sign_cert_sha1"]        = self.sign_cert_sha1.get()
            c["sign_cert_file"]        = self.sign_cert_file.get()
            c["sign_additional_cert"]  = self.sign_additional_cert.get()
            c["sign_hash_alg"]         = self.sign_hash_alg.get()
            c["sign_description"]      = self.sign_description.get()
            c["sign_url"]              = self.sign_url.get()
            c["sign_timestamp"]        = self.sign_timestamp.get()
            c["sign_timestamp_method"] = self.sign_timestamp_method.get()
            c["sign_timestamp_alg"]    = self.sign_timestamp_alg.get()
            c["sign_append"]           = self.sign_append.get()
            c["sign_verbose"]          = self.sign_verbose.get()
            c["sign_debug"]            = self.sign_debug.get()
            # BEZPIECZEŃSTWO: sign_cert_password celowo NIE jest zapisywane
        except Exception as _e:
            pass

        # == TIMESTAMP / VERIFY ==
        try:
            c["ts_server"]            = self.ts_server.get()
            c["ts_timestamp_method"]  = self.ts_timestamp_method.get()
            c["ts_hash_alg"]          = self.ts_hash_alg.get()
            c["ts_verbose"]           = self.ts_verbose.get()
            c["verify_pa"]            = self.verify_pa.get()
            c["verify_pg"]            = self.verify_pg.get()
            c["verify_verbose"]       = self.verify_verbose.get()
            c["verify_catalog"]       = self.verify_catalog.get()
        except Exception as _e:
            pass

        # == CATDB / REMOVE ==
        try:
            c["catdb_file"]    = self.catdb_file.get()
            c["catdb_action"]  = self.catdb_action.get()
            c["catdb_verbose"] = self.catdb_verbose.get()
            c["remove_verbose"] = self.remove_verbose.get()
        except Exception as _e:
            pass

        # == CERTGEN ==
        try:
            c["certgen_method"]       = self.certgen_method.get()
            c["certgen_openssl_path"] = self.certgen_openssl_path.get()
            c["certgen_type"]         = self.certgen_type.get()
            c["certgen_cn"]           = self.certgen_cn.get()
            c["certgen_org"]          = self.certgen_org.get()
            c["certgen_country"]      = self.certgen_country.get()
            c["certgen_city"]         = self.certgen_city.get()
            c["certgen_state"]        = self.certgen_state.get()
            c["certgen_email"]        = self.certgen_email.get()
            c["certgen_key_alg"]      = self.certgen_key_alg.get()
            c["certgen_key_size"]     = self.certgen_key_size.get()
            c["certgen_ec_curve"]     = self.certgen_ec_curve.get()
            c["certgen_hash_alg"]     = self.certgen_hash_alg.get()
            c["certgen_days"]         = self.certgen_days.get()
            c["certgen_outdir"]       = self.certgen_outdir.get()
            c["certgen_basename"]     = self.certgen_basename.get()
            c["certgen_export_pfx"]   = self.certgen_export_pfx.get()
            c["certgen_install"]      = self.certgen_install.get()
            san_dns = self.certgen_san_dns.get("1.0", tk.END).strip()
            san_ip  = self.certgen_san_ip.get("1.0",  tk.END).strip()
            c["certgen_san_dns"] = san_dns
            c["certgen_san_ip"]  = san_ip
            # BEZPIECZEŃSTWO: hasła NIE są zapisywane do pliku konfiguracji
            # certgen_pfx_pass i certgen_ca_key_pass celowo pominięte
        except Exception as _e:
            pass

    def _restore_form_state(self):
        """Przywroc wartosci pol formularzy z self.config."""
        c = self.config

        def _set_entry(widget, key, default=""):
            val = c.get(key, default)
            if val:
                widget.delete(0, tk.END)
                widget.insert(0, val)

        def _set_text(widget, key, default=""):
            val = c.get(key, default)
            if val:
                widget.delete("1.0", tk.END)
                widget.insert("1.0", val)

        def _set_var(var, key, default=None):
            val = c.get(key, default)
            if val is not None:
                var.set(val)

        def _set_combo(widget, key, default=None):
            val = c.get(key, default)
            if val:
                widget.set(val)

        # == SIGN ==
        try:
            _set_var(self.sign_cert_method,      "sign_cert_method")
            _set_entry(self.sign_cert_name,       "sign_cert_name")
            _set_entry(self.sign_cert_sha1,       "sign_cert_sha1")
            _set_entry(self.sign_cert_file,       "sign_cert_file")
            _set_entry(self.sign_additional_cert, "sign_additional_cert")
            _set_combo(self.sign_hash_alg,        "sign_hash_alg")
            _set_entry(self.sign_description,     "sign_description")
            _set_entry(self.sign_url,             "sign_url")
            _set_entry(self.sign_timestamp,       "sign_timestamp")
            _set_var(self.sign_timestamp_method,  "sign_timestamp_method")
            _set_combo(self.sign_timestamp_alg,   "sign_timestamp_alg")
            _set_var(self.sign_append,            "sign_append")
            _set_var(self.sign_verbose,           "sign_verbose")
            _set_var(self.sign_debug,             "sign_debug")
        except Exception as _e:
            pass

        # == TIMESTAMP / VERIFY ==
        try:
            _set_entry(self.ts_server,           "ts_server")
            _set_var(self.ts_timestamp_method,   "ts_timestamp_method")
            _set_combo(self.ts_hash_alg,         "ts_hash_alg")
            _set_var(self.ts_verbose,            "ts_verbose")
            _set_var(self.verify_pa,             "verify_pa")
            _set_var(self.verify_pg,             "verify_pg")
            _set_var(self.verify_verbose,        "verify_verbose")
            _set_entry(self.verify_catalog,      "verify_catalog")
        except Exception as _e:
            pass

        # == CATDB / REMOVE ==
        try:
            _set_entry(self.catdb_file,    "catdb_file")
            _set_combo(self.catdb_action,  "catdb_action")
            _set_var(self.catdb_verbose,   "catdb_verbose")
            _set_var(self.remove_verbose,  "remove_verbose")
        except Exception as _e:
            pass

        # == CERTGEN ==
        try:
            _set_var(self.certgen_method,         "certgen_method")
            _set_entry(self.certgen_openssl_path, "certgen_openssl_path")
            _set_var(self.certgen_type,           "certgen_type")
            _set_entry(self.certgen_cn,           "certgen_cn")
            _set_entry(self.certgen_org,          "certgen_org")
            _set_entry(self.certgen_country,      "certgen_country")
            _set_entry(self.certgen_city,         "certgen_city")
            _set_entry(self.certgen_state,        "certgen_state")
            _set_entry(self.certgen_email,        "certgen_email")
            _set_combo(self.certgen_key_alg,      "certgen_key_alg")
            _set_combo(self.certgen_key_size,     "certgen_key_size")
            _set_combo(self.certgen_ec_curve,     "certgen_ec_curve")
            _set_combo(self.certgen_hash_alg,     "certgen_hash_alg")
            _set_entry(self.certgen_days,         "certgen_days")
            _set_entry(self.certgen_outdir,       "certgen_outdir")
            _set_entry(self.certgen_basename,     "certgen_basename")
            _set_var(self.certgen_export_pfx,     "certgen_export_pfx")
            _set_var(self.certgen_install,        "certgen_install")
            _set_text(self.certgen_san_dns,       "certgen_san_dns")
            _set_text(self.certgen_san_ip,        "certgen_san_ip")
            # Odswiez widocznosc paneli zaleznie od przywroconego typu
            self._certgen_toggle_type()
            self._certgen_toggle_keyalg()
        except Exception as _e:
            pass

    def _set_tool_leds(self, signtool_ok, openssl_ok):
        """Aktualizuje kolory wskaznikow LED w pasku statusu.
        Zielony = narzedzie zaladowane, Czerwony = brak."""
        def _color(ok):
            return ("#00bb00", "#007700") if ok else ("#cc0000", "#880000")

        fill_st, outline_st = _color(signtool_ok)
        fill_os, outline_os = _color(openssl_ok)

        self._led_signtool_canvas.itemconfig(
            self._led_signtool_id, fill=fill_st, outline=outline_st)
        self._led_openssl_canvas.itemconfig(
            self._led_openssl_id, fill=fill_os, outline=outline_os)

    def find_signtool(self):
        """Szybkie wyszukiwanie signtool.exe (bez pełnego skanu dysku – do startu).
        Kolejność priorytetów:
          0. Zapisana konfiguracja (SignToolGUI.json)
          1. Folder obok exe / main.py  (APP_TOOLS_DIR)
          2. Folder _MEIPASS (bundlowane przez PyInstaller)
          3. Systemowy PATH (where signtool.exe)
          4. Typowe lokalizacje Windows Kits
        """
        # 0. Zapisana konfiguracja
        saved = self.config.get('signtool_path', '')
        if saved and os.path.exists(saved):
            return saved
        # 1. Folder obok exe / main.py
        local = os.path.join(APP_TOOLS_DIR, "signtool.exe")
        if os.path.isfile(local):
            return local
        # 2. _MEIPASS (PyInstaller bundle)
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            bundled = os.path.join(meipass, "signtool.exe")
            if os.path.isfile(bundled):
                return bundled
        # 3. PATH
        try:
            res = subprocess.run(['where', 'signtool.exe'],
                                 capture_output=True, text=True, shell=True)
            if res.returncode == 0:
                p = res.stdout.strip().split('\n')[0].strip()
                if p:
                    return p
        except Exception as _e:
            pass
        # 4. Common Windows Kits locations
        candidates = [
            r"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe",
            r"C:\Program Files (x86)\Windows Kits\10\bin\x86\signtool.exe",
            r"C:\Program Files\Microsoft SDKs\Windows\v7.1\Bin\signtool.exe",
        ]
        kits_base = r"C:\Program Files (x86)\Windows Kits"
        if os.path.exists(kits_base):
            for ver in ['10', '8.1', '8.0']:
                for arch in ['x64', 'x86', 'arm64']:
                    candidates.append(os.path.join(kits_base, ver, 'bin', arch, 'signtool.exe'))
        # Windows Kits z numerem buildu (np. 10.0.22621.0)
        kits10 = os.path.join(kits_base, '10', 'bin')
        if os.path.exists(kits10):
            try:
                for sub in sorted(os.listdir(kits10), reverse=True):
                    for arch in ['x64', 'x86', 'arm64']:
                        candidates.append(os.path.join(kits10, sub, arch, 'signtool.exe'))
            except Exception as _e:
                pass
        for p in candidates:
            if os.path.exists(p):
                return p
        return "signtool.exe"

    @staticmethod
    def _get_drives():
        """Zwraca listę dostępnych dysków na Windows"""
        drives = []
        try:
            import string
            for letter in string.ascii_uppercase:
                d = f"{letter}:\\"
                if os.path.exists(d):
                    drives.append(d)
        except Exception as _e:
            pass
        if not drives:
            drives = [r"C:\\"]
        return drives

    @staticmethod
    def _deep_search(filename, search_roots, max_depth=6, stop_event=None):
        """
        Przeszukuje drzewo katalogów w poszukiwaniu pliku.
        Zwraca pierwszą znalezioną ścieżkę lub None.
        """
        found = []
        skip_dirs = {
            'windows', '$recycle.bin', 'system volume information',
            'perflogs', 'recovery', '$windows.~bt', '$windows.~ws',
            'msocache', 'config.msi',
        }
        for root_dir in search_roots:
            for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
                if stop_event and stop_event.is_set():
                    return found
                # Oblicz głębokość
                rel = os.path.relpath(dirpath, root_dir)
                depth = 0 if rel == '.' else len(Path(rel).parts)
                if depth >= max_depth:
                    dirnames.clear()
                    continue
                # Pomiń katalogi systemowe
                dirnames[:] = [d for d in dirnames
                                if d.lower() not in skip_dirs
                                and not d.startswith('.')]
                for fn in filenames:
                    if fn.lower() == filename.lower():
                        found.append(os.path.join(dirpath, fn))
                        if found:
                            return found  # zwróć po pierwszym znalezieniu
        return found

    def _auto_detect_tools(self):
        """
        Uruchamia pełne auto-wykrywanie signtool.exe i openssl.exe w tle.
        Pokazuje dialog postępu, a po zakończeniu raport z wynikami.
        """
        # Dialog postępu
        progress_win = tk.Toplevel(self.root)
        progress_win.title("Detecting tools...")
        progress_win.geometry("520x200")
        progress_win.resizable(False, False)
        progress_win.grab_set()
        progress_win.transient(self.root)

        tk.Label(progress_win, text=t("detect_searching"),
                 font=('TkDefaultFont', 10, 'bold'), pady=8).pack()

        self._detect_status_var = tk.StringVar(value="Initializing...")
        tk.Label(progress_win, textvariable=self._detect_status_var,
                 foreground='gray', font=('TkDefaultFont', 8), wraplength=480).pack(pady=2)

        pb = ttk.Progressbar(progress_win, mode='indeterminate', length=460)
        pb.pack(pady=8)
        pb.start(12)

        stop_event = threading.Event()
        cancel_btn = ttk.Button(progress_win, text=t("detect_cancel"),
                                command=stop_event.set)
        cancel_btn.pack(pady=4)

        result = {'signtool': None, 'openssl': None}

        def update_status(msg):
            self.root.after(0, lambda m=msg: self._detect_status_var.set(m))

        def do_search():
            drives = self._get_drives()

            # ── signtool ──
            update_status(f"Searching signtool.exe on drives: {', '.join(drives[:4])} ...")
            # Priorytet: szybkie lokalizacje
            fast_st = self.find_signtool()
            if fast_st != "signtool.exe" and os.path.exists(fast_st):
                result['signtool'] = fast_st
                update_status(f"signtool.exe found: {fast_st}")
            else:
                # Pełny skan
                found = self._deep_search('signtool.exe', drives,
                                          max_depth=8, stop_event=stop_event)
                result['signtool'] = found[0] if found else None
                if result['signtool']:
                    update_status(f"signtool.exe found: {result['signtool']}")
                else:
                    update_status("signtool.exe — not found")

            if stop_event.is_set():
                self.root.after(0, progress_win.destroy)
                return

            # ── openssl ──
            update_status(f"Searching openssl.exe on drives: {', '.join(drives[:4])} ...")
            fast_ossl = self._find_openssl()
            if fast_ossl != "openssl" and os.path.exists(fast_ossl):
                result['openssl'] = fast_ossl
                update_status(f"openssl.exe found: {fast_ossl}")
            else:
                found = self._deep_search('openssl.exe', drives,
                                          max_depth=8, stop_event=stop_event)
                result['openssl'] = found[0] if found else None
                if result['openssl']:
                    update_status(f"openssl.exe found: {result['openssl']}")
                else:
                    update_status("openssl.exe — not found")

            # Zakończ
            self.root.after(0, lambda: _finish(result))

        def _finish(res):
            try:
                pb.stop()
                progress_win.destroy()
            except Exception as _e:
                pass

            # Zastosuj znalezione ścieżki od razu
            if res['signtool']:
                self.signtool_path = res['signtool']
                self.config['signtool_path'] = res['signtool']

            if res['openssl']:
                self.config['openssl_path'] = res['openssl']
                try:
                    self.certgen_openssl_path.delete(0, tk.END)
                    self.certgen_openssl_path.insert(0, res['openssl'])
                except Exception as _e:
                    pass

            # Zaktualizuj LEDy i pasek statusu
            self._set_tool_leds(bool(res['signtool']), bool(res['openssl']))
            parts = []
            parts.append("signtool OK" if res['signtool'] else "signtool MISSING")
            parts.append("openssl OK"  if res['openssl']  else "openssl MISSING")
            self.status_bar.config(text="v2.0 | " + "  |  ".join(parts))

            # Zapisz do konfiguracji
            self._save_config()

            # Jeśli wszystko znalezione – nie pokazuj żadnego dialogu
            if res['signtool'] and res['openssl']:
                return

            # Czegoś brakuje – pokaż dialog tylko z brakującymi
            self._show_detect_report(res)

        threading.Thread(target=do_search, daemon=True).start()

    def _show_detect_report(self, result):
        """Dialog z raportem wykrywania narzędzi"""
        win = tk.Toplevel(self.root)
        win.title("Tool Detection Results")
        win.geometry("580x340")
        win.resizable(True, True)
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text=t("detect_title"),
                 font=('TkDefaultFont', 11, 'bold'), pady=8).pack()

        frame = ttk.Frame(win, padding=10)
        frame.pack(fill='both', expand=True)
        frame.columnconfigure(1, weight=1)

        missing = []

        def tool_row(row, icon, name, path, browse_cb):
            if path:
                color = '#1a7a1a'
                status_icon = '✅'
                display = path
            else:
                color = '#b50000'
                status_icon = '❌'
                display = 'Not found'
                missing.append(name)

            ttk.Label(frame, text=f"{status_icon} {name}",
                      font=('TkDefaultFont', 9, 'bold'),
                      foreground=color).grid(row=row, column=0, sticky='w', pady=4)

            path_var = tk.StringVar(value=display)
            entry = ttk.Entry(frame, textvariable=path_var, width=46)
            entry.grid(row=row, column=1, sticky='ew', padx=6, pady=4)

            def _browse(pv=path_var, n=name):
                f = filedialog.askopenfilename(
                    title=f"Locate {n}",
                    filetypes=[(f"{n}", f"*{n}*"), ("All files", "*.*")]
                )
                if f:
                    pv.set(f)

            ttk.Button(frame, text="...", width=3, command=_browse).grid(
                row=row, column=2, padx=2)
            return path_var

        st_var   = tool_row(0, '🔨', 'signtool.exe', result.get('signtool'), None)
        ossl_var = tool_row(1, '🔑', 'openssl.exe',  result.get('openssl'),  None)

        # Separator + info
        ttk.Separator(frame, orient='horizontal').grid(
            row=2, column=0, columnspan=3, sticky='ew', pady=8)

        if missing:
            miss_str = ', '.join(missing)
            info = (
                f"⚠️  Not found: {miss_str}\n\n"
                "To use full functionality:\n"
                "• signtool.exe — install Windows SDK (Windows Kits)\n"
                "• openssl.exe — install OpenSSL for Windows or Git for Windows\n\n"
                "You can set paths manually above and click 'Apply'."
            )
            tk.Label(frame, text=info, justify='left', foreground='#7a4400',
                     font=('TkDefaultFont', 8), wraplength=520).grid(
                row=3, column=0, columnspan=3, sticky='w', pady=2)
        else:
            tk.Label(frame, text=t("detect_all_ok"),
                     foreground='#1a7a1a', font=('TkDefaultFont', 9)).grid(
                row=3, column=0, columnspan=3, sticky='w', pady=2)

        # Przyciski
        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill='x', padx=10, pady=8)

        def _apply():
            st_path   = st_var.get().strip()
            ossl_path = ossl_var.get().strip()
            if st_path and st_path not in ('Not found', '') and os.path.exists(st_path):
                self.signtool_path = st_path
            # Zaktualizuj pole openssl w zakładce certgen (jeśli istnieje)
            if ossl_path and ossl_path not in ('Not found', '') and os.path.exists(ossl_path):
                try:
                    self.certgen_openssl_path.delete(0, tk.END)
                    self.certgen_openssl_path.insert(0, ossl_path)
                except Exception as _e:
                    pass
            # Zapisz do konfiguracji
            self.config['signtool_path'] = self.signtool_path
            if ossl_path and ossl_path != 'Not found':
                self.config['openssl_path'] = ossl_path
            self._save_config()
            # Aktualizuj LEDy i status bar
            st_ok   = bool(result.get('signtool'))
            ossl_ok = bool(result.get('openssl'))
            self._set_tool_leds(st_ok, ossl_ok)
            parts = []
            parts.append("signtool OK" if st_ok   else "signtool MISSING")
            parts.append("openssl OK"  if ossl_ok else "openssl MISSING")
            self.status_bar.config(text="v2.0 | " + "  |  ".join(parts))
            win.destroy()

        ttk.Button(btn_frame, text=t("detect_apply"),
                   command=_apply, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text=t("detect_close"),
                   command=win.destroy).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=t("detect_retry"),
                   command=lambda: [win.destroy(), self._auto_detect_tools()]).pack(side='right', padx=5)
    
    def create_sign_tab(self):
        """Zakładka SIGN - podpisywanie plików"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=t("tab_sign"))
        
        # Wewnętrzny notebook: Opcje | Wynik
        inner = ttk.Notebook(frame)
        self._inner_sign = inner
        inner.pack(fill='both', expand=True)
        
        options_tab = ttk.Frame(inner)
        result_tab = ttk.Frame(inner)
        inner.add(options_tab, text=t("tab_options"))
        inner.add(result_tab, text=t("tab_result"))
        
        # Output w zakładce Wynik
        self.sign_output = scrolledtext.ScrolledText(result_tab, wrap=tk.WORD)
        self.sign_output.pack(fill='both', expand=True, padx=3, pady=3)
        
        # ScrolledFrame dla opcji
        canvas = tk.Canvas(options_tab)
        scrollbar = ttk.Scrollbar(options_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_canvas_resize(event):
            items = canvas.find_all()
            if items:
                canvas.itemconfig(items[0], width=event.width)
        canvas.bind("<Configure>", _on_canvas_resize)
        
        # Obsługa kółka myszy
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)
        
        # Pomocnicze funkcje – wykonaj i przełącz na Wynik
        def _exec_sign():
            self.execute_sign()
            inner.select(result_tab)
        
        def _show_cmd():
            self.show_sign_command()
            inner.select(result_tab)
        
        # Pliki do podpisania
        files_frame = ttk.LabelFrame(scrollable_frame, text=t("sign_files_frame"), padding=5)
        files_frame.pack(fill='x', padx=3, pady=3)
        
        self.sign_files = []
        self.sign_files_listbox = tk.Listbox(files_frame, height=3)
        self.sign_files_listbox.pack(fill='x', pady=2)
        self._tip(self.sign_files_listbox, "tip_sign_files")

        btn_frame = ttk.Frame(files_frame)
        btn_frame.pack(fill='x')
        ttk.Button(btn_frame, text=t("btn_add_files"), command=self.add_sign_files).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=t("btn_remove_selected"), command=self.remove_sign_files).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=t("btn_clear"), command=self.clear_sign_files).pack(side='left', padx=2)
        
        # Certyfikat
        cert_frame = ttk.LabelFrame(scrollable_frame, text=t("cert_frame"), padding=5)
        cert_frame.pack(fill='x', padx=3, pady=3)
        
        # Wybór metody certyfikatu
        cert_frame.columnconfigure(1, weight=1)
        ttk.Label(cert_frame, text=t("cert_method_label")).grid(row=0, column=0, sticky='w', pady=2)
        self.sign_cert_method = tk.StringVar(value="store")
        _rb_store = ttk.Radiobutton(cert_frame, text=t("cert_from_store"),
                       variable=self.sign_cert_method, value="store")
        _rb_store.grid(row=0, column=1, sticky='w')
        _rb_file = ttk.Radiobutton(cert_frame, text=t("cert_from_file"),
                       variable=self.sign_cert_method, value="file")
        _rb_file.grid(row=0, column=2, sticky='w')
        self._tip(_rb_store, "tip_sign_cert_store")
        self._tip(_rb_file,  "tip_sign_cert_file")

        # Nazwa certyfikatu (z magazynu)
        ttk.Label(cert_frame, text=t("cert_name_label")).grid(row=1, column=0, sticky='w', pady=1)
        self.sign_cert_name = ttk.Entry(cert_frame, width=32)
        self.sign_cert_name.grid(row=1, column=1, columnspan=2, sticky='ew', pady=1)
        self._tip(self.sign_cert_name, "tip_sign_cert_name")

        # SHA1 certyfikatu
        ttk.Label(cert_frame, text=t("cert_sha1_label")).grid(row=2, column=0, sticky='w', pady=1)
        self.sign_cert_sha1 = ttk.Entry(cert_frame, width=32)
        self.sign_cert_sha1.grid(row=2, column=1, columnspan=2, sticky='ew', pady=1)
        self._tip(self.sign_cert_sha1, "tip_sign_cert_sha1")

        # Plik certyfikatu
        ttk.Label(cert_frame, text=t("cert_file_label")).grid(row=3, column=0, sticky='w', pady=1)
        self.sign_cert_file = ttk.Entry(cert_frame, width=32)
        self.sign_cert_file.grid(row=3, column=1, sticky='ew', pady=1)
        self._tip(self.sign_cert_file, "tip_sign_pfx_file")
        ttk.Button(cert_frame, text="...", width=3,
                  command=lambda: self.browse_file(self.sign_cert_file, "PFX files", "*.pfx")).grid(row=3, column=2, padx=2)

        # Hasło do certyfikatu
        ttk.Label(cert_frame, text=t("cert_password_label")).grid(row=4, column=0, sticky='w', pady=1)
        self.sign_cert_password = ttk.Entry(cert_frame, width=32, show="*")
        self.sign_cert_password.grid(row=4, column=1, columnspan=2, sticky='ew', pady=1)
        self._tip(self.sign_cert_password, "tip_sign_pfx_pass")

        # ===== FAZA 1: DODATKOWY CERTYFIKAT =====
        ttk.Label(cert_frame, text=t("cert_additional_label")).grid(row=5, column=0, sticky='w', pady=1)
        self.sign_additional_cert = ttk.Entry(cert_frame, width=32)
        self.sign_additional_cert.grid(row=5, column=1, sticky='ew', pady=1)
        self._tip(self.sign_additional_cert, "tip_sign_addl_cert")
        ttk.Button(cert_frame, text="...", width=3,
                  command=lambda: self.browse_file(self.sign_additional_cert, "Certificate files", "*.cer;*.crt")).grid(row=5, column=2, padx=2)
        
        # Info o dodatkowym certyfikacie
        info_label = ttk.Label(cert_frame, text=t("cert_additional_info"), 
                              foreground="blue", font=('TkDefaultFont', 7))
        info_label.grid(row=6, column=1, columnspan=2, sticky='w', pady=(0, 2))
        
        # Opcje podpisywania
        options_frame = ttk.LabelFrame(scrollable_frame, text=t("sign_options_frame"), padding=5)
        options_frame.pack(fill='x', padx=3, pady=3)
        
        # Algorytm hash
        options_frame.columnconfigure(1, weight=1)
        ttk.Label(options_frame, text=t("hash_alg_label")).grid(row=0, column=0, sticky='w', pady=1)
        self.sign_hash_alg = ttk.Combobox(options_frame, values=["SHA1", "SHA256", "SHA384", "SHA512"], width=12)
        self.sign_hash_alg.set("SHA256")
        self.sign_hash_alg.grid(row=0, column=1, sticky='w', pady=1)
        self._tip(self.sign_hash_alg, "tip_sign_hash")

        # Opis
        ttk.Label(options_frame, text=t("desc_label")).grid(row=1, column=0, sticky='w', pady=1)
        self.sign_description = ttk.Entry(options_frame, width=32)
        self.sign_description.grid(row=1, column=1, columnspan=2, sticky='ew', pady=1)
        self._tip(self.sign_description, "tip_sign_desc")

        # URL
        ttk.Label(options_frame, text=t("url_label")).grid(row=2, column=0, sticky='w', pady=1)
        self.sign_url = ttk.Entry(options_frame, width=32)
        self.sign_url.grid(row=2, column=1, columnspan=2, sticky='ew', pady=1)
        self._tip(self.sign_url, "tip_sign_url")

        # ===== FAZA 1: TIMESTAMP Z WYBOREM METODY =====
        ttk.Label(options_frame, text=t("timestamp_server_label")).grid(row=3, column=0, sticky='w', pady=1)
        self.sign_timestamp = ttk.Entry(options_frame, width=32)
        self.sign_timestamp.grid(row=3, column=1, columnspan=2, sticky='ew', pady=1)
        self._tip(self.sign_timestamp, "tip_sign_ts_server")

        # Wybór metody timestamp
        timestamp_method_frame = ttk.Frame(options_frame)
        timestamp_method_frame.grid(row=4, column=1, columnspan=2, sticky='w', pady=2)

        self.sign_timestamp_method = tk.StringVar(value="rfc3161")
        _rb_rfc = ttk.Radiobutton(timestamp_method_frame, text=t("ts_rfc3161"),
                       variable=self.sign_timestamp_method, value="rfc3161")
        _rb_rfc.pack(side='left', padx=5)
        _rb_auth = ttk.Radiobutton(timestamp_method_frame, text=t("ts_authenticode"),
                       variable=self.sign_timestamp_method, value="authenticode")
        _rb_auth.pack(side='left', padx=5)
        self._tip(_rb_rfc,  "tip_sign_ts_rfc3161")
        self._tip(_rb_auth, "tip_sign_ts_auth")

        # Info o metodach timestamp
        timestamp_info = ttk.Label(options_frame,
                                   text=t("ts_info"),
                                   foreground="blue", font=('TkDefaultFont', 7), wraplength=400)
        timestamp_info.grid(row=5, column=1, columnspan=2, sticky='w', pady=(0, 2))

        # Timestamp digest algorithm (tylko dla RFC3161)
        ttk.Label(options_frame, text=t("ts_hash_label")).grid(row=6, column=0, sticky='w', pady=1)
        self.sign_timestamp_alg = ttk.Combobox(options_frame, values=["SHA1", "SHA256", "SHA384", "SHA512"], width=12)
        self.sign_timestamp_alg.set("SHA256")
        self.sign_timestamp_alg.grid(row=6, column=1, sticky='w', pady=1)
        self._tip(self.sign_timestamp_alg, "tip_sign_ts_hash")

        timestamp_alg_info = ttk.Label(options_frame, text=t("lbl_rfc3161_only"),
                                       foreground="gray", font=('TkDefaultFont', 7))
        timestamp_alg_info.grid(row=6, column=2, sticky='w', padx=5)

        # Dodatkowe opcje
        self.sign_append = tk.BooleanVar()
        _cb_append = ttk.Checkbutton(options_frame, text=t("sign_append"),
                       variable=self.sign_append)
        _cb_append.grid(row=7, column=0, columnspan=2, sticky='w', pady=1)
        self._tip(_cb_append, "tip_sign_append")

        self.sign_verbose = tk.BooleanVar()
        _cb_verbose = ttk.Checkbutton(options_frame, text=t("lbl_verbose"),
                       variable=self.sign_verbose)
        _cb_verbose.grid(row=8, column=0, columnspan=2, sticky='w', pady=1)
        self._tip(_cb_verbose, "tip_sign_verbose")

        self.sign_debug = tk.BooleanVar()
        _cb_debug = ttk.Checkbutton(options_frame, text=t("sign_debug"),
                       variable=self.sign_debug)
        _cb_debug.grid(row=9, column=0, columnspan=2, sticky='w', pady=1)
        self._tip(_cb_debug, "tip_sign_debug")

        # Przyciski akcji
        action_frame = ttk.Frame(scrollable_frame)
        action_frame.pack(fill='x', padx=3, pady=5)

        _btn_sign = ttk.Button(action_frame, text=t("btn_sign"),
                  command=_exec_sign, style='Accent.TButton')
        _btn_sign.pack(side='left', padx=5)
        self._tip(_btn_sign, "tip_btn_sign")

        _btn_show = ttk.Button(action_frame, text=t("btn_show_cmd"),
                  command=_show_cmd)
        _btn_show.pack(side='left', padx=5)
        self._tip(_btn_show, "tip_btn_show_cmd")
        
        options_tab.rowconfigure(0, weight=1)
        options_tab.columnconfigure(0, weight=1)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
    def create_timestamp_verify_tab(self):
        """Zakładka łączona: Timestamp (góra) + Verify (dół) z separatorem"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=t("tab_ts_verify"))

        inner = ttk.Notebook(frame)
        self._inner_ts = inner
        inner.pack(fill='both', expand=True)
        options_tab = ttk.Frame(inner)
        result_tab = ttk.Frame(inner)
        inner.add(options_tab, text=t("tab_options"))
        inner.add(result_tab, text=t("tab_result"))

        # Dwa outputy w zakładce Wynik – PanedWindow pionowo
        result_pane = ttk.PanedWindow(result_tab, orient=tk.VERTICAL)
        result_pane.pack(fill='both', expand=True, padx=3, pady=3)

        ts_result_frame = ttk.LabelFrame(result_pane, text=t("ts_output_frame"), padding=3)
        self.ts_output = scrolledtext.ScrolledText(ts_result_frame, wrap=tk.WORD, height=8)
        self.ts_output.pack(fill='both', expand=True)
        result_pane.add(ts_result_frame, weight=1)

        verify_result_frame = ttk.LabelFrame(result_pane, text=t("verify_output_frame"), padding=3)
        self.verify_output = scrolledtext.ScrolledText(verify_result_frame, wrap=tk.WORD, height=8)
        self.verify_output.pack(fill='both', expand=True)
        result_pane.add(verify_result_frame, weight=1)

        # Opcje – PanedWindow pionowo z separatorem
        options_tab.rowconfigure(0, weight=1)
        options_tab.columnconfigure(0, weight=1)

        pane = ttk.PanedWindow(options_tab, orient=tk.VERTICAL)
        pane.grid(row=0, column=0, sticky='nsew')

        # ── SEKCJA TIMESTAMP ──────────────────────────────────────
        ts_frame = ttk.LabelFrame(pane, text=t("ts_frame"), padding=5)
        pane.add(ts_frame, weight=1)

        # Pliki timestamp
        ts_files_frame = ttk.LabelFrame(ts_frame, text=t("lbl_files"), padding=4)
        ts_files_frame.pack(fill='x', padx=3, pady=3)

        self.ts_files = []
        self.ts_files_listbox = tk.Listbox(ts_files_frame, height=2)
        self.ts_files_listbox.pack(fill='x', pady=2)
        self._tip(self.ts_files_listbox, "tip_sign_files")
        ts_btn = ttk.Frame(ts_files_frame)
        ts_btn.pack(fill='x')
        ttk.Button(ts_btn, text=t("btn_add_files"), command=self.add_ts_files).pack(side='left', padx=2)
        ttk.Button(ts_btn, text=t("btn_remove_selected"), command=self.remove_ts_files).pack(side='left', padx=2)

        # Opcje timestamp
        ts_opts = ttk.LabelFrame(ts_frame, text=t("lbl_options"), padding=4)
        ts_opts.pack(fill='x', padx=3, pady=3)
        ts_opts.columnconfigure(1, weight=1)

        ttk.Label(ts_opts, text=t("ts_server_label")).grid(row=0, column=0, sticky='w', pady=1)
        self.ts_server = ttk.Entry(ts_opts)
        self.ts_server.grid(row=0, column=1, columnspan=2, sticky='ew', pady=1)
        self._tip(self.ts_server, "tip_ts_server")

        ts_method_frame = ttk.Frame(ts_opts)
        ts_method_frame.grid(row=1, column=1, columnspan=2, sticky='w', pady=1)
        self.ts_timestamp_method = tk.StringVar(value="rfc3161")
        _rb_ts_rfc = ttk.Radiobutton(ts_method_frame, text=t("ts_rfc3161"), variable=self.ts_timestamp_method, value="rfc3161")
        _rb_ts_rfc.pack(side='left', padx=3)
        _rb_ts_auth = ttk.Radiobutton(ts_method_frame, text=t("ts_authenticode"), variable=self.ts_timestamp_method, value="authenticode")
        _rb_ts_auth.pack(side='left', padx=3)
        self._tip(_rb_ts_rfc,  "tip_sign_ts_rfc3161")
        self._tip(_rb_ts_auth, "tip_sign_ts_auth")

        ttk.Label(ts_opts, text=t("ts_hash_short")).grid(row=2, column=0, sticky='w', pady=1)
        self.ts_hash_alg = ttk.Combobox(ts_opts, values=["SHA1", "SHA256", "SHA384", "SHA512"], width=10)
        self.ts_hash_alg.set("SHA256")
        self.ts_hash_alg.grid(row=2, column=1, sticky='w', pady=1)
        self._tip(self.ts_hash_alg, "tip_ts_hash")
        ttk.Label(ts_opts, text=t("lbl_rfc3161_only"), foreground="gray", font=('TkDefaultFont', 7)).grid(row=2, column=2, sticky='w', padx=3)

        self.ts_verbose = tk.BooleanVar()
        _cb_ts_v = ttk.Checkbutton(ts_opts, text=t("lbl_verbose"), variable=self.ts_verbose)
        _cb_ts_v.grid(row=3, column=0, columnspan=3, sticky='w', pady=1)
        self._tip(_cb_ts_v, "tip_sign_verbose")

        def _exec_ts():
            self.execute_timestamp()
            inner.select(result_tab)
        ts_action = ttk.Frame(ts_frame)
        ts_action.pack(fill='x', padx=3, pady=4)
        _btn_ts = ttk.Button(ts_action, text=t("btn_add_timestamp"), command=_exec_ts, style='Accent.TButton')
        _btn_ts.pack(side='left', padx=5)
        self._tip(_btn_ts, "tip_ts_server")

        # ── SEPARATOR ─────────────────────────────────────────────
        # (PanedWindow tworzy przeciągany separator automatycznie)

        # ── SEKCJA VERIFY ─────────────────────────────────────────
        verify_frame = ttk.LabelFrame(pane, text=t("verify_frame"), padding=5)
        pane.add(verify_frame, weight=1)

        # Pliki verify
        v_files_frame = ttk.LabelFrame(verify_frame, text=t("lbl_files"), padding=4)
        v_files_frame.pack(fill='x', padx=3, pady=3)

        self.verify_files = []
        self.verify_files_listbox = tk.Listbox(v_files_frame, height=2)
        self.verify_files_listbox.pack(fill='x', pady=2)
        self._tip(self.verify_files_listbox, "tip_sign_files")
        v_btn = ttk.Frame(v_files_frame)
        v_btn.pack(fill='x')
        ttk.Button(v_btn, text=t("btn_add_files"), command=self.add_verify_files).pack(side='left', padx=2)
        ttk.Button(v_btn, text=t("btn_remove_selected"), command=self.remove_verify_files).pack(side='left', padx=2)

        # Opcje verify
        v_opts = ttk.LabelFrame(verify_frame, text=t("lbl_options"), padding=4)
        v_opts.pack(fill='x', padx=3, pady=3)
        v_opts.columnconfigure(1, weight=1)

        self.verify_pa = tk.BooleanVar()
        _cb_pa = ttk.Checkbutton(v_opts, text=t("verify_pa"), variable=self.verify_pa)
        _cb_pa.grid(row=0, column=0, columnspan=3, sticky='w', pady=1)
        self._tip(_cb_pa, "tip_verify_pa")
        self.verify_pg = tk.BooleanVar()
        _cb_pg = ttk.Checkbutton(v_opts, text=t("verify_pg"), variable=self.verify_pg)
        _cb_pg.grid(row=1, column=0, columnspan=3, sticky='w', pady=1)
        self._tip(_cb_pg, "tip_verify_pg")
        self.verify_verbose = tk.BooleanVar()
        _cb_vv = ttk.Checkbutton(v_opts, text=t("lbl_verbose"), variable=self.verify_verbose)
        _cb_vv.grid(row=2, column=0, columnspan=3, sticky='w', pady=1)
        self._tip(_cb_vv, "tip_sign_verbose")

        ttk.Label(v_opts, text=t("catalog_label")).grid(row=3, column=0, sticky='w', pady=1)
        self.verify_catalog = ttk.Entry(v_opts)
        self.verify_catalog.grid(row=3, column=1, sticky='ew', pady=1)
        self._tip(self.verify_catalog, "tip_verify_catalog")
        ttk.Button(v_opts, text="...", width=3,
                  command=lambda: self.browse_file(self.verify_catalog, "Catalog files", "*.cat")).grid(row=3, column=2, padx=2)

        def _exec_verify():
            self.execute_verify()
            inner.select(result_tab)
        v_action = ttk.Frame(verify_frame)
        v_action.pack(fill='x', padx=3, pady=4)
        ttk.Button(v_action, text=t("btn_verify"), command=_exec_verify, style='Accent.TButton').pack(side='left', padx=5)

    def create_catdb_remove_tab(self):
        """Zakładka łączona: CatDB (góra) + Remove (dół) z separatorem"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=t("tab_catdb_remove"))

        inner = ttk.Notebook(frame)
        self._inner_catdb = inner
        inner.pack(fill='both', expand=True)
        options_tab = ttk.Frame(inner)
        result_tab = ttk.Frame(inner)
        inner.add(options_tab, text=t("tab_options"))
        inner.add(result_tab, text=t("tab_result"))

        # Dwa outputy w zakładce Wynik
        result_pane = ttk.PanedWindow(result_tab, orient=tk.VERTICAL)
        result_pane.pack(fill='both', expand=True, padx=3, pady=3)

        catdb_result_frame = ttk.LabelFrame(result_pane, text=t("catdb_output_frame"), padding=3)
        self.catdb_output = scrolledtext.ScrolledText(catdb_result_frame, wrap=tk.WORD, height=8)
        self.catdb_output.pack(fill='both', expand=True)
        result_pane.add(catdb_result_frame, weight=1)

        remove_result_frame = ttk.LabelFrame(result_pane, text=t("remove_output_frame"), padding=3)
        self.remove_output = scrolledtext.ScrolledText(remove_result_frame, wrap=tk.WORD, height=8)
        self.remove_output.pack(fill='both', expand=True)
        result_pane.add(remove_result_frame, weight=1)

        # Opcje – PanedWindow pionowy z separatorem
        options_tab.rowconfigure(0, weight=1)
        options_tab.columnconfigure(0, weight=1)

        pane = ttk.PanedWindow(options_tab, orient=tk.VERTICAL)
        pane.grid(row=0, column=0, sticky='nsew')

        # ── SEKCJA CATDB ──────────────────────────────────────────
        catdb_frame = ttk.LabelFrame(pane, text=t("catdb_frame"), padding=5)
        pane.add(catdb_frame, weight=1)

        ttk.Label(catdb_frame,
                  text=t("catdb_desc"),
                  foreground="gray", font=('TkDefaultFont', 7)).pack(anchor='w', padx=3)

        catdb_opts = ttk.LabelFrame(catdb_frame, text=t("lbl_options"), padding=4)
        catdb_opts.pack(fill='x', padx=3, pady=3)
        catdb_opts.columnconfigure(1, weight=1)

        ttk.Label(catdb_opts, text=t("catdb_file_label")).grid(row=0, column=0, sticky='w', pady=1)
        self.catdb_file = ttk.Entry(catdb_opts)
        self.catdb_file.grid(row=0, column=1, sticky='ew', pady=1)
        self._tip(self.catdb_file, "tip_catdb_file")
        ttk.Button(catdb_opts, text="...", width=3,
                  command=lambda: self.browse_file(self.catdb_file, "Catalog files", "*.cat")).grid(row=0, column=2, padx=2)

        ttk.Label(catdb_opts, text=t("catdb_action_label")).grid(row=1, column=0, sticky='w', pady=1)
        self.catdb_action = ttk.Combobox(catdb_opts, values=["Dodaj (/u)", "Usuń (/r)"], width=14)
        self.catdb_action.set("Dodaj (/u)")
        self.catdb_action.grid(row=1, column=1, sticky='w', pady=1)
        self._tip(self.catdb_action, "tip_catdb_action")

        self.catdb_verbose = tk.BooleanVar()
        _cb_catdb_v = ttk.Checkbutton(catdb_opts, text=t("lbl_verbose"), variable=self.catdb_verbose)
        _cb_catdb_v.grid(row=2, column=0, columnspan=3, sticky='w', pady=1)
        self._tip(_cb_catdb_v, "tip_sign_verbose")

        def _exec_catdb():
            self.execute_catdb()
            inner.select(result_tab)
        catdb_action_frame = ttk.Frame(catdb_frame)
        catdb_action_frame.pack(fill='x', padx=3, pady=4)
        _btn_catdb = ttk.Button(catdb_action_frame, text=t("btn_exec_catdb"), command=_exec_catdb, style='Accent.TButton')
        _btn_catdb.pack(side='left', padx=5)
        self._tip(_btn_catdb, "tip_catdb_file")

        # ── SEKCJA REMOVE ─────────────────────────────────────────
        remove_frame = ttk.LabelFrame(pane, text=t("remove_frame"), padding=5)
        pane.add(remove_frame, weight=1)

        # Pliki remove
        r_files_frame = ttk.LabelFrame(remove_frame, text=t("lbl_files"), padding=4)
        r_files_frame.pack(fill='x', padx=3, pady=3)

        self.remove_files = []
        self.remove_files_listbox = tk.Listbox(r_files_frame, height=2)
        self.remove_files_listbox.pack(fill='x', pady=2)
        self._tip(self.remove_files_listbox, "tip_remove_files")
        r_btn = ttk.Frame(r_files_frame)
        r_btn.pack(fill='x')
        ttk.Button(r_btn, text=t("btn_add_files"), command=self.add_remove_files).pack(side='left', padx=2)
        ttk.Button(r_btn, text=t("btn_remove_selected"), command=self.remove_remove_files).pack(side='left', padx=2)

        # Opcje remove
        r_opts = ttk.LabelFrame(remove_frame, text=t("lbl_options"), padding=4)
        r_opts.pack(fill='x', padx=3, pady=3)
        r_opts.columnconfigure(0, weight=1)

        self.remove_all = tk.BooleanVar(value=True)
        _cb_rem_s = ttk.Checkbutton(r_opts, text=t("remove_sig_cb"),
                       variable=self.remove_all, state='disabled')
        _cb_rem_s.grid(row=0, column=0, sticky='w', pady=1)
        self._tip(_cb_rem_s, "tip_remove_files")
        ttk.Label(r_opts, text=t("remove_sig_info"),
                 foreground="blue", font=('TkDefaultFont', 7)).grid(row=1, column=0, columnspan=2, sticky='w', pady=1)
        self.remove_verbose = tk.BooleanVar()
        _cb_rem_v = ttk.Checkbutton(r_opts, text=t("lbl_verbose"), variable=self.remove_verbose)
        _cb_rem_v.grid(row=2, column=0, sticky='w', pady=1)
        self._tip(_cb_rem_v, "tip_sign_verbose")

        def _exec_remove():
            self.execute_remove()
            inner.select(result_tab)
        r_action_frame = ttk.Frame(remove_frame)
        r_action_frame.pack(fill='x', padx=3, pady=4)
        _btn_rem = ttk.Button(r_action_frame, text=t("btn_remove_sigs"), command=_exec_remove, style='Accent.TButton')
        _btn_rem.pack(side='left', padx=5)
        self._tip(_btn_rem, "tip_remove_files")

    def create_batch_tab(self):
        """Zakładka BATCH - wykonywanie wielu operacji z pliku odpowiedzi"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=t("tab_batch"))
        
        inner = ttk.Notebook(frame)
        self._inner_batch = inner
        inner.pack(fill='both', expand=True)
        options_tab = ttk.Frame(inner)
        result_tab = ttk.Frame(inner)
        inner.add(options_tab, text=t("tab_options"))
        inner.add(result_tab, text=t("tab_result"))
        
        self.batch_output = scrolledtext.ScrolledText(result_tab, wrap=tk.WORD)
        self.batch_output.pack(fill='both', expand=True, padx=3, pady=3)
        
        options_tab.rowconfigure(0, weight=1)
        options_tab.columnconfigure(0, weight=1)
        
        info_frame = ttk.LabelFrame(options_tab, text=t("batch_info_frame"), padding=5)
        info_frame.pack(fill='x', padx=3, pady=3)
        
        ttk.Label(info_frame, text=t("batch_info_text"), justify='left', font=('TkDefaultFont', 8)).pack()
        
        # Edytor
        editor_frame = ttk.LabelFrame(options_tab, text=t("batch_editor_frame"), padding=5)
        editor_frame.pack(fill='both', expand=True, padx=3, pady=3)
        
        btn_toolbar = ttk.Frame(editor_frame)
        btn_toolbar.pack(fill='x', pady=(0, 3))
        
        ttk.Button(btn_toolbar, text=t("btn_load_file"), 
                  command=self.load_response_file).pack(side='left', padx=2)
        ttk.Button(btn_toolbar, text=t("btn_save_file"), 
                  command=self.save_response_file).pack(side='left', padx=2)
        ttk.Button(btn_toolbar, text=t("btn_clear"), 
                  command=self.clear_response_file).pack(side='left', padx=2)
        
        self.batch_editor = scrolledtext.ScrolledText(editor_frame, height=10, wrap=tk.NONE)
        self.batch_editor.pack(fill='both', expand=True)
        self._tip(self.batch_editor, "tip_batch_editor")

        def _exec_batch():
            self.execute_batch()
            inner.select(result_tab)

        action_frame = ttk.Frame(options_tab)
        action_frame.pack(fill='x', padx=3, pady=5)
        _btn_batch = ttk.Button(action_frame, text=t("btn_exec_batch"),
                  command=_exec_batch, style='Accent.TButton')
        _btn_batch.pack(side='left', padx=5)
        self._tip(_btn_batch, "tip_batch_exec")
    
    def create_certgen_tab(self):
        """Zakładka generowania certyfikatów (self-signed, CA, łańcuch)"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=t("tab_certgen"))

        inner = ttk.Notebook(frame)
        self._inner_certgen = inner
        inner.pack(fill='both', expand=True)

        options_tab = ttk.Frame(inner)
        result_tab  = ttk.Frame(inner)
        inner.add(options_tab, text=t("tab_options"))
        inner.add(result_tab, text=t("tab_result"))

        self.certgen_output = scrolledtext.ScrolledText(result_tab, wrap=tk.WORD)
        self.certgen_output.pack(fill='both', expand=True, padx=3, pady=3)

        canvas = tk.Canvas(options_tab)
        scrollbar = ttk.Scrollbar(options_tab, orient="vertical", command=canvas.yview)
        sf = ttk.Frame(canvas)
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _resize(event):
            items = canvas.find_all()
            if items:
                canvas.itemconfig(items[0], width=event.width)
        canvas.bind("<Configure>", _resize)
        canvas.bind("<Enter>",  lambda e: canvas.bind_all("<MouseWheel>",
                    lambda ev: canvas.yview_scroll(int(-1*(ev.delta/120)), "units")))
        canvas.bind("<Leave>",  lambda e: canvas.unbind_all("<MouseWheel>"))

        options_tab.rowconfigure(0, weight=1)
        options_tab.columnconfigure(0, weight=1)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        method_frame = ttk.LabelFrame(sf, text=t("certgen_method_frame"), padding=5)
        method_frame.pack(fill='x', padx=3, pady=3)

        self.certgen_method = tk.StringVar(value="openssl")
        _rb_ossl = ttk.Radiobutton(method_frame, text=t("certgen_ossl"),
                        variable=self.certgen_method, value="openssl",
                        command=self._certgen_toggle_method)
        _rb_ossl.pack(anchor='w')
        self._tip(_rb_ossl, "tip_certgen_openssl")
        _rb_ps = ttk.Radiobutton(method_frame, text=t("certgen_ps"),
                        variable=self.certgen_method, value="powershell",
                        command=self._certgen_toggle_method)
        _rb_ps.pack(anchor='w')
        self._tip(_rb_ps, "tip_certgen_install")

        openssl_row = ttk.Frame(method_frame)
        openssl_row.pack(fill='x', pady=(4, 0))
        self._certgen_openssl_row = openssl_row
        ttk.Label(openssl_row, text=t("certgen_ossl_path")).pack(side='left')
        self.certgen_openssl_path = ttk.Entry(openssl_row, width=38)
        self.certgen_openssl_path.insert(0, self._find_openssl())
        self.certgen_openssl_path.pack(side='left', padx=4)
        self._tip(self.certgen_openssl_path, "tip_certgen_openssl")
        ttk.Button(openssl_row, text="...", width=3,
                   command=lambda: self.browse_file(self.certgen_openssl_path,
                                                    "openssl.exe", "openssl.exe")).pack(side='left')

        type_frame = ttk.LabelFrame(sf, text=t("certgen_type_frame"), padding=5)
        type_frame.pack(fill='x', padx=3, pady=3)

        self.certgen_type = tk.StringVar(value="self_signed")
        _rb_self = ttk.Radiobutton(type_frame, text=t("certgen_self"),
                        variable=self.certgen_type, value="self_signed",
                        command=self._certgen_toggle_type)
        _rb_self.pack(anchor='w')
        self._tip(_rb_self, "tip_certgen_type_self")
        _rb_ca = ttk.Radiobutton(type_frame, text=t("certgen_ca"),
                        variable=self.certgen_type, value="root_ca",
                        command=self._certgen_toggle_type)
        _rb_ca.pack(anchor='w')
        self._tip(_rb_ca, "tip_certgen_type_ca")
        _rb_signed = ttk.Radiobutton(type_frame, text=t("certgen_signed"),
                        variable=self.certgen_type, value="signed_by_ca",
                        command=self._certgen_toggle_type)
        _rb_signed.pack(anchor='w')
        self._tip(_rb_signed, "tip_certgen_type_signed")

        subj_frame = ttk.LabelFrame(sf, text=t("certgen_subj_frame"), padding=5)
        subj_frame.pack(fill='x', padx=3, pady=3)
        subj_frame.columnconfigure(1, weight=1)

        fields = [
            ("certgen_lbl_cn",      "certgen_cn",      "MojaFirma",              "tip_certgen_cn"),
            ("certgen_lbl_org",     "certgen_org",     "MojaFirma Sp. z o.o.",   None),
            ("certgen_lbl_country", "certgen_country", "PL",                     "tip_certgen_country"),
            ("certgen_lbl_city",    "certgen_city",    "Warszawa",               None),
            ("certgen_lbl_state",   "certgen_state",   "Mazowieckie",            None),
            ("certgen_lbl_email",   "certgen_email",   "",                       None),
        ]
        for r, (lbl_key, attr, default, tip_key) in enumerate(fields):
            ttk.Label(subj_frame, text=t(lbl_key)).grid(row=r, column=0, sticky='w', pady=1, padx=(0,6))
            entry = ttk.Entry(subj_frame, width=38)
            entry.insert(0, default)
            entry.grid(row=r, column=1, sticky='ew', pady=1)
            setattr(self, attr, entry)
            if tip_key:
                self._tip(entry, tip_key)

        crypto_frame = ttk.LabelFrame(sf, text=t("certgen_crypto_frame"), padding=5)
        crypto_frame.pack(fill='x', padx=3, pady=3)
        crypto_frame.columnconfigure(1, weight=1)

        ttk.Label(crypto_frame, text=t("certgen_key_alg")).grid(row=0, column=0, sticky='w', pady=1)
        self.certgen_key_alg = ttk.Combobox(crypto_frame,
                                             values=["RSA", "EC"], width=10, state='readonly')
        self.certgen_key_alg.set("RSA")
        self.certgen_key_alg.grid(row=0, column=1, sticky='w', pady=1)
        self.certgen_key_alg.bind("<<ComboboxSelected>>", self._certgen_toggle_keyalg)
        self._tip(self.certgen_key_alg, "tip_certgen_key_alg")

        ttk.Label(crypto_frame, text=t("certgen_key_size")).grid(row=1, column=0, sticky='w', pady=1)
        self.certgen_key_size = ttk.Combobox(crypto_frame,
                                              values=["2048", "3072", "4096"], width=10, state='readonly')
        self.certgen_key_size.set("2048")
        self.certgen_key_size.grid(row=1, column=1, sticky='w', pady=1)
        self._tip(self.certgen_key_size, "tip_certgen_key_size")

        ttk.Label(crypto_frame, text=t("certgen_ec_curve")).grid(row=2, column=0, sticky='w', pady=1)
        self.certgen_ec_curve = ttk.Combobox(crypto_frame,
                                              values=["prime256v1", "secp384r1", "secp521r1"],
                                              width=14, state='readonly')
        self.certgen_ec_curve.set("prime256v1")
        self.certgen_ec_curve.grid(row=2, column=1, sticky='w', pady=1)
        self.certgen_ec_curve.grid_remove()
        self._tip(self.certgen_ec_curve, "tip_certgen_ec_curve")

        ttk.Label(crypto_frame, text=t("certgen_hash_alg")).grid(row=3, column=0, sticky='w', pady=1)
        self.certgen_hash_alg = ttk.Combobox(crypto_frame,
                                              values=["sha256", "sha384", "sha512"], width=10, state='readonly')
        self.certgen_hash_alg.set("sha256")
        self.certgen_hash_alg.grid(row=3, column=1, sticky='w', pady=1)
        self._tip(self.certgen_hash_alg, "tip_certgen_hash")

        ttk.Label(crypto_frame, text=t("certgen_validity")).grid(row=4, column=0, sticky='w', pady=1)
        self.certgen_days = ttk.Entry(crypto_frame, width=10)
        self.certgen_days.insert(0, "365")
        self.certgen_days.grid(row=4, column=1, sticky='w', pady=1)
        self._tip(self.certgen_days, "tip_certgen_days")

        san_frame = ttk.LabelFrame(sf, text=t("certgen_san_frame"), padding=5)
        san_frame.pack(fill='x', padx=3, pady=3)
        san_frame.columnconfigure(1, weight=1)

        ttk.Label(san_frame, text=t("certgen_dns"),
                  font=('TkDefaultFont', 8)).grid(row=0, column=0, sticky='nw', pady=1)
        self.certgen_san_dns = tk.Text(san_frame, height=2, width=38, font=('TkDefaultFont', 8))
        self.certgen_san_dns.grid(row=0, column=1, sticky='ew', pady=1)
        self._tip(self.certgen_san_dns, "tip_certgen_san_dns")
        ttk.Label(san_frame, text=t("certgen_dns_hint"),
                  foreground="gray", font=('TkDefaultFont', 7)).grid(row=1, column=1, sticky='w')

        ttk.Label(san_frame, text=t("certgen_ip"),
                  font=('TkDefaultFont', 8)).grid(row=2, column=0, sticky='nw', pady=1)
        self.certgen_san_ip = tk.Text(san_frame, height=2, width=38, font=('TkDefaultFont', 8))
        self.certgen_san_ip.grid(row=2, column=1, sticky='ew', pady=1)
        self._tip(self.certgen_san_ip, "tip_certgen_san_ip")
        ttk.Label(san_frame, text=t("certgen_ip_hint"),
                  foreground="gray", font=('TkDefaultFont', 7)).grid(row=3, column=1, sticky='w')

        self.certgen_ca_frame = ttk.LabelFrame(sf, text=t("certgen_ca_frame"), padding=5)
        self.certgen_ca_frame.pack(fill='x', padx=3, pady=3)
        self.certgen_ca_frame.columnconfigure(1, weight=1)

        ttk.Label(self.certgen_ca_frame, text=t("certgen_ca_cert")).grid(row=0, column=0, sticky='w', pady=1)
        self.certgen_ca_cert = ttk.Entry(self.certgen_ca_frame, width=32)
        self.certgen_ca_cert.grid(row=0, column=1, sticky='ew', pady=1)
        ttk.Button(self.certgen_ca_frame, text="...", width=3,
                   command=lambda: self.browse_file(self.certgen_ca_cert,
                                                    "Certificate files", "*.crt;*.pem;*.cer")).grid(row=0, column=2, padx=2)

        ttk.Label(self.certgen_ca_frame, text=t("certgen_ca_key")).grid(row=1, column=0, sticky='w', pady=1)
        self.certgen_ca_key  = ttk.Entry(self.certgen_ca_frame, width=32)
        self.certgen_ca_key.grid(row=1, column=1, sticky='ew', pady=1)
        ttk.Button(self.certgen_ca_frame, text="...", width=3,
                   command=lambda: self.browse_file(self.certgen_ca_key,
                                                    "Key files", "*.key;*.pem")).grid(row=1, column=2, padx=2)

        ttk.Label(self.certgen_ca_frame, text=t("certgen_ca_pass")).grid(row=2, column=0, sticky='w', pady=1)
        self.certgen_ca_key_pass = ttk.Entry(self.certgen_ca_frame, width=32, show="*")
        self.certgen_ca_key_pass.grid(row=2, column=1, sticky='ew', pady=1)

        self.certgen_ca_frame.pack_forget()

        out_frame = ttk.LabelFrame(sf, text=t("certgen_out_frame"), padding=5)
        out_frame.pack(fill='x', padx=3, pady=3)
        out_frame.columnconfigure(1, weight=1)

        ttk.Label(out_frame, text=t("certgen_out_dir")).grid(row=0, column=0, sticky='w', pady=1)
        self.certgen_outdir = ttk.Entry(out_frame, width=32)
        self.certgen_outdir.insert(0, CERT_DIR)
        self.certgen_outdir.grid(row=0, column=1, sticky='ew', pady=1)
        ttk.Button(out_frame, text="...", width=3,
                   command=self._certgen_browse_outdir).grid(row=0, column=2, padx=2)

        ttk.Label(out_frame, text=t("certgen_base_name")).grid(row=1, column=0, sticky='w', pady=1)
        self.certgen_basename = ttk.Entry(out_frame, width=20)
        self.certgen_basename.insert(0, "certyfikat")
        self.certgen_basename.grid(row=1, column=1, sticky='w', pady=1)

        ttk.Label(out_frame, text=t("certgen_pfx_pass")).grid(row=2, column=0, sticky='w', pady=1)
        self.certgen_pfx_pass = ttk.Entry(out_frame, width=20, show="*")
        self.certgen_pfx_pass.grid(row=2, column=1, sticky='w', pady=1)
        self._tip(self.certgen_pfx_pass, "tip_certgen_pfx_pass")
        ttk.Label(out_frame, text=t("certgen_pfx_hint"),
                  foreground="gray", font=('TkDefaultFont', 7)).grid(row=2, column=2, sticky='w', padx=3)

        self.certgen_export_pfx = tk.BooleanVar(value=True)
        _cb_pfx = ttk.Checkbutton(out_frame, text=t("certgen_export_pfx"),
                        variable=self.certgen_export_pfx)
        _cb_pfx.grid(row=3, column=0, columnspan=3, sticky='w', pady=1)
        self._tip(_cb_pfx, "tip_certgen_export_pfx")

        self.certgen_install = tk.BooleanVar(value=False)
        _cb_install = ttk.Checkbutton(
            out_frame, text=t("certgen_install"),
            variable=self.certgen_install)
        _cb_install.grid(row=4, column=0, columnspan=3, sticky='w', pady=1)
        self._tip(_cb_install, "tip_certgen_install")

        act_frame = ttk.Frame(sf)
        act_frame.pack(fill='x', padx=3, pady=6)

        def _exec_certgen():
            self.execute_certgen()
            inner.select(result_tab)

        def _show_certgen_cmd():
            self.show_certgen_commands()
            inner.select(result_tab)

        _btn_gen = ttk.Button(act_frame, text=t("btn_generate"),
                   command=_exec_certgen, style='Accent.TButton')
        _btn_gen.pack(side='left', padx=5)
        self._tip(_btn_gen, "tip_certgen_generate")

        _btn_show_cmd = ttk.Button(act_frame, text=t("btn_show_cmds"),
                   command=_show_certgen_cmd)
        _btn_show_cmd.pack(side='left', padx=5)
        self._tip(_btn_show_cmd, "tip_btn_show_cmd")

    def _find_openssl(self):
        """Szybkie wyszukiwanie openssl.exe (bez pełnego skanu dysku).
        Kolejność priorytetów:
          0. Zapisana konfiguracja (SignToolGUI.json)
          1. Folder obok exe / main.py  (APP_TOOLS_DIR)
          2. Folder _MEIPASS (bundlowane przez PyInstaller)
          3. Systemowy PATH (where openssl.exe)
          4. Typowe lokalizacje
        """
        # 0. Zapisana konfiguracja
        saved = self.config.get('openssl_path', '')
        if saved and os.path.exists(saved):
            return saved
        # 1. Folder obok exe / main.py
        local = os.path.join(APP_TOOLS_DIR, "openssl.exe")
        if os.path.isfile(local):
            return local
        # 2. _MEIPASS (PyInstaller bundle)
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            bundled = os.path.join(meipass, "openssl.exe")
            if os.path.isfile(bundled):
                return bundled
        # 3. PATH
        try:
            res = subprocess.run(["where", "openssl.exe"], capture_output=True, text=True, shell=True)
            if res.returncode == 0:
                p = res.stdout.strip().split("\n")[0].strip()
                if p:
                    return p
        except Exception as _e:
            pass
        candidates = [
            r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe",
            r"C:\Program Files (x86)\OpenSSL-Win32\bin\openssl.exe",
            r"C:\Program Files\Git\usr\bin\openssl.exe",
            r"C:\Program Files\Git\mingw64\bin\openssl.exe",
            r"C:\Program Files\Git\bin\openssl.exe",
            r"C:\OpenSSL-Win64\bin\openssl.exe",
            r"C:\OpenSSL-Win32\bin\openssl.exe",
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return "openssl"

    def _certgen_toggle_method(self):
        """Pokaż/ukryj wiersz ścieżki OpenSSL w zależności od wybranej metody."""
        method = self.certgen_method.get()
        if method == "openssl":
            self._certgen_openssl_row.pack(fill='x', pady=(4, 0))
        else:
            self._certgen_openssl_row.pack_forget()

    def _certgen_toggle_type(self):
        t = self.certgen_type.get()
        if t == "signed_by_ca":
            self.certgen_ca_frame.pack(fill='x', padx=3, pady=3)
        else:
            self.certgen_ca_frame.pack_forget()

    def _certgen_toggle_keyalg(self, event=None):
        if self.certgen_key_alg.get() == "EC":
            self.certgen_key_size.grid_remove()
            self.certgen_ec_curve.grid()
        else:
            self.certgen_ec_curve.grid_remove()
            self.certgen_key_size.grid()

    def _certgen_browse_outdir(self):
        d = filedialog.askdirectory(title="Wybierz folder wyjściowy")
        if d:
            self.certgen_outdir.delete(0, tk.END)
            self.certgen_outdir.insert(0, d)

    def _certgen_subject(self):
        parts = []
        if self.certgen_country.get():
            parts.append(f"C={self.certgen_country.get()}")
        if self.certgen_state.get():
            parts.append(f"ST={self.certgen_state.get()}")
        if self.certgen_city.get():
            parts.append(f"L={self.certgen_city.get()}")
        if self.certgen_org.get():
            parts.append(f"O={self.certgen_org.get()}")
        if self.certgen_cn.get():
            parts.append(f"CN={self.certgen_cn.get()}")
        if self.certgen_email.get():
            parts.append(f"emailAddress={self.certgen_email.get()}")
        return "/" + "/".join(parts) if parts else "/CN=MyCert"

    def _certgen_san_ext(self):
        dns_lines = [l.strip() for l in self.certgen_san_dns.get("1.0", tk.END).splitlines() if l.strip()]
        ip_lines  = [l.strip() for l in self.certgen_san_ip.get("1.0",  tk.END).splitlines() if l.strip()]
        items = [f"DNS:{d}" for d in dns_lines] + [f"IP:{i}" for i in ip_lines]
        return ",".join(items) if items else None

    def _build_openssl_commands(self):
        ossl   = self.certgen_openssl_path.get().strip() or "openssl"
        outdir = self.certgen_outdir.get().strip()
        base   = self.certgen_basename.get().strip() or "certyfikat"
        days   = self.certgen_days.get().strip() or "365"
        hash_  = self.certgen_hash_alg.get()
        subj   = self._certgen_subject()
        san    = self._certgen_san_ext()
        typ    = self.certgen_type.get()
        pfx_pass = self.certgen_pfx_pass.get()

        key_path  = os.path.join(outdir, f"{base}.key")
        crt_path  = os.path.join(outdir, f"{base}.crt")
        csr_path  = os.path.join(outdir, f"{base}.csr")
        pfx_path  = os.path.join(outdir, f"{base}.pfx")

        steps = []

        if self.certgen_key_alg.get() == "EC":
            curve = self.certgen_ec_curve.get()
            steps.append(("Generowanie klucza EC",
                           [ossl, "ecparam", "-genkey", "-name", curve, "-noout", "-out", key_path]))
        else:
            bits = self.certgen_key_size.get()
            steps.append(("Generowanie klucza RSA",
                           [ossl, "genrsa", "-out", key_path, bits]))

        if typ == "self_signed":
            cmd = [ossl, "req", "-new", "-x509",
                   "-key", key_path, "-out", crt_path,
                   "-days", days, f"-{hash_}", "-subj", subj,
                   "-addext", "extendedKeyUsage=codeSigning",
                   "-addext", "keyUsage=digitalSignature"]
            if san:
                cmd += ["-addext", f"subjectAltName={san}"]
            steps.append(("Generowanie self-signed certyfikatu", cmd))

        elif typ == "root_ca":
            cmd = [ossl, "req", "-new", "-x509",
                   "-key", key_path, "-out", crt_path,
                   "-days", days, f"-{hash_}", "-subj", subj,
                   "-addext", "basicConstraints=critical,CA:TRUE",
                   "-addext", "keyUsage=critical,keyCertSign,cRLSign"]
            steps.append(("Generowanie certyfikatu Root CA", cmd))

        elif typ == "signed_by_ca":
            ca_cert = self.certgen_ca_cert.get().strip()
            ca_key  = self.certgen_ca_key.get().strip()
            ca_pass = self.certgen_ca_key_pass.get().strip()

            csr_cmd = [ossl, "req", "-new", "-key", key_path,
                       "-out", csr_path, f"-{hash_}", "-subj", subj]
            steps.append(("Generowanie CSR", csr_cmd))

            # Zapisz rozszerzenia do pliku tymczasowego (zamiast /dev/stdin – niekompatybilne z Windows)
            ext_content = "extendedKeyUsage=codeSigning\nkeyUsage=digitalSignature\n"
            if san:
                ext_content += f"subjectAltName={san}\n"
            ext_tmp = tempfile.NamedTemporaryFile(
                mode='w', suffix='.ext', delete=False,
                dir=outdir, prefix='_signtool_ext_'
            )
            ext_tmp.write(ext_content)
            ext_tmp.close()
            ext_file_path = ext_tmp.name

            sign_cmd = [ossl, "x509", "-req",
                        "-in", csr_path, "-CA", ca_cert, "-CAkey", ca_key,
                        "-CAcreateserial", "-out", crt_path, "-days", days, f"-{hash_}",
                        "-extfile", ext_file_path]
            if ca_pass:
                sign_cmd += ["-passin", f"pass:{ca_pass}"]
            steps.append(("Podpisanie przez CA", (sign_cmd, ext_file_path)))

        if self.certgen_export_pfx.get():
            pfx_cmd = [ossl, "pkcs12", "-export",
                       "-out", pfx_path, "-inkey", key_path, "-in", crt_path,
                       "-passout", f"pass:{pfx_pass}"]
            steps.append(("Eksport do PFX", pfx_cmd))

        return steps, key_path, crt_path, pfx_path

    def _build_powershell_commands(self):
        outdir   = self.certgen_outdir.get().strip()
        base     = self.certgen_basename.get().strip() or "certyfikat"
        days     = int(self.certgen_days.get().strip() or "365")
        cn       = self.certgen_cn.get().strip() or "MyCert"
        pfx_pass = self.certgen_pfx_pass.get().strip()
        pfx_path = os.path.join(outdir, f"{base}.pfx").replace("/", "\\")
        crt_path = os.path.join(outdir, f"{base}.crt").replace("/", "\\")
        typ = self.certgen_type.get()

        lines = ["$ErrorActionPreference = 'Stop'"]
        not_after = f"(Get-Date).AddDays({days})"
        cert_store = "Cert:\\CurrentUser\\My"

        if typ == "root_ca":
            lines.append(
                f'$cert = New-SelfSignedCertificate -Subject "CN={cn}" '
                f'-CertStoreLocation "{cert_store}" '
                f'-KeyUsage CertSign,CRLSign -IsCA $true -NotAfter {not_after}'
            )
        else:
            lines.append(
                f'$cert = New-SelfSignedCertificate -Subject "CN={cn}" '
                f'-CertStoreLocation "{cert_store}" '
                f'-Type CodeSigningCert -HashAlgorithm SHA256 -NotAfter {not_after}'
            )

        if pfx_pass:
            lines.append(f'$pw = ConvertTo-SecureString -String "{pfx_pass}" -Force -AsPlainText')
        else:
            lines.append('$pw = (New-Object System.Security.SecureString)')

        lines.append(f'Export-PfxCertificate -Cert $cert -FilePath "{pfx_path}" -Password $pw | Out-Null')
        lines.append(f'Export-Certificate -Cert $cert -FilePath "{crt_path}" -Type CERT | Out-Null')
        lines.append(f'Write-Host "Certyfikat zapisany: {pfx_path}"')
        lines.append(f'Write-Host "Certyfikat (CRT): {crt_path}"')

        return "\n".join(lines), pfx_path, crt_path

    def show_certgen_commands(self):
        out = self.certgen_output
        out.delete(1.0, tk.END)
        method = self.certgen_method.get()
        if method == "openssl":
            try:
                steps, key_path, crt_path, pfx_path = self._build_openssl_commands()
            except Exception as e:
                out.insert(tk.END, f"Command build error: {e}\n")
                return
            out.insert(tk.END, "=== KOMENDY OPENSSL ===\n\n")
            for desc, cmd_or_tuple in steps:
                out.insert(tk.END, f"# {desc}\n")
                if isinstance(cmd_or_tuple, tuple):
                    cmd, ext_file_path = cmd_or_tuple
                    out.insert(tk.END, f"# (plik rozszerzeń: {ext_file_path})\n")
                    out.insert(tk.END, " ".join(f'"{a}"' if ' ' in a else a for a in cmd) + "\n\n")
                else:
                    out.insert(tk.END, " ".join(f'"{a}"' if ' ' in a else a for a in cmd_or_tuple) + "\n\n")
            out.insert(tk.END, f"\nKlucz: {key_path}\nCert:  {crt_path}\nPFX:   {pfx_path}\n")
        else:
            script, pfx_path, crt_path = self._build_powershell_commands()
            out.insert(tk.END, "=== SKRYPT POWERSHELL ===\n\n")
            out.insert(tk.END, script)
            out.insert(tk.END, f"\n\nPFX: {pfx_path}\nCRT: {crt_path}\n")

    def execute_certgen(self):
        if not self.certgen_cn.get().strip():
            messagebox.showwarning("Missing data", t("msg_no_cn"))
            return
        outdir = self.certgen_outdir.get().strip()
        if not outdir or not os.path.isdir(outdir):
            messagebox.showwarning(t("msg_no_outdir"), t("msg_outdir_missing"))
            return

        # Walidacja pola Kraj (musi mieć 2 litery)
        country = self.certgen_country.get().strip()
        if country and (len(country) != 2 or not country.isalpha()):
            messagebox.showerror("Błąd walidacji", "Kod kraju musi składać się z dokładnie 2 liter (np. PL, US).")
            return

        # Walidacja liczby dni (musi być dodatnią liczbą całkowitą)
        days_str = self.certgen_days.get().strip()
        try:
            days_int = int(days_str)
            if days_int <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Błąd walidacji", "Ważność certyfikatu musi być dodatnią liczbą całkowitą (dni).")
            return

        # Walidacja e-maila (podstawowa)
        email = self.certgen_email.get().strip()
        if email and "@" not in email:
            messagebox.showerror("Błąd walidacji", "Podany adres e-mail jest nieprawidłowy.")
            return

        method = self.certgen_method.get()
        out = self.certgen_output

        def safe_insert(text):
            self.root.after(0, lambda t=text: out.insert(tk.END, t))

        def safe_see():
            self.root.after(0, lambda: out.see(tk.END))

        def safe_status(text):
            self.root.after(0, lambda t=text: self.status_bar.config(text=t))

        def safe_clear():
            self.root.after(0, lambda: out.delete(1.0, tk.END))

        def run_openssl():
            try:
                steps, key_path, crt_path, pfx_path = self._build_openssl_commands()
            except Exception as e:
                safe_insert(f"Command build error: {e}\n")
                return

            safe_clear()
            safe_status(t("certgen_gen_status"))
            safe_insert("=== GENEROWANIE CERTYFIKATU (OpenSSL) ===\n\n")
            all_ok = True
            ext_tmp_files = []  # pliki tymczasowe do usunięcia po zakończeniu

            for desc, cmd_or_tuple in steps:
                safe_insert(f"▶ {desc}...\n")
                safe_see()

                # Rozróżnij typ kroku: (cmd, ext_file_path) lub zwykły cmd
                if isinstance(cmd_or_tuple, tuple):
                    cmd, ext_file_path = cmd_or_tuple
                    ext_tmp_files.append(ext_file_path)
                    stdin_bytes = None
                else:
                    cmd = cmd_or_tuple
                    stdin_bytes = None

                safe_insert("  " + " ".join(f'"{a}"' if ' ' in a else a for a in cmd) + "\n")
                try:
                    proc = subprocess.Popen(
                        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        stdin=None, text=False)
                    stdout_data, _ = proc.communicate()
                    output_text = stdout_data.decode('utf-8', errors='replace')
                    if output_text.strip():
                        safe_insert(output_text)
                    if proc.returncode == 0:
                        safe_insert("  ✓ OK\n\n")
                    else:
                        safe_insert(f"  ✗ Error! Code: {proc.returncode}\n\n")
                        all_ok = False
                        break
                except FileNotFoundError:
                    safe_insert(f"  ✗ Nie znaleziono: {cmd[0]}\n     Zainstaluj OpenSSL lub podaj właściwą ścieżkę.\n\n")
                    all_ok = False
                    break
                except Exception as e:
                    safe_insert(f"  ✗ Exception: {e}\n\n")
                    all_ok = False
                    break

            # Usuń pliki tymczasowe rozszerzeń
            for tmp in ext_tmp_files:
                try:
                    os.unlink(tmp)
                except Exception as _e:
                    pass

            if all_ok:
                safe_insert(f"✓ Certyfikat wygenerowany pomyślnie!\n  Klucz: {key_path}\n  Cert:  {crt_path}\n")
                if self.certgen_export_pfx.get():
                    safe_insert(f"  PFX:   {pfx_path}\n")
                safe_status(t("certgen_success_status"))
                if self.certgen_install.get() and self.certgen_export_pfx.get():
                    safe_insert("\n▶ Instalowanie PFX w magazynie Windows...\n")
                    pfx_pass = self.certgen_pfx_pass.get()
                    ps_cmd = (
                        f'$pw = ConvertTo-SecureString -String "{pfx_pass}" -Force -AsPlainText; '
                        f'Import-PfxCertificate -FilePath "{pfx_path}" '
                        f'-CertStoreLocation Cert:\\CurrentUser\\My -Password $pw'
                    )
                    try:
                        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd],
                                             capture_output=True, text=True)
                        if res.returncode == 0:
                            safe_insert("  ✓ Zainstalowano w magazynie Cert:\\CurrentUser\\My\n")
                        else:
                            safe_insert(f"  ✗ Installation error:\n{res.stderr}\n")
                    except Exception as e:
                        safe_insert(f"  ✗ Wyjątek podczas instalacji: {e}\n")
            else:
                safe_status(t("certgen_error_status"))

        def run_powershell():
            safe_clear()
            safe_status(t("certgen_gen_ps_status"))
            safe_insert("=== GENEROWANIE CERTYFIKATU (PowerShell) ===\n\n")
            try:
                script, pfx_path, crt_path = self._build_powershell_commands()
                safe_insert(script + "\n\n")
                proc = subprocess.Popen(
                    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding='utf-8', errors='replace')
                for line in proc.stdout:
                    safe_insert(line)
                    safe_see()
                proc.wait()
                if proc.returncode == 0:
                    safe_insert(f"\n✓ Success!\n  PFX: {pfx_path}\n  CRT: {crt_path}\n")
                    safe_status(t("certgen_success_status"))
                else:
                    safe_insert(f"\n✗ Error! Kod: {proc.returncode}\n")
                    safe_status(t("certgen_error_status"))
            except Exception as e:
                safe_insert(f"\n✗ Exception: {e}\n")
                safe_status(t("status_error"))

        if method == "openssl":
            threading.Thread(target=run_openssl, daemon=True).start()
        else:
            threading.Thread(target=run_powershell, daemon=True).start()

    # === METODY POMOCNICZE ===
    
    def browse_file(self, entry_widget, file_type, pattern):
        """Otwórz dialog wyboru pliku"""
        filename = filedialog.askopenfilename(
            title=f"Wybierz plik {file_type}",
            filetypes=[(file_type, pattern), ("All files", "*.*")]
        )
        if filename:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filename)
    
    def add_sign_files(self):
        """Dodaj pliki do podpisania"""
        files = filedialog.askopenfilenames(
            title="Wybierz pliki do podpisania",
            filetypes=[("Pliki wykonywalne", "*.exe;*.dll;*.sys;*.cat;*.msi"), 
                      ("All files", "*.*")]
        )
        for f in files:
            if f not in self.sign_files:
                self.sign_files.append(f)
                self.sign_files_listbox.insert(tk.END, os.path.basename(f))
    
    def remove_sign_files(self):
        """Usuń zaznaczone pliki"""
        selection = self.sign_files_listbox.curselection()
        for index in reversed(selection):
            self.sign_files_listbox.delete(index)
            del self.sign_files[index]
    
    def clear_sign_files(self):
        """Wyczyść listę plików"""
        self.sign_files_listbox.delete(0, tk.END)
        self.sign_files.clear()
    
    def add_ts_files(self):
        """Dodaj pliki do timestamp"""
        files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=[("Pliki wykonywalne", "*.exe;*.dll;*.sys"), ("All files", "*.*")]
        )
        for f in files:
            if f not in self.ts_files:
                self.ts_files.append(f)
                self.ts_files_listbox.insert(tk.END, os.path.basename(f))
    
    def remove_ts_files(self):
        selection = self.ts_files_listbox.curselection()
        for index in reversed(selection):
            self.ts_files_listbox.delete(index)
            del self.ts_files[index]
    
    def add_verify_files(self):
        """Dodaj pliki do weryfikacji"""
        files = filedialog.askopenfilenames(
            title="Select files to verify",
            filetypes=[("Pliki wykonywalne", "*.exe;*.dll;*.sys"), ("All files", "*.*")]
        )
        for f in files:
            if f not in self.verify_files:
                self.verify_files.append(f)
                self.verify_files_listbox.insert(tk.END, os.path.basename(f))
    
    def remove_verify_files(self):
        selection = self.verify_files_listbox.curselection()
        for index in reversed(selection):
            self.verify_files_listbox.delete(index)
            del self.verify_files[index]
    
    def add_remove_files(self):
        """Dodaj pliki do usunięcia podpisów"""
        files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=[("Pliki wykonywalne", "*.exe;*.dll;*.sys"), ("All files", "*.*")]
        )
        for f in files:
            if f not in self.remove_files:
                self.remove_files.append(f)
                self.remove_files_listbox.insert(tk.END, os.path.basename(f))
    
    def remove_remove_files(self):
        selection = self.remove_files_listbox.curselection()
        for index in reversed(selection):
            self.remove_files_listbox.delete(index)
            del self.remove_files[index]
    
    # === BUDOWANIE KOMEND ===
    
    def build_sign_command(self):
        """Zbuduj komendę sign - ZAKTUALIZOWANA W FAZIE 1"""
        if not self.sign_files:
            return None

        # Walidacja SHA1 (musi być 40 hex znaków jeśli podane)
        sha1_val = self.sign_cert_sha1.get().strip()
        if sha1_val and (len(sha1_val) != 40 or not all(c in '0123456789abcdefABCDEF' for c in sha1_val)):
            messagebox.showerror("Błąd walidacji", "SHA1 certyfikatu musi mieć dokładnie 40 znaków szesnastkowych.")
            return None

        # Walidacja URL timestampu
        ts_url = self.sign_timestamp.get().strip()
        if ts_url and not (ts_url.startswith("http://") or ts_url.startswith("https://")):
            messagebox.showerror("Błąd walidacji", "URL serwera timestamp musi zaczynać się od http:// lub https://")
            return None

        cmd = [self.signtool_path, "sign"]
        
        # Certyfikat
        cert_provided = False
        if self.sign_cert_method.get() == "store":
            if self.sign_cert_name.get():
                cmd.extend(["/n", self.sign_cert_name.get()])
                cert_provided = True
            if self.sign_cert_sha1.get():
                cmd.extend(["/sha1", self.sign_cert_sha1.get()])
                cert_provided = True
        else:
            if self.sign_cert_file.get():
                cmd.extend(["/f", self.sign_cert_file.get()])
                cert_provided = True
            if self.sign_cert_password.get():
                cmd.extend(["/p", self.sign_cert_password.get()])
        
        # Ostrzeżenie gdy brak certyfikatu (fix: brak walidacji)
        if not cert_provided:
            answer = messagebox.askyesno(
                t("msg_no_cert"),
                t("msg_no_cert_body"),
                icon='warning'
            )
            if not answer:
                return None
        
        # ===== FAZA 1: DODATKOWY CERTYFIKAT =====
        if self.sign_additional_cert.get():
            cmd.extend(["/ac", self.sign_additional_cert.get()])
        
        # Algorytm hash
        if self.sign_hash_alg.get():
            cmd.extend(["/fd", self.sign_hash_alg.get()])
        
        # Opis i URL
        if self.sign_description.get():
            cmd.extend(["/d", self.sign_description.get()])
        if self.sign_url.get():
            cmd.extend(["/du", self.sign_url.get()])
        
        # ===== FAZA 1: TIMESTAMP Z WYBOREM METODY =====
        if self.sign_timestamp.get():
            if self.sign_timestamp_method.get() == "rfc3161":
                # RFC3161 - nowoczesny
                cmd.extend(["/tr", self.sign_timestamp.get()])
                if self.sign_timestamp_alg.get():
                    cmd.extend(["/td", self.sign_timestamp_alg.get()])
            else:
                # Authenticode - legacy
                cmd.extend(["/t", self.sign_timestamp.get()])
        
        # Dodatkowe opcje
        if self.sign_append.get():
            cmd.append("/as")
        if self.sign_verbose.get():
            cmd.append("/v")
        if self.sign_debug.get():
            cmd.append("/debug")
        
        # Pliki
        cmd.extend(self.sign_files)
        
        return cmd
    
    def build_timestamp_command(self):
        """Zbuduj komendę timestamp - ZAKTUALIZOWANA W FAZIE 1"""
        if not self.ts_files or not self.ts_server.get():
            return None
        
        cmd = [self.signtool_path, "timestamp"]
        
        # ===== FAZA 1: WYBÓR METODY TIMESTAMP =====
        if self.ts_timestamp_method.get() == "rfc3161":
            # RFC3161 - nowoczesny
            cmd.extend(["/tr", self.ts_server.get()])
            if self.ts_hash_alg.get():
                cmd.extend(["/td", self.ts_hash_alg.get()])
        else:
            # Authenticode - legacy
            cmd.extend(["/t", self.ts_server.get()])
        
        if self.ts_verbose.get():
            cmd.append("/v")
        
        cmd.extend(self.ts_files)
        
        return cmd
    
    def build_verify_command(self):
        """Zbuduj komendę verify"""
        if not self.verify_files:
            return None
        
        cmd = [self.signtool_path, "verify"]
        
        if self.verify_pa.get():
            cmd.append("/pa")
        if self.verify_pg.get():
            cmd.append("/pg")
        if self.verify_verbose.get():
            cmd.append("/v")
        if self.verify_catalog.get():
            cmd.extend(["/c", self.verify_catalog.get()])
        
        cmd.extend(self.verify_files)
        
        return cmd
    
    def build_catdb_command(self):
        """Zbuduj komendę catdb"""
        if not self.catdb_file.get():
            return None

        cmd = [self.signtool_path, "catdb", "/d"]

        if "Usuń" in self.catdb_action.get() or "/r" in self.catdb_action.get():
            cmd.append("/r")
        else:
            # /u = utwórz unikalny ID dla katalogu (flaga bez argumentu)
            cmd.append("/u")

        # plik katalogu zawsze jako ostatni argument pozycyjny
        cmd.append(self.catdb_file.get())

        if self.catdb_verbose.get():
            cmd.append("/v")

        return cmd
    
    def build_remove_command(self):
        """Zbuduj komendę remove"""
        if not self.remove_files:
            return None
        
        cmd = [self.signtool_path, "remove"]
        
        # /s usuwa podpisy Authenticode - signtool remove zawsze wymaga tej flagi
        cmd.append("/s")
        
        if self.remove_verbose.get():
            cmd.append("/v")
        
        cmd.extend(self.remove_files)
        
        return cmd
    
    # === EXECUTING COMMANDS ===

    @staticmethod
    def _setup_output_tags(widget):
        """Configure color tags for a ScrolledText output widget."""
        widget.tag_configure("cmd",     foreground="#00cfff",  font=("Consolas", 9, "bold"))
        widget.tag_configure("success", foreground="#22dd55",  font=("Consolas", 9, "bold"))
        widget.tag_configure("error",   foreground="#ff4444",  font=("Consolas", 9, "bold"))
        widget.tag_configure("warning", foreground="#ffaa00",  font=("Consolas", 9))
        widget.tag_configure("info",    foreground="#aaaacc",  font=("Consolas", 9))
        widget.tag_configure("normal",  foreground="#cccccc",  font=("Consolas", 9))
        widget.configure(bg="#0d1117", insertbackground="#cccccc")

    @staticmethod
    def _classify_line(line):
        """Return a tag name based on line content."""
        lo = line.lower()
        if any(k in lo for k in ("error", "failed", "failure", "invalid", "not found",
                                  "cannot", "unable", "denied", "✗", "błąd")):
            return "error"
        if any(k in lo for k in ("successfully", "success", "verified", "passed",
                                  "signed", "✓", "added", "removed")):
            return "success"
        if any(k in lo for k in ("warning", "warn", "caution")):
            return "warning"
        if line.startswith("Executing:") or line.startswith(">>>") or line.startswith("---"):
            return "cmd"
        return "normal"

    def run_command(self, cmd, output_widget):
        """Run a command in a background thread with colored output and Stop support."""
        self._setup_output_tags(output_widget)

        def safe_insert(text, tag="normal"):
            self.root.after(0, lambda t=text, tg=tag: output_widget.insert(tk.END, t, tg))

        def safe_see():
            self.root.after(0, lambda: output_widget.see(tk.END))

        def safe_status(text):
            self.root.after(0, lambda: self.status_bar.config(text=text))

        def safe_clear():
            self.root.after(0, lambda: output_widget.delete(1.0, tk.END))

        # Referencja do bieżącego procesu – umożliwia anulowanie przez stop_current_process()
        self._current_process = None

        def thread_func():
            try:
                safe_status(t("status_running"))
                safe_clear()
                cmd_str = ' '.join(f'"{a}"' if ' ' in a else a for a in cmd)
                safe_insert(f"Executing: {cmd_str}\n", "cmd")
                safe_insert("─" * 72 + "\n", "info")

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                self._current_process = process

                for line in process.stdout:
                    tag = self._classify_line(line)
                    safe_insert(line, tag)
                    safe_see()

                process.wait()
                self._current_process = None

                safe_insert("─" * 72 + "\n", "info")
                if process.returncode == 0:
                    safe_insert("\n  ✓  Success  (exit code 0)\n", "success")
                    safe_status(t("status_ready_ok"))
                else:
                    safe_insert(f"\n  ✗  Error  (exit code {process.returncode})\n", "error")
                    safe_status(f"{t('status_error')} (code: {process.returncode})")

            except Exception as e:
                self._current_process = None
                safe_insert(f"\n  ✗  Exception: {str(e)}\n", "error")
                safe_status(t("status_error"))

        thread = threading.Thread(target=thread_func, daemon=True)
        thread.start()

    def stop_current_process(self):
        """Anuluj aktualnie wykonywaną komendę signtool."""
        proc = getattr(self, '_current_process', None)
        if proc and proc.poll() is None:
            try:
                proc.kill()
                self.status_bar.config(text=t("status_cancelled"))
            except Exception as _e:
                pass
    
    def execute_sign(self):
        """Wykonaj podpisywanie"""
        cmd = self.build_sign_command()
        if cmd:
            self.run_command(cmd, self.sign_output)
        else:
            messagebox.showwarning("Missing data", t("msg_select_cert"))

    def show_sign_command(self):
        """Show the sign command"""
        cmd = self.build_sign_command()
        if cmd:
            cmd_str = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in cmd)
            self._setup_output_tags(self.sign_output)
            self.sign_output.delete(1.0, tk.END)
            self.sign_output.insert(tk.END, t("out_cmd_header"), "info")
            self.sign_output.insert(tk.END, cmd_str, "cmd")
            self.sign_output.insert(tk.END, t("out_cmd_footer"), "info")
        else:
            messagebox.showwarning("Missing data", t("msg_select_cert"))
    
    def execute_timestamp(self):
        """Wykonaj timestamp"""
        cmd = self.build_timestamp_command()
        if cmd:
            self.run_command(cmd, self.ts_output)
        else:
            messagebox.showwarning("Missing data", t("msg_select_ts"))

    def execute_verify(self):
        """Wykonaj weryfikację"""
        cmd = self.build_verify_command()
        if cmd:
            self.run_command(cmd, self.verify_output)
        else:
            messagebox.showwarning("Missing data", t("msg_select_verify"))

    def execute_catdb(self):
        """Wykonaj catdb"""
        cmd = self.build_catdb_command()
        if cmd:
            self.run_command(cmd, self.catdb_output)
        else:
            messagebox.showwarning("Missing data", t("msg_select_catdb"))

    def execute_remove(self):
        """Wykonaj usuwanie"""
        cmd = self.build_remove_command()
        if cmd:
            self.run_command(cmd, self.remove_output)
        else:
            messagebox.showwarning("Missing data", t("msg_select_remove"))

    def load_response_file(self):
        """Wczytaj plik odpowiedzi"""
        filename = filedialog.askopenfilename(
            title=t("dlg_response_files"),
            filetypes=[(t("dlg_text_files"), "*.txt"), (t("dlg_all_files"), "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.batch_editor.delete(1.0, tk.END)
                self.batch_editor.insert(1.0, content)
            except Exception as e:
                messagebox.showerror(t("msg_error"), t("msg_load_fail", e=e))

    def save_response_file(self):
        """Zapisz plik odpowiedzi"""
        filename = filedialog.asksaveasfilename(
            title=t("dlg_save_response"),
            defaultextension=".txt",
            filetypes=[(t("dlg_text_files"), "*.txt"), (t("dlg_all_files"), "*.*")]
        )
        if filename:
            try:
                content = self.batch_editor.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo(t("msg_success"), t("msg_file_saved"))
            except Exception as e:
                messagebox.showerror(t("msg_error"), t("msg_save_fail", e=e))

    def clear_response_file(self):
        """Wyczyść edytor"""
        self.batch_editor.delete(1.0, tk.END)

    def execute_batch(self):
        """Execute batch response file"""
        content = self.batch_editor.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Missing data", t("msg_batch_empty"))
            return

        # Write to temp file
        batch_tmp_path = os.path.join(APP_DIR, "_batch_response.txt")
        with open(batch_tmp_path, 'w', encoding='utf-8') as f:
            f.write(content)
        temp_file = batch_tmp_path

        cmd = [self.signtool_path, f"@{temp_file}"]
        self._setup_output_tags(self.batch_output)

        def run_and_cleanup():
            """Run command and delete temp file only after process finishes."""
            def safe_insert(text, tag="normal"):
                self.root.after(0, lambda t=text, tg=tag: self.batch_output.insert(tk.END, t, tg))

            def safe_see():
                self.root.after(0, lambda: self.batch_output.see(tk.END))

            def safe_status(text):
                self.root.after(0, lambda: self.status_bar.config(text=text))

            try:
                safe_status(t("status_running"))
                self.root.after(0, lambda: self.batch_output.delete(1.0, tk.END))
                safe_insert(f"Executing: {' '.join(cmd)}\n", "cmd")
                safe_insert("─" * 72 + "\n", "info")

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )

                for line in process.stdout:
                    tag = self._classify_line(line)
                    safe_insert(line, tag)
                    safe_see()

                process.wait()

                safe_insert("─" * 72 + "\n", "info")
                if process.returncode == 0:
                    safe_insert("\n  ✓  Success  (exit code 0)\n", "success")
                    safe_status(t("status_ready_ok"))
                else:
                    safe_insert(f"\n  ✗  Error  (exit code {process.returncode})\n", "error")
                    safe_status(f"{t('status_error')} (code: {process.returncode})")

            except Exception as e:
                safe_insert(f"\n  ✗  Exception: {str(e)}\n", "error")
                safe_status(t("status_error"))
            finally:
                # Delete temp file only after process ends (fix race condition)
                try:
                    os.unlink(temp_file)
                except Exception as _e:
                    pass

        thread = threading.Thread(target=run_and_cleanup, daemon=True)
        thread.start()


def main():
    root = tk.Tk()
    
    # Stylizacja
    style = ttk.Style()
    style.theme_use('clam')
    
    app = SignToolGUI(root)
    
    # Wycentruj okno
    root.update_idletasks()
    x = (root.winfo_screenwidth()  // 2) - (720 // 2)
    y = (root.winfo_screenheight() // 2) - (807 // 2)
    root.geometry(f'720x807+{x}+{y}')
    
    root.mainloop()


# ── Ukryj okno konsoli dla WSZYSTKICH subprocess.Popen na Windows ─────────────
# Bez tego każde wywołanie signtool/openssl/powershell powoduje mignięcie
# czarnego okna konsoli. CREATE_NO_WINDOW ustawiony jako domyślna flaga.
if sys.platform == "win32":
    _CREATE_NO_WINDOW = 0x08000000
    _original_popen_init = subprocess.Popen.__init__

    def _popen_no_window(self, *args, **kwargs):
        if "creationflags" not in kwargs:
            kwargs["creationflags"] = _CREATE_NO_WINDOW
        else:
            kwargs["creationflags"] |= _CREATE_NO_WINDOW
        _original_popen_init(self, *args, **kwargs)

    subprocess.Popen.__init__ = _popen_no_window


if __name__ == "__main__":
    main()