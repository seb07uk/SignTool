Quick DigitalSignature GUI v1.9
================================
Autor: Sebastian Januchowski | polsoft.ITS(tm) Group
Kontakt: polsoft.its@fastservice.com
Strona: https://github.com/seb07uk
Copyright (c) 2026 polsoft.ITS(tm). Wszelkie prawa zastrzezone.

CO ROBI PROGRAM
---------------
Lekki interfejs graficzny Windows do podpisywania i weryfikacji
plikow wykonywalnych (.exe, .dll, .msi, .cab) za pomoca
Microsoft SignTool i certyfikatu PFX. Bez znajomosci linii polecen.

SZYBKI START
------------
1. Umiesz QuickDigitalSignature.exe w tym samym folderze co plik .pfx.
2. Uruchom dwukrotnym kliknieciem.
3. Wybierz plik, certyfikat, wpisz haslo (jesli wymagane).
4. Kliknij "Sign File" (Podpisz plik).

WYMAGANIA
---------
- Windows 10 / 11 (zalecane 64-bit)
- SignTool.exe (wbudowany, lub z Windows SDK, lub w PATH)
- Python 3.8+ + Pillow + tkinterdnd2 (tylko przy uruchamianiu ze zrodel)

GLOWNE FUNKCJE
--------------
- Podpisywanie plikow SHA-256
- Weryfikacja podpisu (PA) lub podpisu + znacznika czasu (PA+TS, RFC 3161)
- Bezpieczne przechowywanie hasla przez Windows DPAPI
- Automatyczne wykrywanie certyfikatow .pfx
- Wybor pliku metoda przeciagnij i upusc
- Instalacja Root CA / Intermediate CA
- Motyw ciemny / jasny (zapamietywany miedzy sesjami)
- Przycisk "Zawsze na wierzchu"
- Przywracanie sesji (ostatni plik, certyfikat, haslo)
- Rotacyjny dziennik: %APPDATA%\QuickDigitalSignature\app.log

ROZWIAZYWANIE PROBLEMOW
-----------------------
Nie znaleziono SignTool:
  Umiesc signtool.exe obok aplikacji lub zainstaluj Windows SDK.

Weryfikacja nie powiodla sie (niezaufany certyfikat):
  Uzyj przyciskow "Zainstaluj Root CA" / "Zainstaluj Intermediate CA",
  lub uruchom w PowerShell:
    Import-Certificate -FilePath root.cer -CertStoreLocation Cert:\LocalMachine\Root
    Import-Certificate -FilePath inter.cer -CertStoreLocation Cert:\LocalMachine\CA

Zapis hasla wyszarzony:
  DPAPI niedostepne. Wpisuj haslo recznie przy kazdym uruchomieniu.
