hook_utf8.py — Hook startowy UTF-8 dla PyInstaller
===================================================
Wersja: 1.1.0 (naprawiona)

CO ROBI
-------
Wymusza kodowanie UTF-8 na stdin/stdout/stderr PRZED uruchomieniem kodu aplikacji.
Zapobiega zniekształcaniu polskich/cyrylickich/CJK znaków w plikach EXE dla Windows.

SZYBKI START
------------
1. Skopiuj hook_utf8.py do projektu (np. do folderu hooks/)
2. Dodaj do pliku .spec:
     runtime_hooks=['hooks/hook_utf8.py']
   LUB użyj linii poleceń:
     pyinstaller myapp.py --runtime-hook hooks/hook_utf8.py

NAPRAWIONE BLEDY wzgledem oryginalu
------------------------------------
- sys.stdin nie byl rekonfigurowany (odczyt UTF-8 mogl nie dzialac)
- stderr uzywalo errors='replace' (teraz backslashreplace dla bezpieczniejszej diagnostyki)
- Wyjatki byly po cichu tlumione (teraz logowany jest komunikat diagnostyczny)
- Uzywano tylko sprawdzenia hasattr() (teraz rowniez isinstance(io.TextIOWrapper))
- PYTHONUTF8 ustawiany bezwarunkowo (teraz tylko dla Python >= 3.7)
- Brak deklaracji __all__ (dodana)

WYMAGANIA
---------
- Python 3.6+ (pelne wsparcie od 3.7+)
- PyInstaller 3.x lub nowszy
- Windows / Linux / macOS

PLIKI
-----
hook_utf8.py         Naprawiony hook startowy (uzyj tego)

KONTAKT
-------
Odwiedz repozytorium projektu w celu zglaszania bledow i contribucji.
