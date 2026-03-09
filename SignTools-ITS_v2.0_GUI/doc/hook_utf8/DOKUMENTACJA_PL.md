# Dokumentacja Oprogramowania
# hook_utf8.py — Hook startowy UTF-8 dla PyInstaller

**Wersja:** 1.1.0 (naprawiona)  
**Autor:** Zespół projektowy  
**Data:** 2024  
**Klasyfikacja:** Wewnętrzna / Open Source  

---

## Spis treści

1. [Przegląd](#przegląd)
2. [Kontekst i motywacja](#kontekst-i-motywacja)
3. [Architektura](#architektura)
4. [Analiza błędów i poprawki](#analiza-błędów-i-poprawki)
5. [Dokumentacja API](#dokumentacja-api)
6. [Przewodnik integracji](#przewodnik-integracji)
7. [Testowanie](#testowanie)
8. [Macierz zgodności](#macierz-zgodności)
9. [Historia zmian](#historia-zmian)

---

## 1. Przegląd

`hook_utf8.py` jest hookiem startowym PyInstaller, który gwarantuje kodowanie UTF-8 we wszystkich standardowych strumieniach I/O zanim zostanie uruchomiony jakikolwiek kod aplikacji. Rozwiązuje powszechny problem zniekształconych znaków spoza ASCII w plikach wykonywalnych Python spakowanych dla systemu Windows.

### Zrzut ekranu — przed i po

```
PRZED (Windows cp1250, bez hooka):
  C:\> dist\myapp.exe
  Witaj Å›wiecie!   ← uszkodzone polskie znaki

PO (z hook_utf8.py):
  C:\> dist\myapp.exe
  Witaj świecie!    ← poprawne wyjście UTF-8
```

---

## 2. Kontekst i motywacja

### Problem ze stroną kodową Windows

Na systemie Windows domyślne kodowanie I/O Pythona jest określane przez stronę kodową ustawień regionalnych:

| Ustawienia | Strona kodowa | Języki |
|-----------|---------------|--------|
| Polska | cp1250 | Polski, czeski, słowacki |
| Rosja | cp1251 | Alfabet cyrylicki |
| Niemcy | cp1252 | Europa Zachodnia |
| DOS | cp852 | Terminale legacy |

Gdy plik wykonywalny PyInstaller działa w takich systemach, `sys.stdout.encoding` jest ustawiony na stronę kodową systemu. Próba wypisania znaku spoza tej strony powoduje:
- **Ciche uszkodzenie** — znak jest zastępowany lub zniekształcany.
- **`UnicodeEncodeError`** — aplikacja się crashuje.

### Dlaczego hook startowy?

Hooki startowe PyInstaller są wykonywane na samym początku procesu bootstrap, przed modułem `__main__` zamrożonej aplikacji i przed jakimkolwiek poleceniem `import`. Gwarantuje to, że do czasu uruchomienia kodu użytkownika kodowanie jest już poprawne.

---

## 3. Architektura

```
Zamrożony plik wykonywalny PyInstaller
┌──────────────────────────────────────────┐
│  1. Bootstrap PyInstaller                │
│  2. Hooki startowe (kolejność alfa.)     │
│     └─ hook_utf8.py  ◄── URUCHAMIA SIĘ  │
│         ├─ Ustawienie zmiennych środow.  │
│         └─ Rekonfiguracja strumieni      │
│  3. Wstrzyknięcie sys.path               │
│  4. Aplikacja __main__                   │
└──────────────────────────────────────────┘
```

### Wewnętrzny przepływ hook_utf8.py

```
Start
  │
  ├─► Ustaw os.environ["PYTHONIOENCODING"] = "utf-8"
  │
  ├─► jeśli Python >= 3.7:
  │       Ustaw os.environ["PYTHONUTF8"] = "1"
  │   w przeciwnym razie:
  │       warnings.warn(RuntimeWarning)
  │
  ├─► _reconfigure(sys.stdin,  "stdin",  errors="replace")
  ├─► _reconfigure(sys.stdout, "stdout", errors="replace")
  └─► _reconfigure(sys.stderr, "stderr", errors="backslashreplace")
         │
         └─ isinstance(io.TextIOWrapper)?  → Nie → return
            hasattr("reconfigure")?        → Nie → return
            stream.reconfigure(...)
              │
              ├─ Sukces → gotowe
              └─ Wyjątek → sys.stderr.write(komunikat diagnostyczny)
```

---

## 4. Analiza błędów i poprawki

### Błąd 1 — Brak rekonfiguracji stdin

**Ważność:** Wysoka  
**Oryginalny kod:**
```python
# sys.stdin NIE był rekonfigurowany
```
**Problem:** Jeśli aplikacja odczytuje dane od użytkownika lub dane potokowe, `sys.stdin` zachowywał kodowanie strony kodowej systemu. Odczyt sekwencji bajtów UTF-8 powodowałby `UnicodeDecodeError` lub cicho produkował błędne znaki.  
**Naprawa:** Dodano `_reconfigure(sys.stdin, "stdin", errors="replace")`.

---

### Błąd 2 — Nieprawidłowy handler błędów na stderr

**Ważność:** Średnia  
**Oryginalny kod:**
```python
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
```
**Problem:** `errors='replace'` na strumieniu diagnostycznym zastępuje nierozkodowalne bajty znakiem `?`, niszcząc informacje potrzebne do debugowania problemów z kodowaniem.  
**Naprawa:** Zmieniono na `errors='backslashreplace'`, który renderuje bajty jako sekwencje `\xNN` — zachowując wszystkie dane diagnostyczne.

---

### Błąd 3 — Ciche tłumienie wyjątków

**Ważność:** Średnia  
**Oryginalny kod:**
```python
except Exception:
    pass
```
**Problem:** Każdy błąd podczas rekonfiguracji był po cichu odrzucany. Deweloper nie ma żadnej informacji o tym, że hook nie został zastosowany.  
**Naprawa:** Dodano `sys.stderr.write(f"hook_utf8: nie można rekonfigurować {name}: {exc}\n")` w bloku except.

---

### Błąd 4 — Niewystarczający test typu

**Ważność:** Niska  
**Oryginalny kod:**
```python
if hasattr(sys.stdout, "reconfigure"):
```
**Problem:** Sam `hasattr` nie gwarantuje, że obiekt jest `io.TextIOWrapper`. W niektórych konfiguracjach PyInstaller standardowe strumienie mogą być owinięte lub zastąpione przez niestandardowe obiekty posiadające atrybut `reconfigure` o innym zachowaniu.  
**Naprawa:** Dodano sprawdzenie `isinstance(stream, io.TextIOWrapper)` przed `hasattr`.

---

### Błąd 5 — Bezwarunkowe przypisanie PYTHONUTF8

**Ważność:** Niska  
**Oryginalny kod:**
```python
os.environ["PYTHONUTF8"] = "1"
```
**Problem:** `PYTHONUTF8` został wprowadzony w Pythonie 3.7. Ustawienie go na wcześniejszych wersjach nie ma żadnego efektu i może mylić narzędzia odczytujące zmienne środowiskowe.  
**Naprawa:** Zabezpieczono przez `if sys.version_info >= (3, 7)` z fallbackiem `warnings.warn`.

---

### Błąd 6 — Brak `__all__`

**Ważność:** Informacyjna  
**Problem:** Bez `__all__ = []` skaner hooków PyInstaller może przypadkowo pobrać nazwy na poziomie modułu jako symbole eksportu.  
**Naprawa:** Dodano `__all__: list = []`.

---

## 5. Dokumentacja API

### `_reconfigure(stream, name, errors='replace')`

Wewnętrzna funkcja pomocnicza. Rekonfiguruje strumień tekstowy I/O do kodowania UTF-8.

| Parametr | Typ | Opis |
|----------|-----|------|
| `stream` | `object` | Strumień do rekonfiguracji (`sys.stdin`, `sys.stdout` lub `sys.stderr`) |
| `name` | `str` | Czytelna dla człowieka nazwa do komunikatów diagnostycznych |
| `errors` | `str` | Handler błędów kodeka Python (`'replace'`, `'backslashreplace'` itp.) |

**Zwraca:** `None`

**Rzuca wyjątek:** Nigdy. Wszystkie wyjątki są przechwytywane i zapisywane do `sys.stderr`.

---

### Ustawiane zmienne środowiskowe

| Zmienna | Wartość | Efekt |
|---------|---------|-------|
| `PYTHONIOENCODING` | `utf-8` | Ustawia domyślne kodowanie I/O dla procesu i procesów potomnych |
| `PYTHONUTF8` | `1` | Włącza tryb UTF-8 (Python ≥ 3.7), odpowiednik `python -X utf8` |

---

## 6. Przewodnik integracji

### Krok 1 — Dodaj do projektu

```
mojprojekt/
├── myapp.py
├── myapp.spec
└── hooks/
    └── hook_utf8.py
```

### Krok 2a — Przez plik `.spec` (zalecane)

```python
# myapp.spec
a = Analysis(
    ['myapp.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    runtime_hooks=['hooks/hook_utf8.py'],   # ← dodaj to
    ...
)
```

### Krok 2b — Przez linię poleceń

```bash
pyinstaller myapp.py \
    --name myapp \
    --runtime-hook hooks/hook_utf8.py \
    --onefile
```

### Krok 3 — Weryfikacja

Po zbudowaniu uruchom plik wykonywalny i sprawdź, czy znaki spoza ASCII są renderowane poprawnie:

```bash
dist\myapp.exe
# Oczekiwane: Witaj świecie! (nie: Witaj ÅwieciE!)
```

---

## 7. Testowanie

### Test manualny

```python
# test_encoding.py  — dodaj do aplikacji w celu weryfikacji
import sys
print(f"kodowanie stdout : {sys.stdout.encoding}")
print(f"kodowanie stderr : {sys.stderr.encoding}")
print(f"kodowanie stdin  : {sys.stdin.encoding}")
print("Polskie : ąęćśźżółń ĄĘĆŚŹŻÓŁŃ")
print("Cyryl.  : Привет мир")
print("CJK     : 你好世界")
```

Oczekiwane wyjście po zastosowaniu hooka:
```
kodowanie stdout : utf-8
kodowanie stderr : utf-8
kodowanie stdin  : utf-8
Polskie : ąęćśźżółń ĄĘĆŚŹŻÓŁŃ
Cyryl.  : Привет мир
CJK     : 你好世界
```

---

## 8. Macierz zgodności

| Python | Windows | Linux | macOS | Uwagi |
|--------|---------|-------|-------|-------|
| 3.6 | ⚠️ Częściowa | ✅ | ✅ | Brak PYTHONUTF8; reconfigure niedostępne |
| 3.7 | ✅ | ✅ | ✅ | Pełne wsparcie |
| 3.8 | ✅ | ✅ | ✅ | Pełne wsparcie |
| 3.9 | ✅ | ✅ | ✅ | Pełne wsparcie |
| 3.10 | ✅ | ✅ | ✅ | Pełne wsparcie |
| 3.11 | ✅ | ✅ | ✅ | Pełne wsparcie |
| 3.12 | ✅ | ✅ | ✅ | Pełne wsparcie |
| 3.13 | ✅ | ✅ | ✅ | Pełne wsparcie |

**PyInstaller:** 3.x, 4.x, 5.x, 6.x — wszystkie obsługiwane.

---

## 9. Historia zmian

### v1.1.0 (aktualna — naprawiona)
- **Dodano** rekonfigurację `sys.stdin`
- **Zmieniono** handler błędów `sys.stderr` na `backslashreplace`
- **Naprawiono** ciche tłumienie wyjątków — teraz emitowane są komunikaty diagnostyczne
- **Dodano** sprawdzenie typu `isinstance(io.TextIOWrapper)`
- **Dodano** zabezpieczenie `sys.version_info` dla `PYTHONUTF8`
- **Dodano** deklarację `__all__ = []`
- **Zrefaktoryzowano** powtarzającą się logikę rekonfiguracji do funkcji pomocniczej `_reconfigure()`

### v1.0.0 (oryginalna)
- Pierwsza implementacja
- Ustawia `PYTHONIOENCODING` i `PYTHONUTF8`
- Rekonfiguruje `sys.stdout` i `sys.stderr`
