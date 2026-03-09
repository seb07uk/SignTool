# Quick DigitalSignature GUI

> **Lekki interfejs graficzny Windows do podpisywania i weryfikacji plików wykonywalnych za pomocą Microsoft SignTool**

![Quick DigitalSignature GUI v1.9](Screenshot.png)

[![Wersja](https://img.shields.io/badge/wersja-1.9-blue.svg)](https://github.com/seb07uk)
[![Platforma](https://img.shields.io/badge/platforma-Windows-lightgrey.svg)](https://github.com/seb07uk)
[![Python](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org)
[![Licencja](https://img.shields.io/badge/licencja-Własnościowa-red.svg)](https://github.com/seb07uk)

---

## Opis

**Quick DigitalSignature GUI** to przyjazny interfejs graficzny dla narzędzia `SignTool.exe` firmy Microsoft. Umożliwia programistom i administratorom systemów podpisywanie plików binarnych Windows (`.exe`, `.dll`, `.msi`, `.cab`) certyfikatem PFX oraz weryfikację istniejących podpisów — bez konieczności pamiętania złożonej składni wiersza poleceń.

**Autor:** Sebastian Januchowski  
**Firma:** polsoft.ITS™ Group  
**Kontakt:** polsoft.its@fastservice.com  
**Strona:** https://github.com/seb07uk  
**Copyright:** 2026 © polsoft.ITS™. Wszelkie prawa zastrzeżone.

---

## Funkcje

| Funkcja | Opis |
|---|---|
| 🖊️ **Podpisz plik** | Podpisz dowolny plik binarny Windows certyfikatem PFX (SHA-256) |
| ✅ **Weryfikuj (PA)** | Sprawdź podpis w lokalnym magazynie certyfikatów (Policy-based) |
| ✅ **Weryfikuj (PA+TS)** | Sprawdź podpis **oraz** znacznik czasu RFC 3161 przez urząd online |
| 🔁 **Ponów** | Powtórz ostatnią operację Podpisania lub Weryfikacji |
| 🔒 **Bezpieczne hasło** | Zapisz hasło PFX zaszyfrowane przez Windows DPAPI (per użytkownik, per maszyna) |
| 📂 **Automatyczne wykrywanie certyfikatów** | Automatycznie wyszukuje pliki `.pfx` w folderze programu i podfolderze `certs/` |
| 🖱️ **Przeciągnij i upuść** | Przeciągnij dowolny plik bezpośrednio na okno aplikacji |
| 🏛️ **Instaluj Root CA** | Zainstaluj certyfikat główny w systemowym magazynie Trusted Root |
| 🏛️ **Instaluj Intermediate CA** | Zainstaluj certyfikat pośredni w magazynie CA |
| 🌙 **Motyw ciemny / jasny** | Przełączaj między jasnym a ciemnym interfejsem; wybór jest zapamiętywany |
| 🔝 **Zawsze na wierzchu** | Przypnij okno ponad wszystkimi innymi oknami |
| 📋 **Przywracanie sesji** | Zapamiętuje ostatnio używany plik i certyfikat między sesjami |
| 📝 **Rotacyjny dziennik** | Zapisuje rotacyjny plik `app.log` (max 1 MB × 5 kopii zapasowych) |

---

## Wymagania

- **System:** Windows 10 / Windows 11 (zalecane 64-bit)
- **Python:** 3.8 lub nowszy (tylko uruchamianie ze źródeł)
- **SignTool.exe** — jeden z:
  - Dołączony wewnątrz spakowanego EXE (jeśli dystrybuowany w tej formie)
  - Umieszczony w tym samym folderze co aplikacja
  - Zainstalowany przez [Windows SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/)
  - Dostępny w zmiennej środowiskowej `PATH`
- **Zależności Python** (tylko źródła):
  ```
  Pillow
  tkinterdnd2
  ```

---

## Instalacja

### Opcja A — Gotowy plik EXE (zalecane)

1. Pobierz najnowszy `QuickDigitalSignature.exe` z sekcji [Releases](https://github.com/seb07uk).
2. Umieść go w dowolnym folderze razem z plikami `.pfx` (lub podfolderze `certs/`).
3. Uruchom dwukrotnym kliknięciem — Python nie jest wymagany.

### Opcja B — Uruchomienie ze źródeł

```bash
# Sklonuj lub pobierz repozytorium
git clone https://github.com/seb07uk/quick-digitalsignature

# Zainstaluj zależności
pip install Pillow tkinterdnd2

# Uruchom
python Quick_DigitalSignature.py
```

---

## Użytkowanie

### Podpisywanie pliku

1. **Plik** — kliknij **Browse…** lub przeciągnij i upuść docelowy plik binarny.
2. **Certyfikat** — wybierz `.pfx` z listy rozwijanej lub kliknij **Browse…**, aby wybrać ręcznie.
3. **Hasło PFX** — wpisz hasło certyfikatu (zostaw puste, jeśli brak). Zaznacz **Zapisz**, aby je bezpiecznie przechować.
4. Kliknij **Podpisz plik**.
5. Po sukcesie pojawia się okno dialogowe z wynikiem narzędzia SignTool.

### Weryfikacja podpisu

- **Weryfikuj (PA)** — sprawdza podpis cyfrowy w lokalnym magazynie certyfikatów.
- **Weryfikuj (PA+TS)** — dodatkowo waliduje znacznik czasu RFC 3161 przez urząd online.

### Instalowanie certyfikatów

Jeśli weryfikacja nie powiedzie się z błędem *„certyfikat główny nie jest zaufany"*:

1. Kliknij **Zainstaluj Root CA** i wybierz plik `.cer` / `.crt` certyfikatu głównego.
2. W razie potrzeby kliknij **Zainstaluj Intermediate CA** dla certyfikatów pośrednich.

> **Uwaga:** Instalacja w magazynie komputera lokalnego wymaga uprawnień Administratora. Bez podniesienia uprawnień certyfikat zostanie zainstalowany tylko w magazynie bieżącego użytkownika.

---

## Konfiguracja i dzienniki

| Element | Lokalizacja |
|---|---|
| Plik konfiguracyjny | `%APPDATA%\QuickDigitalSignature\config.json` |
| Plik dziennika | `%APPDATA%\QuickDigitalSignature\app.log` |

Aplikacja automatycznie zapisuje i przywraca:
- Ostatnio używaną ścieżkę do pliku
- Ostatnio używany certyfikat
- Zaszyfrowane hasło PFX (jeśli zaznaczono **Zapisz**)
- Preferencję motywu interfejsu

---

## Rozwiązywanie problemów

**Nie znaleziono SignTool.exe**  
Umieść `signtool.exe` w tym samym folderze co aplikacja lub zainstaluj Windows SDK i upewnij się, że ścieżka `bin\<wersja>\x64\` jest dodana do zmiennej `PATH`.

**Weryfikacja podpisu nie powiodła się (niezaufany certyfikat główny)**  
Zaimportuj certyfikaty łańcucha podpisu używając **Zainstaluj Root CA** i **Zainstaluj Intermediate CA**, lub przez PowerShell:
```powershell
Import-Certificate -FilePath root.cer    -CertStoreLocation Cert:\LocalMachine\Root
Import-Certificate -FilePath inter.cer   -CertStoreLocation Cert:\LocalMachine\CA
```

**Opcja zapisu hasła jest wyszarzona**  
Windows DPAPI nie jest dostępne dla tej sesji użytkownika. Wpisuj hasło ręcznie przy każdym uruchomieniu.

---

## Licencja

Copyright © 2026 polsoft.ITS™. Wszelkie prawa zastrzeżone.  
Kopiowanie, dystrybucja lub modyfikacja bez pisemnej zgody jest zabroniona.
