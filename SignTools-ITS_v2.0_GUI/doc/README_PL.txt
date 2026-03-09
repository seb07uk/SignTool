================================================================================
  SignTool's-ITS GUI v2.0
  Podpisywanie kodu i generowanie certyfikatow — Microsoft SignTool & OpenSSL
  Copyright 2026© polsoft.ITS™ Group. Wszelkie prawa zastrzezone.
================================================================================

SZYBKI START
------------
  python main.py

  Wymagania:  Python 3.9+  |  Windows 10/11  |  Brak zewnetrznych pakietow

  signtool.exe  — Windows SDK (wykrywany automatycznie przy starcie)
  openssl.exe   — Wymagany do generowania certyfikatow (wykrywany automatycznie)

  Brakujace narzedzia? Dialog startowy umozliwia reczne wskazanie sciezek.

KOMPILACJA DO EXE
-----------------
  pip install pyinstaller
  pyinstaller --noconsole --onefile main.py
  -> Wynik: dist/main.exe  (Python nie jest wymagany na docelowej maszynie)

ZAKLADKI
--------
  Sign               Podpisz EXE, DLL, skrypty (magazyn certyfikatow lub PFX)
  Timestamp/Verify   Dodaj znacznik czasu RFC3161 / Authenticode; weryfikuj podpisy
  CatDB / Remove     Zarzadzaj baza katalogow Windows; usuwaj podpisy z plikow
  Batch              Wykonuj pliki odpowiedzi signtool (jeden argument na linie)
  Generuj certyfikat Samopodpisany / Root CA / CA-signed via OpenSSL lub PowerShell
  Opcje              Przelacznik jezyka PL <-> EN; konfiguracja sciezek narzedzi
  Wynik              Kolorowe strumieniowane wyjscie dla wszystkich operacji

UWAGI
-----
  - Jezyk przelaczany w czasie dzialania (PL / EN)
  - Miganie konsoli wytlumione na Windows (CREATE_NO_WINDOW)
  - Wszystkie wywolania subprocess dzialaja w watkach-demonach
  - Uprawnienia administratora wymagane do operacji CatDB i magazynu certyfikatow
  - Ustawienia nie sa zapisywane miedzy sesjami

--------------------------------------------------------------------------------
  Autor   : Sebastian Januchowski
  Firma   : polsoft.ITS™ Group
  Kontakt : polsoft.its@fastservice.com
  GitHub  : https://github.com/seb07uk
  Licencja: Wlasnosciowa
================================================================================
