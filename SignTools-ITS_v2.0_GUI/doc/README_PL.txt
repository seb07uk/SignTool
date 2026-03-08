================================================================================
  SignTool's-ITS GUI v2.0
  Graficzny interfejs podpisywania kodu i generowania certyfikatów
  polsoft.ITS™ Group — creative coding
  © 2026 polsoft.ITS™. Wszelkie prawa zastrzeżone.
================================================================================

CO TO JEST?
-----------
SignTool's-ITS GUI v2.0 to przenośna aplikacja graficzna (GUI) dla systemu
Windows, która zastępuje ręczne wpisywanie poleceń signtool.exe i openssl.exe
w wierszu poleceń. Wszystkie operacje kryptograficzne — podpisywanie kodu,
znacznikowanie czasu, weryfikacja podpisów, zarządzanie certyfikatami —
dostępne są przez czytelny interfejs z zakładkami.

WYMAGANIA SYSTEMOWE
-------------------
  • System operacyjny : Windows 7 SP1 / 8 / 8.1 / 10 / 11 (x64)
  • signtool.exe      : Windows SDK (wykrywany automatycznie)
  • openssl.exe       : OpenSSL dla Windows (wykrywany automatycznie)
  • Uprawnienia       : Zwykły użytkownik (bez UAC)
  • RAM               : min. 128 MB
  • Miejsce na dysku  : ~30 MB

SZYBKI START — GOTOWY PLIK EXE
--------------------------------
1. Otwórz folder:  app\
2. Uruchom:        "SignTools-ITS v2.0 GUI.exe"
3. Przy pierwszym uruchomieniu aplikacja automatycznie wykryje
   signtool.exe i openssl.exe na wszystkich dyskach.
4. Kliknij "Zastosuj i zamknij" — gotowe!

BUDOWANIE ZE ŹRÓDEŁ (opcjonalne)
---------------------------------
Wymaganie: Python 3.8+ w zmiennej PATH

  cd SignTools-ITS_v2.0_GUI
  SignTool_GUI_v2.0_build.bat

Skrypt automatycznie:
  [1/6] Weryfikuje instalację Pythona
  [2/6] Instaluje PyInstaller (jeśli brak)
  [3/6] Weryfikuje pliki źródłowe
  [4/6] Czyści poprzednie artefakty
  [5/6] Kompiluje plik EXE
  [6/6] Otwiera folder dist\ w Eksploratorze

GŁÓWNE FUNKCJE
--------------
  [Sign]              Podpisywanie plików EXE/DLL/SYS/MSI/CAT/PS1
                      Certyfikat z magazynu Windows lub z pliku PFX
                      Algorytmy: SHA1 / SHA256 / SHA384 / SHA512
                      Znacznik czasu: RFC 3161 lub Authenticode

  [Timestamp/Verify]  Dodawanie znacznika czasu do podpisanych plików
                      Weryfikacja podpisów cyfrowych

  [CatDB/Remove]      Zarządzanie bazą katalogów Windows (catdb)
                      Usuwanie podpisów Authenticode z plików

  [Batch]             Tryb wsadowy z plikiem odpowiedzi (@response_file)
                      Wbudowany edytor tekstowy

  [Generuj cert]      Certyfikaty Self-signed, Root CA, podpisane przez CA
                      Silnik: OpenSSL lub PowerShell
                      Eksport PFX, instalacja w magazynie Windows

USTAWIENIA I KONFIGURACJA
--------------------------
Plik konfiguracyjny:
  %USERPROFILE%\.polsoft\software\SignToolGUI\SignToolGUI.json

Zapisywane automatycznie:
  • Ścieżki do signtool.exe i openssl.exe
  • Język interfejsu (PL / EN)
  • Wartości wszystkich pól formularzy

NIGDY niezapisywane (bezpieczeństwo):
  • Hasła PFX
  • Hasła kluczy CA

Wygenerowane certyfikaty:
  %USERPROFILE%\.polsoft\software\SignToolGUI\Certificates\

ZMIANA JĘZYKA
-------------
Kliknij przycisk [EN] w prawym dolnym rogu paska stanu,
aby przełączyć interfejs na język angielski.
Przełączenie następuje natychmiast — bez restartu.

UWAGA DOTYCZĄCA ANTYWIRUSA
---------------------------
Jeżeli budujesz ze źródeł: niektóre programy AV mogą flagować
nowo skompilowane pliki EXE (PyInstaller) jako podejrzane (false positive).
Dodaj folder projektu do wyjątków przed kompilacją.

KONTAKT I WSPARCIE
------------------
  Autor   : Sebastian Januchowski
  Firma   : polsoft.ITS™ Group
  E-mail  : polsoft.its@fastservice.com
  GitHub  : github.com/seb07uk

LICENCJA
--------
Oprogramowanie własnościowe. Wszelkie prawa zastrzeżone — polsoft.ITS™ Group.
Nieautoryzowane kopiowanie, modyfikowanie lub dystrybucja są zabronione.

================================================================================
  polsoft.ITS™ Group — creative coding — 2026©
================================================================================
