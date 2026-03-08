# -*- coding: utf-8 -*-
"""
i18n.py – Translation plugin for SignTool GUI
Supports: Polish (pl), English (en)
Usage:
    from i18n import set_language, t
    set_language("en")
    label_text = t("sign_files")

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

_LANG = "pl"

TRANSLATIONS = {
    # ── App / Window ──────────────────────────────────────────────────────────
    "app_title": {
        "pl": "SignTool GUI v2.0 - Graficzny interfejs podpisywania",
        "en": "SignTool GUI v2.0 - Code Signing GUI",
    },
    "header_subtitle": {
        "pl": "Graficzny interfejs podpisywania kodu | v2.0",
        "en": "Graphical code signing interface | v2.0",
    },
    "status_ready": {
        "pl": "Gotowy | v2.0",
        "en": "Ready | v2.0",
    },
    "status_ready_ok": {
        "pl": "Gotowy - Sukces | v2.0",
        "en": "Ready - Success | v2.0",
    },
    "status_error": {
        "pl": "Błąd | v2.0",
        "en": "Error | v2.0",
    },
    "status_running": {
        "pl": "Wykonywanie...",
        "en": "Running...",
    },

    # ── Tab labels ────────────────────────────────────────────────────────────
    "tab_sign": {
        "pl": "Sign - Podpisz",
        "en": "Sign",
    },
    "tab_ts_verify": {
        "pl": "Timestamp / Verify",
        "en": "Timestamp / Verify",
    },
    "tab_catdb_remove": {
        "pl": "CatDB / Remove",
        "en": "CatDB / Remove",
    },
    "tab_batch": {
        "pl": "Batch - Wsadowe",
        "en": "Batch",
    },
    "tab_certgen": {
        "pl": "🔑 Generuj certyfikat",
        "en": "🔑 Generate Certificate",
    },
    "tab_options": {
        "pl": "Opcje",
        "en": "Options",
    },
    "tab_result": {
        "pl": "Wynik",
        "en": "Result",
    },

    # ── Sign tab ──────────────────────────────────────────────────────────────
    "sign_files_frame": {
        "pl": "Pliki do podpisania",
        "en": "Files to sign",
    },
    "btn_add_files": {
        "pl": "Dodaj pliki",
        "en": "Add files",
    },
    "btn_remove_selected": {
        "pl": "Usuń zaznaczone",
        "en": "Remove selected",
    },
    "btn_clear": {
        "pl": "Wyczyść",
        "en": "Clear",
    },
    "cert_frame": {
        "pl": "Certyfikat",
        "en": "Certificate",
    },
    "cert_method_label": {
        "pl": "Metoda:",
        "en": "Method:",
    },
    "cert_from_store": {
        "pl": "Z magazynu certyfikatów",
        "en": "From certificate store",
    },
    "cert_from_file": {
        "pl": "Z pliku PFX",
        "en": "From PFX file",
    },
    "cert_name_label": {
        "pl": "Nazwa certyfikatu (/n):",
        "en": "Certificate name (/n):",
    },
    "cert_sha1_label": {
        "pl": "SHA1 certyfikatu (/sha1):",
        "en": "Certificate SHA1 (/sha1):",
    },
    "cert_file_label": {
        "pl": "Plik certyfikatu (/f):",
        "en": "Certificate file (/f):",
    },
    "cert_password_label": {
        "pl": "Hasło (/p):",
        "en": "Password (/p):",
    },
    "cert_additional_label": {
        "pl": "Dodatkowy certyfikat (/ac):",
        "en": "Additional certificate (/ac):",
    },
    "cert_additional_info": {
        "pl": "ℹ️ Dodatkowy certyfikat dla cross-certification",
        "en": "ℹ️ Additional certificate for cross-certification",
    },
    "sign_options_frame": {
        "pl": "Opcje podpisywania",
        "en": "Signing options",
    },
    "hash_alg_label": {
        "pl": "Algorytm hash (/fd):",
        "en": "Hash algorithm (/fd):",
    },
    "desc_label": {
        "pl": "Opis (/d):",
        "en": "Description (/d):",
    },
    "url_label": {
        "pl": "URL (/du):",
        "en": "URL (/du):",
    },
    "timestamp_server_label": {
        "pl": "Serwer timestamp:",
        "en": "Timestamp server:",
    },
    "ts_rfc3161": {
        "pl": "RFC3161 (/tr) - Nowoczesny",
        "en": "RFC3161 (/tr) - Modern",
    },
    "ts_authenticode": {
        "pl": "Authenticode (/t) - Legacy",
        "en": "Authenticode (/t) - Legacy",
    },
    "ts_info": {
        "pl": "ℹ️ RFC3161 zalecany, Authenticode dla starszych systemów",
        "en": "ℹ️ RFC3161 recommended, Authenticode for older systems",
    },
    "ts_hash_label": {
        "pl": "Timestamp hash (/td):",
        "en": "Timestamp hash (/td):",
    },
    "ts_hash_info": {
        "pl": "(tylko dla RFC3161)",
        "en": "(RFC3161 only)",
    },
    "sign_append": {
        "pl": "Dołącz podpis (/as)",
        "en": "Append signature (/as)",
    },
    "sign_verbose": {
        "pl": "Tryb szczegółowy (/v)",
        "en": "Verbose mode (/v)",
    },
    "sign_debug": {
        "pl": "Debug (/debug)",
        "en": "Debug (/debug)",
    },
    "btn_sign": {
        "pl": "Podpisz pliki",
        "en": "Sign files",
    },
    "btn_show_cmd": {
        "pl": "Pokaż komendę",
        "en": "Show command",
    },

    # ── Timestamp / Verify tab ────────────────────────────────────────────────
    "ts_result_frame": {
        "pl": "Wynik Timestamp",
        "en": "Timestamp Result",
    },
    "verify_result_frame": {
        "pl": "Wynik Verify",
        "en": "Verify Result",
    },
    "ts_section": {
        "pl": "Timestamp",
        "en": "Timestamp",
    },
    "files_frame": {
        "pl": "Pliki",
        "en": "Files",
    },
    "ts_server_label": {
        "pl": "Serwer:",
        "en": "Server:",
    },
    "ts_hash_label2": {
        "pl": "Hash (/td):",
        "en": "Hash (/td):",
    },
    "ts_rfc3161_short": {
        "pl": "RFC3161 (/tr)",
        "en": "RFC3161 (/tr)",
    },
    "ts_auth_short": {
        "pl": "Authenticode (/t)",
        "en": "Authenticode (/t)",
    },
    "ts_hash_only_rfc": {
        "pl": "(tylko RFC3161)",
        "en": "(RFC3161 only)",
    },
    "btn_add_timestamp": {
        "pl": "Dodaj timestamp",
        "en": "Add timestamp",
    },
    "verify_section": {
        "pl": "Verify",
        "en": "Verify",
    },
    "verify_pa": {
        "pl": "Weryfikuj wszystkie podpisy (/pa)",
        "en": "Verify all signatures (/pa)",
    },
    "verify_pg": {
        "pl": "Weryfikuj podpis strony (/pg)",
        "en": "Verify page signature (/pg)",
    },
    "verify_verbose": {
        "pl": "Tryb szczegółowy (/v)",
        "en": "Verbose mode (/v)",
    },
    "verify_catalog_label": {
        "pl": "Plik katalogu (/c):",
        "en": "Catalog file (/c):",
    },
    "btn_verify": {
        "pl": "Weryfikuj",
        "en": "Verify",
    },

    # ── CatDB / Remove tab ────────────────────────────────────────────────────
    "catdb_result_frame": {
        "pl": "Wynik CatDB",
        "en": "CatDB Result",
    },
    "remove_result_frame": {
        "pl": "Wynik Remove",
        "en": "Remove Result",
    },
    "catdb_section": {
        "pl": "CatDB",
        "en": "CatDB",
    },
    "catdb_desc": {
        "pl": "Dodawanie/usuwanie plików katalogów z bazy danych katalogów.",
        "en": "Adding/removing catalog files from the catalog database.",
    },
    "catdb_options": {
        "pl": "Opcje",
        "en": "Options",
    },
    "catdb_file_label": {
        "pl": "Plik katalogu:",
        "en": "Catalog file:",
    },
    "catdb_action_label": {
        "pl": "Akcja:",
        "en": "Action:",
    },
    "catdb_add": {
        "pl": "Dodaj (/u)",
        "en": "Add (/u)",
    },
    "catdb_remove_action": {
        "pl": "Usuń (/r)",
        "en": "Remove (/r)",
    },
    "catdb_verbose": {
        "pl": "Tryb szczegółowy (/v)",
        "en": "Verbose mode (/v)",
    },
    "btn_exec_catdb": {
        "pl": "Wykonaj CatDB",
        "en": "Execute CatDB",
    },
    "remove_section": {
        "pl": "Remove - Usuń podpisy",
        "en": "Remove - Delete signatures",
    },
    "remove_authenticode": {
        "pl": "Usuń podpisy Authenticode (/s) — wymagane",
        "en": "Remove Authenticode signatures (/s) — required",
    },
    "remove_info": {
        "pl": "ℹ️ signtool remove zawsze wymaga flagi /s",
        "en": "ℹ️ signtool remove always requires /s flag",
    },
    "remove_verbose": {
        "pl": "Tryb szczegółowy (/v)",
        "en": "Verbose mode (/v)",
    },
    "btn_remove_sigs": {
        "pl": "Usuń podpisy",
        "en": "Remove signatures",
    },

    # ── Batch tab ─────────────────────────────────────────────────────────────
    "batch_info_frame": {
        "pl": "Informacja",
        "en": "Information",
    },
    "batch_info_text": {
        "pl": 'Tryb wsadowy: każdy argument w osobnej linii, pierwsza linia to komenda.\nPrzykład:  sign  /n "Certyfikat"  /fd SHA256  plik.exe',
        "en": 'Batch mode: each argument on a separate line, first line is the command.\nExample:  sign  /n "Certificate"  /fd SHA256  file.exe',
    },
    "batch_editor_frame": {
        "pl": "Plik odpowiedzi",
        "en": "Response file",
    },
    "btn_load_file": {
        "pl": "Wczytaj plik",
        "en": "Load file",
    },
    "btn_save_file": {
        "pl": "Zapisz plik",
        "en": "Save file",
    },
    "btn_exec_batch": {
        "pl": "Wykonaj plik odpowiedzi",
        "en": "Execute response file",
    },

    # ── CertGen tab ───────────────────────────────────────────────────────────
    "certgen_method_frame": {
        "pl": "Metoda generowania",
        "en": "Generation method",
    },
    "certgen_openssl_method": {
        "pl": "OpenSSL  (cross-platform, zalecany)",
        "en": "OpenSSL  (cross-platform, recommended)",
    },
    "certgen_ps_method": {
        "pl": "PowerShell  New-SelfSignedCertificate  (tylko Windows, eksport do PFX)",
        "en": "PowerShell  New-SelfSignedCertificate  (Windows only, PFX export)",
    },
    "certgen_openssl_path_label": {
        "pl": "Ścieżka openssl:",
        "en": "OpenSSL path:",
    },
    "certgen_type_frame": {
        "pl": "Typ certyfikatu",
        "en": "Certificate type",
    },
    "certgen_self_signed": {
        "pl": "Self-signed  (samopodpisany, do testów)",
        "en": "Self-signed  (self-signed, for testing)",
    },
    "certgen_root_ca": {
        "pl": "Root CA  (urząd certyfikacji)",
        "en": "Root CA  (certificate authority)",
    },
    "certgen_signed_by_ca": {
        "pl": "Podpisany przez CA  (wymaga Root CA)",
        "en": "Signed by CA  (requires Root CA)",
    },
    "certgen_subject_frame": {
        "pl": "Dane certyfikatu (Subject)",
        "en": "Certificate data (Subject)",
    },
    "certgen_cn": {
        "pl": "Nazwa (CN):",
        "en": "Name (CN):",
    },
    "certgen_org": {
        "pl": "Organizacja (O):",
        "en": "Organization (O):",
    },
    "certgen_country": {
        "pl": "Kraj (C, 2 litery):",
        "en": "Country (C, 2 letters):",
    },
    "certgen_city": {
        "pl": "Miejscowość (L):",
        "en": "City (L):",
    },
    "certgen_state": {
        "pl": "Województwo (ST):",
        "en": "State/Province (ST):",
    },
    "certgen_email": {
        "pl": "E-mail:",
        "en": "E-mail:",
    },
    "certgen_crypto_frame": {
        "pl": "Parametry kryptograficzne",
        "en": "Cryptographic parameters",
    },
    "certgen_key_alg": {
        "pl": "Algorytm klucza:",
        "en": "Key algorithm:",
    },
    "certgen_key_size": {
        "pl": "Rozmiar klucza RSA:",
        "en": "RSA key size:",
    },
    "certgen_ec_curve": {
        "pl": "Krzywa EC:",
        "en": "EC curve:",
    },
    "certgen_hash_alg": {
        "pl": "Algorytm hash (sig):",
        "en": "Hash algorithm (sig):",
    },
    "certgen_days": {
        "pl": "Ważność (dni):",
        "en": "Validity (days):",
    },
    "certgen_san_frame": {
        "pl": "Subject Alternative Names (SAN) — opcjonalne",
        "en": "Subject Alternative Names (SAN) — optional",
    },
    "certgen_san_dns_hint": {
        "pl": "(jedna na linię, np. localhost)",
        "en": "(one per line, e.g. localhost)",
    },
    "certgen_san_ip_hint": {
        "pl": "(jedna na linię, np. 127.0.0.1)",
        "en": "(one per line, e.g. 127.0.0.1)",
    },
    "certgen_ca_frame": {
        "pl": "Certyfikat CA (tylko dla trybu Podpisany przez CA)",
        "en": "CA Certificate (signed by CA mode only)",
    },
    "certgen_ca_cert_label": {
        "pl": "Plik CA cert (.crt/.pem):",
        "en": "CA cert file (.crt/.pem):",
    },
    "certgen_ca_key_label": {
        "pl": "Plik CA klucza (.key/.pem):",
        "en": "CA key file (.key/.pem):",
    },
    "certgen_ca_pass_label": {
        "pl": "Hasło klucza CA:",
        "en": "CA key password:",
    },
    "certgen_out_frame": {
        "pl": "Pliki wyjściowe",
        "en": "Output files",
    },
    "certgen_outdir_label": {
        "pl": "Folder wyjściowy:",
        "en": "Output folder:",
    },
    "certgen_basename_label": {
        "pl": "Nazwa bazowa plików:",
        "en": "Base filename:",
    },
    "certgen_pfx_pass_label": {
        "pl": "Hasło do PFX:",
        "en": "PFX password:",
    },
    "certgen_pfx_pass_hint": {
        "pl": "(puste = brak hasła)",
        "en": "(empty = no password)",
    },
    "certgen_export_pfx": {
        "pl": "Eksportuj PFX (klucz + certyfikat razem)",
        "en": "Export PFX (key + certificate together)",
    },
    "certgen_install": {
        "pl": "Zainstaluj certyfikat w magazynie Windows (wymaga uprawnień admina)",
        "en": "Install certificate in Windows store (requires admin rights)",
    },
    "btn_gen_cert": {
        "pl": "Generuj certyfikat",
        "en": "Generate certificate",
    },
    "btn_show_cmds": {
        "pl": "Pokaż komendy",
        "en": "Show commands",
    },

    # ── Auto-detect / dialogs ─────────────────────────────────────────────────
    "detect_title": {
        "pl": "Wykrywanie narzędzi...",
        "en": "Detecting tools...",
    },
    "detect_searching": {
        "pl": "🔍  Przeszukiwanie systemu w poszukiwaniu narzędzi...",
        "en": "🔍  Searching the system for tools...",
    },
    "detect_init": {
        "pl": "Inicjalizacja...",
        "en": "Initializing...",
    },
    "btn_cancel": {
        "pl": "Anuluj",
        "en": "Cancel",
    },
    "detect_report_title": {
        "pl": "Wyniki wykrywania narzędzi",
        "en": "Tool detection results",
    },
    "detect_report_header": {
        "pl": "Wyniki automatycznego wykrywania narzędzi",
        "en": "Automatic tool detection results",
    },
    "detect_not_found": {
        "pl": "Nie znaleziono",
        "en": "Not found",
    },
    "detect_missing_info": {
        "pl": (
            "⚠️  Nie znaleziono: {missing}\n\n"
            "Aby korzystać z pełnej funkcjonalności:\n"
            "• signtool.exe — zainstaluj Windows SDK (Windows Kits)\n"
            "• openssl.exe — zainstaluj OpenSSL dla Windows lub Git for Windows\n\n"
            "Możesz wskazać ścieżki ręcznie powyżej i kliknąć 'Zastosuj'."
        ),
        "en": (
            "⚠️  Not found: {missing}\n\n"
            "To use full functionality:\n"
            "• signtool.exe — install Windows SDK (Windows Kits)\n"
            "• openssl.exe — install OpenSSL for Windows or Git for Windows\n\n"
            "You can specify paths manually above and click 'Apply'."
        ),
    },
    "detect_all_ok": {
        "pl": "✅  Wszystkie narzędzia zostały wykryte pomyślnie.",
        "en": "✅  All tools detected successfully.",
    },
    "btn_apply_close": {
        "pl": "Zastosuj i zamknij",
        "en": "Apply and close",
    },
    "btn_close": {
        "pl": "Zamknij",
        "en": "Close",
    },
    "btn_rescan": {
        "pl": "🔄 Ponów skanowanie",
        "en": "🔄 Rescan",
    },
    "status_signtool_ok": {
        "pl": "signtool OK",
        "en": "signtool OK",
    },
    "status_signtool_missing": {
        "pl": "signtool BRAK",
        "en": "signtool MISSING",
    },
    "status_openssl_ok": {
        "pl": "openssl OK",
        "en": "openssl OK",
    },
    "status_openssl_missing": {
        "pl": "openssl BRAK",
        "en": "openssl MISSING",
    },

    # ── Message boxes ─────────────────────────────────────────────────────────
    "msg_no_data": {
        "pl": "Brak danych",
        "en": "Missing data",
    },
    "msg_no_cert": {
        "pl": "Brak certyfikatu",
        "en": "No certificate",
    },
    "msg_no_cert_body": {
        "pl": (
            "Nie podano żadnego certyfikatu.\n"
            "SignTool spróbuje automatycznie znaleźć certyfikat w magazynie.\n\n"
            "Kontynuować?"
        ),
        "en": (
            "No certificate provided.\n"
            "SignTool will try to find a certificate in the store automatically.\n\n"
            "Continue?"
        ),
    },
    "msg_select_cert": {
        "pl": "Wybierz pliki i podaj informacje o certyfikacie",
        "en": "Select files and provide certificate information",
    },
    "msg_select_ts": {
        "pl": "Wybierz pliki i podaj serwer timestamp",
        "en": "Select files and provide a timestamp server",
    },
    "msg_select_verify": {
        "pl": "Wybierz pliki do weryfikacji",
        "en": "Select files to verify",
    },
    "msg_select_catdb": {
        "pl": "Podaj plik katalogu",
        "en": "Provide a catalog file",
    },
    "msg_select_remove": {
        "pl": "Wybierz pliki",
        "en": "Select files",
    },
    "msg_batch_empty": {
        "pl": "Edytor jest pusty",
        "en": "Editor is empty",
    },
    "msg_save_error": {
        "pl": "Błąd zapisu",
        "en": "Save error",
    },
    "msg_save_config_fail": {
        "pl": "Nie można zapisać konfiguracji:\n{e}",
        "en": "Cannot save configuration:\n{e}",
    },
    "msg_success": {
        "pl": "Sukces",
        "en": "Success",
    },
    "msg_file_saved": {
        "pl": "Plik zapisany pomyślnie",
        "en": "File saved successfully",
    },
    "msg_error": {
        "pl": "Błąd",
        "en": "Error",
    },
    "msg_load_fail": {
        "pl": "Nie można wczytać pliku: {e}",
        "en": "Cannot load file: {e}",
    },
    "msg_save_fail": {
        "pl": "Nie można zapisać pliku: {e}",
        "en": "Cannot save file: {e}",
    },
    "msg_no_cn": {
        "pl": "Podaj przynajmniej nazwę (CN) certyfikatu.",
        "en": "Please provide at least the certificate name (CN).",
    },
    "msg_no_outdir": {
        "pl": "Brak folderu",
        "en": "Missing folder",
    },
    "msg_outdir_missing": {
        "pl": "Wybrany folder wyjściowy nie istnieje.",
        "en": "The selected output folder does not exist.",
    },

    # ── Output messages ───────────────────────────────────────────────────────
    "out_running": {
        "pl": "Wykonywanie: {cmd}\n\n",
        "en": "Running: {cmd}\n\n",
    },
    "out_success": {
        "pl": "\n✓ Sukces!\n",
        "en": "\n✓ Success!\n",
    },
    "out_error_code": {
        "pl": "\n✗ Błąd! Kod: {code}\n",
        "en": "\n✗ Error! Code: {code}\n",
    },
    "out_exception": {
        "pl": "\n✗ Wyjątek: {e}\n",
        "en": "\n✗ Exception: {e}\n",
    },
    "out_cmd_header": {
        "pl": "=== WYGENEROWANA KOMENDA ===\n\n",
        "en": "=== GENERATED COMMAND ===\n\n",
    },
    "out_cmd_footer": {
        "pl": "\n\n=== KONIEC KOMENDY ===",
        "en": "\n\n=== END OF COMMAND ===",
    },
    "out_batch_running": {
        "pl": "Wykonywanie: {cmd}\n\n",
        "en": "Running: {cmd}\n\n",
    },

    # ── CertGen output ────────────────────────────────────────────────────────
    "certgen_openssl_header": {
        "pl": "=== KOMENDY OPENSSL ===\n\n",
        "en": "=== OPENSSL COMMANDS ===\n\n",
    },
    "certgen_ps_header": {
        "pl": "=== SKRYPT POWERSHELL ===\n\n",
        "en": "=== POWERSHELL SCRIPT ===\n\n",
    },
    "certgen_gen_header": {
        "pl": "=== GENEROWANIE CERTYFIKATU (OpenSSL) ===\n\n",
        "en": "=== CERTIFICATE GENERATION (OpenSSL) ===\n\n",
    },
    "certgen_gen_ps_header": {
        "pl": "=== GENEROWANIE CERTYFIKATU (PowerShell) ===\n\n",
        "en": "=== CERTIFICATE GENERATION (PowerShell) ===\n\n",
    },
    "certgen_build_error": {
        "pl": "Błąd budowania komend: {e}\n",
        "en": "Command build error: {e}\n",
    },
    "certgen_gen_status": {
        "pl": "Generowanie certyfikatu...",
        "en": "Generating certificate...",
    },
    "certgen_gen_ps_status": {
        "pl": "Generowanie certyfikatu (PowerShell)...",
        "en": "Generating certificate (PowerShell)...",
    },
    "certgen_success_status": {
        "pl": "Gotowy - Certyfikat wygenerowany | v2.0",
        "en": "Ready - Certificate generated | v2.0",
    },
    "certgen_error_status": {
        "pl": "Błąd generowania certyfikatu | v2.0",
        "en": "Certificate generation error | v2.0",
    },
    "certgen_success_msg": {
        "pl": "✓ Certyfikat wygenerowany pomyślnie!\n  Klucz: {key}\n  Cert:  {crt}\n",
        "en": "✓ Certificate generated successfully!\n  Key: {key}\n  Cert: {crt}\n",
    },
    "certgen_installing": {
        "pl": "\n▶ Instalowanie PFX w magazynie Windows...\n",
        "en": "\n▶ Installing PFX in Windows certificate store...\n",
    },
    "certgen_installed_ok": {
        "pl": "  ✓ Zainstalowano w magazynie Cert:\\CurrentUser\\My\n",
        "en": "  ✓ Installed in Cert:\\CurrentUser\\My store\n",
    },
    "certgen_install_error": {
        "pl": "  ✗ Błąd instalacji:\n{e}\n",
        "en": "  ✗ Installation error:\n{e}\n",
    },
    "certgen_not_found": {
        "pl": "  ✗ Nie znaleziono: {tool}\n     Zainstaluj OpenSSL lub podaj właściwą ścieżkę.\n\n",
        "en": "  ✗ Not found: {tool}\n     Install OpenSSL or provide the correct path.\n\n",
    },
    "certgen_step_ec_key": {
        "pl": "Generowanie klucza EC",
        "en": "Generating EC key",
    },
    "certgen_step_rsa_key": {
        "pl": "Generowanie klucza RSA",
        "en": "Generating RSA key",
    },
    "certgen_step_self_signed": {
        "pl": "Generowanie self-signed certyfikatu",
        "en": "Generating self-signed certificate",
    },
    "certgen_step_root_ca": {
        "pl": "Generowanie certyfikatu Root CA",
        "en": "Generating Root CA certificate",
    },
    "certgen_step_csr": {
        "pl": "Generowanie CSR",
        "en": "Generating CSR",
    },
    "certgen_step_sign_ca": {
        "pl": "Podpisanie przez CA",
        "en": "Signing by CA",
    },
    "certgen_step_pfx": {
        "pl": "Eksport do PFX",
        "en": "Export to PFX",
    },
    "certgen_ps_cert_saved": {
        "pl": "Certyfikat zapisany:",
        "en": "Certificate saved:",
    },
    "certgen_ps_crt": {
        "pl": "Certyfikat (CRT):",
        "en": "Certificate (CRT):",
    },

    # ── File dialogs ──────────────────────────────────────────────────────────
    "dlg_select_file": {
        "pl": "Wybierz plik {type}",
        "en": "Select {type} file",
    },
    "dlg_all_files": {
        "pl": "Wszystkie pliki",
        "en": "All files",
    },
    "dlg_sign_files": {
        "pl": "Wybierz pliki do podpisania",
        "en": "Select files to sign",
    },
    "dlg_exec_files": {
        "pl": "Pliki wykonywalne",
        "en": "Executable files",
    },
    "dlg_verify_files": {
        "pl": "Wybierz pliki do weryfikacji",
        "en": "Select files for verification",
    },
    "dlg_select_files": {
        "pl": "Wybierz pliki",
        "en": "Select files",
    },
    "dlg_response_files": {
        "pl": "Wybierz plik odpowiedzi",
        "en": "Select response file",
    },
    "dlg_save_response": {
        "pl": "Zapisz plik odpowiedzi",
        "en": "Save response file",
    },
    "dlg_text_files": {
        "pl": "Text files",
        "en": "Text files",
    },
    "dlg_select_outdir": {
        "pl": "Wybierz folder wyjściowy",
        "en": "Select output folder",
    },

    # ── Tooltips ──────────────────────────────────────────────────────────────
    "tip_lang_btn": {
        "pl": "Przełącz język interfejsu\n(PL ↔ EN)",
        "en": "Switch interface language\n(PL ↔ EN)",
    },
    "tip_stop_btn": {
        "pl": "Zatrzymaj bieżącą operację signtool",
        "en": "Stop the current signtool operation",
    },
    "tip_led_signtool": {
        "pl": "Status signtool.exe\n● Zielony = znaleziony\n● Czerwony = nie znaleziony",
        "en": "signtool.exe status\n● Green = found\n● Red = not found",
    },
    "tip_led_openssl": {
        "pl": "Status openssl.exe\n● Zielony = znaleziony\n● Czerwony = nie znaleziony",
        "en": "openssl.exe status\n● Green = found\n● Red = not found",
    },
    # Sign tab
    "tip_sign_files": {
        "pl": "Lista plików do podpisania.\nObsługiwane: .exe, .dll, .sys, .cat, .msi\nMożna dodać wiele plików naraz.",
        "en": "Files to be signed.\nSupported: .exe, .dll, .sys, .cat, .msi\nMultiple files can be added at once.",
    },
    "tip_sign_cert_store": {
        "pl": "Użyj certyfikatu z magazynu Windows.\nNie wymaga pliku PFX – certyfikat musi\nbyć zainstalowany w systemie.",
        "en": "Use a certificate from the Windows store.\nNo PFX file needed – the certificate must\nbe installed in the system.",
    },
    "tip_sign_cert_file": {
        "pl": "Użyj certyfikatu z pliku PFX.\nPlik PFX zawiera klucz prywatny\ni certyfikat w jednym archiwum.",
        "en": "Use a certificate from a PFX file.\nA PFX file contains both the private key\nand certificate in one archive.",
    },
    "tip_sign_cert_name": {
        "pl": "Nazwa certyfikatu w magazynie Windows.\nSignTool wybierze certyfikat pasujący\ndo podanego ciągu znaków.\nFlaga: /n",
        "en": "Certificate name in the Windows store.\nSignTool selects the certificate matching\nthe provided string.\nFlag: /n",
    },
    "tip_sign_cert_sha1": {
        "pl": "Odcisk SHA1 certyfikatu (40 hex).\nJednoznacznie identyfikuje certyfikat\ngdy w magazynie jest kilka podobnych.\nFlaga: /sha1",
        "en": "Certificate SHA1 thumbprint (40 hex chars).\nUniquely identifies a certificate\nwhen the store has several similar ones.\nFlag: /sha1",
    },
    "tip_sign_pfx_file": {
        "pl": "Ścieżka do pliku .pfx / .p12.\nKliknij '...' aby wybrać plik.\nFlaga: /f",
        "en": "Path to .pfx / .p12 file.\nClick '...' to browse.\nFlag: /f",
    },
    "tip_sign_pfx_pass": {
        "pl": "Hasło do pliku PFX.\nZostawienie pustego działa dla\ncertyfikatów bez hasła.\nFlaga: /p",
        "en": "Password for the PFX file.\nLeave empty for certificates\nwithout a password.\nFlag: /p",
    },
    "tip_sign_addl_cert": {
        "pl": "Dodatkowy certyfikat pośredni (.cer / .crt).\nStosowany przy cross-certification lub\ngdy łańcuch certyfikatów jest niekompletny.\nFlaga: /ac",
        "en": "Additional intermediate certificate (.cer / .crt).\nUsed for cross-certification or when\nthe certificate chain is incomplete.\nFlag: /ac",
    },
    "tip_sign_hash": {
        "pl": "Algorytm skrótu podpisu cyfrowego.\nSHA256 – zalecany (Windows 8+)\nSHA1 – tylko starsze systemy (deprecated)\nFlaga: /fd",
        "en": "Digital signature hash algorithm.\nSHA256 – recommended (Windows 8+)\nSHA1 – legacy systems only (deprecated)\nFlag: /fd",
    },
    "tip_sign_desc": {
        "pl": "Opis programu widoczny w dialogu\nUAC ('Ten zweryfikowany wydawca...').\nFlaga: /d",
        "en": "Program description shown in the\nUAC dialog ('This verified publisher...').\nFlag: /d",
    },
    "tip_sign_url": {
        "pl": "URL strony programu wyświetlany\nw dialogu bezpieczeństwa Windows.\nFlaga: /du",
        "en": "Program URL displayed in the\nWindows security dialog.\nFlag: /du",
    },
    "tip_sign_ts_server": {
        "pl": "Adres serwera znacznika czasu (TSA).\nPopularne serwery:\n• http://timestamp.digicert.com\n• http://ts.ssl.com\n• http://timestamp.sectigo.com",
        "en": "Timestamp Authority (TSA) server URL.\nPopular servers:\n• http://timestamp.digicert.com\n• http://ts.ssl.com\n• http://timestamp.sectigo.com",
    },
    "tip_sign_ts_rfc3161": {
        "pl": "RFC 3161 – nowoczesny protokół znacznika czasu.\nZalecany dla wszystkich nowych podpisów.\nFlaga: /tr + /td",
        "en": "RFC 3161 – modern timestamp protocol.\nRecommended for all new signatures.\nFlag: /tr + /td",
    },
    "tip_sign_ts_auth": {
        "pl": "Authenticode – starszy protokół timestamp.\nStosuj tylko dla zgodności ze starszymi\nsystemami (Windows XP/Vista).\nFlaga: /t",
        "en": "Authenticode – legacy timestamp protocol.\nUse only for compatibility with older\nsystems (Windows XP/Vista).\nFlag: /t",
    },
    "tip_sign_ts_hash": {
        "pl": "Algorytm skrótu dla znacznika RFC 3161.\nPowinien być taki sam jak algorytm podpisu.\nFlaga: /td (tylko z /tr)",
        "en": "Hash algorithm for RFC 3161 timestamp.\nShould match the signature hash algorithm.\nFlag: /td (only with /tr)",
    },
    "tip_sign_append": {
        "pl": "Dołącz dodatkowy podpis do już podpisanego pliku\n(dual signing – SHA1 + SHA256).\nFlaga: /as",
        "en": "Append an additional signature to an already\nsigned file (dual signing – SHA1 + SHA256).\nFlag: /as",
    },
    "tip_sign_verbose": {
        "pl": "Tryb szczegółowy – wyświetla więcej\ninformacji w logu operacji.\nFlaga: /v",
        "en": "Verbose mode – displays more\ndetails in the operation log.\nFlag: /v",
    },
    "tip_sign_debug": {
        "pl": "Tryb debugowania – maksymalna ilość\ninformacji diagnostycznych.\nFlaga: /debug",
        "en": "Debug mode – maximum amount of\ndiagnostic information.\nFlag: /debug",
    },
    "tip_btn_sign": {
        "pl": "Uruchom signtool sign z podanymi\nopcjami i podpisz wybrane pliki.",
        "en": "Run signtool sign with the specified\noptions and sign the selected files.",
    },
    "tip_btn_show_cmd": {
        "pl": "Pokaż gotową komendę bez wykonywania.\nMożna ją skopiować i uruchomić ręcznie.",
        "en": "Show the generated command without running it.\nYou can copy and run it manually.",
    },
    # Timestamp / Verify tab
    "tip_ts_server": {
        "pl": "URL serwera TSA do dodania znacznika czasu.\nNp. http://timestamp.digicert.com\nFlaga: /tr (RFC3161) lub /t (Authenticode)",
        "en": "TSA server URL for adding a timestamp.\nE.g. http://timestamp.digicert.com\nFlag: /tr (RFC3161) or /t (Authenticode)",
    },
    "tip_ts_hash": {
        "pl": "Algorytm skrótu znacznika czasu.\nMusi odpowiadać algorytmowi użytemu\nprzy podpisywaniu. Flaga: /td",
        "en": "Hash algorithm for the timestamp.\nMust match the algorithm used when\nsigning the file. Flag: /td",
    },
    "tip_verify_pa": {
        "pl": "Weryfikuj wszystkie podpisy (Authenticode i catalog).\nZalecane do ogólnej weryfikacji.\nFlaga: /pa",
        "en": "Verify all signatures (Authenticode and catalog).\nRecommended for general verification.\nFlag: /pa",
    },
    "tip_verify_pg": {
        "pl": "Weryfikuj podpis strony kodu (page hash).\nStosowane dla sterowników i plików\nkernel-mode. Flaga: /pg",
        "en": "Verify page hash signature.\nUsed for drivers and kernel-mode\nfiles. Flag: /pg",
    },
    "tip_verify_catalog": {
        "pl": "Plik katalogu (.cat) do weryfikacji podpisu.\nJeśli plik nie ma osadzonego podpisu,\nweryfikacja odbywa się przez katalog.\nFlaga: /c",
        "en": "Catalog (.cat) file for signature verification.\nIf the file has no embedded signature,\nverification is done via the catalog.\nFlag: /c",
    },
    # CatDB tab
    "tip_catdb_file": {
        "pl": "Plik katalogu (.cat) do dodania lub\nusunięcia z bazy danych katalogów systemu.\nKatalogi są używane do weryfikacji\npodpisów plików bez osadzonego podpisu.",
        "en": "Catalog (.cat) file to add or remove\nfrom the system catalog database.\nCatalogs are used to verify signatures\nof files without embedded signatures.",
    },
    "tip_catdb_action": {
        "pl": "Dodaj (/u) – dodaj katalog do bazy\nUsuń (/r) – usuń katalog z bazy\nFlaga /d wymusza unikalność GUID.",
        "en": "Add (/u) – add catalog to database\nRemove (/r) – remove catalog from database\nFlag /d enforces GUID uniqueness.",
    },
    # Remove tab
    "tip_remove_files": {
        "pl": "Pliki, z których zostanie usunięty\npodpis Authenticode.\nUWAGA: Operacja jest nieodwracalna!\nFlaga: /s",
        "en": "Files from which the Authenticode\nsignature will be removed.\nWARNING: This operation is irreversible!\nFlag: /s",
    },
    # Batch tab
    "tip_batch_editor": {
        "pl": "Edytor pliku odpowiedzi signtool.\nFormat: jeden argument na linię,\npierwsza linia to komenda (np. sign).\nPrzykład:\n  sign\n  /n MyCert\n  /fd SHA256\n  plik.exe",
        "en": "signtool response file editor.\nFormat: one argument per line,\nfirst line is the command (e.g. sign).\nExample:\n  sign\n  /n MyCert\n  /fd SHA256\n  file.exe",
    },
    "tip_batch_exec": {
        "pl": "Wykonaj plik odpowiedzi:\nsigntool @plik_odpowiedzi.txt\nWszystkie argumenty z edytora\nzostaną przekazane do signtool.",
        "en": "Execute the response file:\nsigntool @response_file.txt\nAll arguments from the editor\nwill be passed to signtool.",
    },
    # CertGen tab
    "tip_certgen_openssl": {
        "pl": "Ścieżka do openssl.exe.\nJeśli OpenSSL jest w PATH, można\nzostąwić 'openssl'.\nPobierz: https://slproweb.com/products/Win32OpenSSL.html",
        "en": "Path to openssl.exe.\nIf OpenSSL is in PATH, you can\nleave it as 'openssl'.\nDownload: https://slproweb.com/products/Win32OpenSSL.html",
    },
    "tip_certgen_type_self": {
        "pl": "Certyfikat samopodpisany – podpisuje\ngo własny klucz prywatny.\nIdealny do testów i środowisk deweloperskich.\nNIE jest zaufany przez Windows domyślnie.",
        "en": "Self-signed certificate – signed by\nits own private key.\nIdeal for testing and development environments.\nNOT trusted by Windows by default.",
    },
    "tip_certgen_type_ca": {
        "pl": "Certyfikat Root CA – urząd certyfikacji.\nMoże podpisywać inne certyfikaty.\nAby był zaufany, należy go zainstalować\nw magazynie 'Zaufane główne urzędy'.",
        "en": "Root CA certificate – certification authority.\nCan sign other certificates.\nTo be trusted, install it in the\n'Trusted Root Certification Authorities' store.",
    },
    "tip_certgen_type_signed": {
        "pl": "Certyfikat podpisany przez własne CA.\nWymaga pliku .crt i .key Root CA.\nZaufany w systemach, gdzie CA jest\nzainstalowane jako zaufane.",
        "en": "Certificate signed by your own CA.\nRequires Root CA .crt and .key files.\nTrusted on systems where the CA\nis installed as trusted.",
    },
    "tip_certgen_cn": {
        "pl": "Common Name – nazwa podmiotu certyfikatu.\nDla podpisywania kodu użyj nazwy firmy\nlub aplikacji.\nPole: CN=",
        "en": "Common Name – the certificate subject name.\nFor code signing, use your company\nor application name.\nField: CN=",
    },
    "tip_certgen_country": {
        "pl": "Kod kraju ISO 3166-1 alpha-2 (2 litery).\nPrzykłady: PL, US, DE, GB, FR\nPole: C=",
        "en": "ISO 3166-1 alpha-2 country code (2 letters).\nExamples: PL, US, DE, GB, FR\nField: C=",
    },
    "tip_certgen_key_alg": {
        "pl": "Algorytm klucza:\nRSA – szeroka kompatybilność (zalecany)\nEC (ECDSA) – krótsze klucze, nowocześniejszy",
        "en": "Key algorithm:\nRSA – wide compatibility (recommended)\nEC (ECDSA) – shorter keys, more modern",
    },
    "tip_certgen_key_size": {
        "pl": "Rozmiar klucza RSA w bitach.\n2048 – minimum dla code signing\n3072/4096 – wyższe bezpieczeństwo,\nwolniejsze operacje",
        "en": "RSA key size in bits.\n2048 – minimum for code signing\n3072/4096 – higher security,\nslower operations",
    },
    "tip_certgen_ec_curve": {
        "pl": "Krzywa eliptyczna dla klucza EC:\nprime256v1 (P-256) – 128-bit security\nsecp384r1 (P-384) – 192-bit security\nsecp521r1 (P-521) – 256-bit security",
        "en": "Elliptic curve for EC key:\nprime256v1 (P-256) – 128-bit security\nsecp384r1 (P-384) – 192-bit security\nsecp521r1 (P-521) – 256-bit security",
    },
    "tip_certgen_hash": {
        "pl": "Algorytm skrótu podpisu certyfikatu.\nsha256 – zalecany\nsha384/sha512 – dla wyższego bezpieczeństwa",
        "en": "Certificate signature hash algorithm.\nsha256 – recommended\nsha384/sha512 – for higher security",
    },
    "tip_certgen_days": {
        "pl": "Czas ważności certyfikatu w dniach.\nPrzykłady:\n365 = 1 rok\n730 = 2 lata\n3650 = ~10 lat",
        "en": "Certificate validity period in days.\nExamples:\n365 = 1 year\n730 = 2 years\n3650 = ~10 years",
    },
    "tip_certgen_san_dns": {
        "pl": "Alternatywne nazwy DNS (Subject Alternative Names).\nJedna nazwa na linię.\nPrzykład: localhost, mojadomena.pl",
        "en": "DNS Subject Alternative Names (SAN).\nOne name per line.\nExample: localhost, mydomain.com",
    },
    "tip_certgen_san_ip": {
        "pl": "Alternatywne adresy IP (Subject Alternative Names).\nJeden adres na linię.\nPrzykład: 127.0.0.1, 192.168.1.1",
        "en": "IP Address Subject Alternative Names (SAN).\nOne address per line.\nExample: 127.0.0.1, 192.168.1.1",
    },
    "tip_certgen_pfx_pass": {
        "pl": "Hasło do eksportowanego pliku PFX.\nZostawienie pustego = brak hasła.\nHasło nie jest zapisywane w konfiguracji.",
        "en": "Password for the exported PFX file.\nLeave empty = no password.\nPassword is NOT saved to configuration.",
    },
    "tip_certgen_export_pfx": {
        "pl": "Eksportuj klucz prywatny + certyfikat\ndo pliku .pfx (PKCS#12).\nFormat wymagany przez signtool /f",
        "en": "Export private key + certificate\nto a .pfx (PKCS#12) file.\nFormat required by signtool /f",
    },
    "tip_certgen_install": {
        "pl": "Zainstaluj wygenerowany certyfikat\nw magazynie Windows (CurrentUser\\My).\nWymaga uprawnień administratora.\nWykonuje: Import-PfxCertificate",
        "en": "Install the generated certificate\nin the Windows store (CurrentUser\\My).\nRequires administrator privileges.\nExecutes: Import-PfxCertificate",
    },
    "tip_certgen_generate": {
        "pl": "Uruchom generowanie certyfikatu\nza pomocą wybranej metody (OpenSSL/PowerShell).\nPliki zostaną zapisane w podanym folderze.",
        "en": "Start certificate generation\nusing the selected method (OpenSSL/PowerShell).\nFiles will be saved to the specified folder.",
    },

    # ── Language switcher ─────────────────────────────────────────────────────
    "lang_label": {
        "pl": "Język / Language:",
        "en": "Język / Language:",
    },
    "lang_restart_title": {
        "pl": "Zmiana języka",
        "en": "Language change",
    },
    "lang_restart_body": {
        "pl": "Zmiana języka wymaga restartu aplikacji.\nCzy chcesz zrestartować teraz?",
        "en": "Language change requires application restart.\nDo you want to restart now?",
    },
}


def set_language(lang: str):
    """Set active language: 'pl' or 'en'"""
    global _LANG
    if lang in ("pl", "en"):
        _LANG = lang


def get_language() -> str:
    return _LANG


def t(key: str, **kwargs) -> str:
    """Return translated string for key in active language."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key  # fallback: return key itself
    text = entry.get(_LANG, entry.get("pl", key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
    return text
