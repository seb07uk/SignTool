# hook_utf8.py

> **Hook startowy PyInstaller** — wymusza kodowanie UTF-8 *przed* importem jakiegokolwiek modułu aplikacji.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![Platforma](https://img.shields.io/badge/Platforma-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Licencja](https://img.shields.io/badge/Licencja-MIT-green)

---

## 📸 Zrzut ekranu

```
┌─────────────────────────────────────────────────────────────┐
│  Terminal / cmd.exe                                         │
├─────────────────────────────────────────────────────────────┤
│  C:\> myapp.exe                                             │
│  [hook_utf8] stdin  → UTF-8 ✓                               │
│  [hook_utf8] stdout → UTF-8 ✓                               │
│  [hook_utf8] stderr → UTF-8 (backslashreplace) ✓            │
│  Witaj świecie! Cześć! Привет! 你好!                        │
└─────────────────────────────────────────────────────────────┘
```
*Bez tego hooka Windows (cp1250/cp852) wyświetliłby ostatnią linię jako krzaki.*

---

## 🔍 Problem

Na systemie Windows Python domyślnie używa strony kodowej systemu (`cp1250`, `cp852` itp.).  
Gdy aplikacja spakowana przez PyInstaller wypisuje znaki spoza ASCII — polskie, cyrylicę, CJK — wynik jest zniekształcony lub pojawia się błąd `UnicodeEncodeError`.

## ✅ Rozwiązanie

`hook_utf8.py` jest wstrzykiwany przez PyInstaller jako **hook startowy** — uruchamiany przed `__main__` i wszystkimi importami aplikacji. Wykonuje:

1. Ustawia `PYTHONIOENCODING=utf-8` i `PYTHONUTF8=1` w środowisku procesu.
2. Rekonfiguruje `sys.stdin`, `sys.stdout` i `sys.stderr` do UTF-8 w procesie.
3. Stosuje różne strategie `errors=` dla każdego strumienia.

---

## 🐛 Naprawione błędy (względem oryginału)

| # | Problem | Naprawa |
|---|---------|---------|
| 1 | `sys.stdin` nie był rekonfigurowany | Dodano `_reconfigure(sys.stdin, ...)` |
| 2 | `errors='replace'` na stderr cichło ukrywał błędne bajty | stderr używa `errors='backslashreplace'` |
| 3 | `except Exception: pass` pochłaniał błędy bez informacji | Teraz zapisuje komunikat diagnostyczny do stderr |
| 4 | Tylko sprawdzenie `hasattr` przed `reconfigure()` | Dodano sprawdzenie `isinstance(io.TextIOWrapper)` |
| 5 | `PYTHONUTF8` ustawiane bezwarunkowo (wymaga ≥ 3.7) | Zabezpieczono przez `sys.version_info >= (3, 7)` |
| 6 | Brak deklaracji `__all__` | Dodano `__all__ = []` dla czystego skanowania hooka |

---

## 🚀 Instalacja

### 1. Skopiuj plik

Umieść `hook_utf8.py` w projekcie, np. `hooks/hook_utf8.py`.

### 2. Odwołaj się do niego w pliku `.spec`

```python
# myapp.spec
a = Analysis(
    ['myapp.py'],
    ...
    runtime_hooks=['hooks/hook_utf8.py'],
    ...
)
```

### 3. Lub przekaż przez linię poleceń

```bash
pyinstaller myapp.py --runtime-hook hooks/hook_utf8.py
```

---

## ⚙️ Jak to działa

```
Bootstrap PyInstaller
        │
        ▼
  hook_utf8.py  ◄── uruchamia się TUTAJ, przed wszystkim
        │
        ├─ os.environ["PYTHONIOENCODING"] = "utf-8"
        ├─ os.environ["PYTHONUTF8"]       = "1"       (Python ≥ 3.7)
        ├─ sys.stdin.reconfigure(utf-8,  errors="replace")
        ├─ sys.stdout.reconfigure(utf-8, errors="replace")
        └─ sys.stderr.reconfigure(utf-8, errors="backslashreplace")
        │
        ▼
   myapp.__main__   ◄── uruchamia się z gwarantowanymi strumieniami UTF-8
```

### Strategia błędów dla każdego strumienia

| Strumień | `errors=` | Uzasadnienie |
|----------|-----------|--------------|
| `stdin` | `replace` | Nieoczekiwane bajty stają się `?` — aplikacja działa dalej |
| `stdout` | `replace` | Wyjście użytkownika pozostaje czytelne |
| `stderr` | `backslashreplace` | Bajty diagnostyczne zachowane jako `\xNN` do debugowania |

---

## 📋 Wymagania

- Python **3.6+** (rekonfiguracja stdin/stdout/stderr wymaga 3.7+; plik działa na 3.6 z ostrzeżeniem)
- PyInstaller **3.x** lub nowszy
- Działa na **Windows**, **Linux**, **macOS**

---

## 📁 Struktura plików

```
projekt/
├── myapp.py
├── myapp.spec
└── hooks/
    └── hook_utf8.py   ← ten plik
```

---

## 📄 Licencja

MIT © 2024
