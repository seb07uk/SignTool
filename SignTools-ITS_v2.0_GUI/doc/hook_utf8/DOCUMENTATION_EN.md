# Software Documentation
# hook_utf8.py — PyInstaller UTF-8 Runtime Hook

**Version:** 1.1.0 (fixed)  
**Author:** Project Team  
**Date:** 2024  
**Classification:** Internal / Open Source  

---

## Table of Contents

1. [Overview](#overview)
2. [Background & Motivation](#background--motivation)
3. [Architecture](#architecture)
4. [Bug Analysis & Fixes](#bug-analysis--fixes)
5. [API Reference](#api-reference)
6. [Integration Guide](#integration-guide)
7. [Testing](#testing)
8. [Compatibility Matrix](#compatibility-matrix)
9. [Changelog](#changelog)

---

## 1. Overview

`hook_utf8.py` is a PyInstaller runtime hook that guarantees UTF-8 encoding across all standard I/O streams before any application code runs. It is designed to solve the common problem of garbled non-ASCII characters in Windows-packaged Python executables.

### Screenshot — before & after

```
BEFORE (Windows cp1250, no hook):
  C:\> dist\myapp.exe
  Witaj Å›wiecie!   ← corrupted Polish characters

AFTER (with hook_utf8.py):
  C:\> dist\myapp.exe
  Witaj świecie!    ← correct UTF-8 output
```

---

## 2. Background & Motivation

### The Windows Code Page Problem

On Windows, Python's default I/O encoding is determined by the system locale code page:

| Locale | Code Page | Affected languages |
|--------|-----------|-------------------|
| Poland | cp1250 | Polish, Czech, Slovak |
| Russia | cp1251 | Cyrillic scripts |
| Germany| cp1252 | Western European |
| DOS    | cp852  | Legacy terminals |

When a PyInstaller executable runs on such systems, `sys.stdout.encoding` is set to the system code page. Attempting to print a character outside that page results in either:
- **Silent corruption** — the character is replaced or mangled.
- **`UnicodeEncodeError`** — the application crashes.

### Why a Runtime Hook?

PyInstaller runtime hooks are executed at the very start of the bootstrap process, before the frozen application's `__main__` module and before any `import` statement. This guarantees that by the time any user code runs, the encoding is already correct.

---

## 3. Architecture

```
PyInstaller Frozen Executable
┌──────────────────────────────────────────┐
│  1. PyInstaller bootstrap                │
│  2. Runtime hooks (alphabetical order)   │
│     └─ hook_utf8.py  ◄── RUNS HERE       │
│         ├─ Environment variables set     │
│         └─ Stream reconfiguration        │
│  3. sys.path injection                   │
│  4. Application __main__                 │
└──────────────────────────────────────────┘
```

### Internal flow of hook_utf8.py

```
Entry
  │
  ├─► Set os.environ["PYTHONIOENCODING"] = "utf-8"
  │
  ├─► if Python >= 3.7:
  │       Set os.environ["PYTHONUTF8"] = "1"
  │   else:
  │       warnings.warn(RuntimeWarning)
  │
  ├─► _reconfigure(sys.stdin,  "stdin",  errors="replace")
  ├─► _reconfigure(sys.stdout, "stdout", errors="replace")
  └─► _reconfigure(sys.stderr, "stderr", errors="backslashreplace")
         │
         └─ isinstance(io.TextIOWrapper)?  → No  → return
            hasattr("reconfigure")?        → No  → return
            stream.reconfigure(...)
              │
              ├─ Success → done
              └─ Exception → sys.stderr.write(diagnostic message)
```

---

## 4. Bug Analysis & Fixes

### Bug 1 — Missing stdin reconfiguration

**Severity:** High  
**Original code:**
```python
# sys.stdin was NOT reconfigured
```
**Problem:** If the application reads user input or piped data, `sys.stdin` retained the system code page encoding. Reading a UTF-8 byte sequence would raise `UnicodeDecodeError` or silently produce wrong characters.  
**Fix:** Added `_reconfigure(sys.stdin, "stdin", errors="replace")`.

---

### Bug 2 — Incorrect error handler on stderr

**Severity:** Medium  
**Original code:**
```python
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
```
**Problem:** `errors='replace'` on the diagnostic stream replaces undecodable bytes with `?`, destroying forensic information needed for debugging encoding issues.  
**Fix:** Changed to `errors='backslashreplace'`, which renders bytes as `\xNN` escape sequences — preserving all diagnostic data.

---

### Bug 3 — Silent exception suppression

**Severity:** Medium  
**Original code:**
```python
except Exception:
    pass
```
**Problem:** Any failure during reconfiguration was silently discarded. The developer has no indication that the hook failed to apply.  
**Fix:** Added `sys.stderr.write(f"hook_utf8: could not reconfigure {name}: {exc}\n")` in the except block.

---

### Bug 4 — Insufficient type guard

**Severity:** Low  
**Original code:**
```python
if hasattr(sys.stdout, "reconfigure"):
```
**Problem:** `hasattr` alone does not guarantee the object is an `io.TextIOWrapper`. In some PyInstaller configurations, standard streams may be wrapped or replaced by custom objects that happen to have a `reconfigure` attribute with different behaviour.  
**Fix:** Added `isinstance(stream, io.TextIOWrapper)` check before `hasattr`.

---

### Bug 5 — Unconditional PYTHONUTF8 assignment

**Severity:** Low  
**Original code:**
```python
os.environ["PYTHONUTF8"] = "1"
```
**Problem:** `PYTHONUTF8` was introduced in Python 3.7. Setting it on earlier versions has no effect and may confuse tooling that reads environment variables.  
**Fix:** Guarded by `if sys.version_info >= (3, 7)` with a `warnings.warn` fallback.

---

### Bug 6 — Missing `__all__`

**Severity:** Informational  
**Problem:** Without `__all__ = []`, PyInstaller's hook scanner may accidentally pick up module-level names as export symbols.  
**Fix:** Added `__all__: list = []`.

---

## 5. API Reference

### `_reconfigure(stream, name, errors='replace')`

Internal helper function. Reconfigures a text I/O stream to UTF-8 encoding.

| Parameter | Type | Description |
|-----------|------|-------------|
| `stream` | `object` | The stream to reconfigure (`sys.stdin`, `sys.stdout`, or `sys.stderr`) |
| `name` | `str` | Human-readable name for diagnostic messages |
| `errors` | `str` | Python codec error handler (`'replace'`, `'backslashreplace'`, etc.) |

**Returns:** `None`

**Raises:** Never raises. All exceptions are caught and written to `sys.stderr`.

---

### Environment Variables Set

| Variable | Value | Effect |
|----------|-------|--------|
| `PYTHONIOENCODING` | `utf-8` | Sets default I/O encoding for the process and child processes |
| `PYTHONUTF8` | `1` | Enables UTF-8 mode (Python ≥ 3.7), equivalent to `python -X utf8` |

---

## 6. Integration Guide

### Step 1 — Add to your project

```
myproject/
├── myapp.py
├── myapp.spec
└── hooks/
    └── hook_utf8.py
```

### Step 2a — Via `.spec` file (recommended)

```python
# myapp.spec
a = Analysis(
    ['myapp.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    runtime_hooks=['hooks/hook_utf8.py'],   # ← add this
    ...
)
```

### Step 2b — Via command line

```bash
pyinstaller myapp.py \
    --name myapp \
    --runtime-hook hooks/hook_utf8.py \
    --onefile
```

### Step 3 — Verify

After building, run the executable and confirm that non-ASCII characters render correctly:

```bash
dist\myapp.exe
# Expected: Witaj świecie! (not: Witaj ÅwieciE!)
```

---

## 7. Testing

### Manual test

```python
# test_encoding.py  — add to your application for verification
import sys
print(f"stdout encoding : {sys.stdout.encoding}")
print(f"stderr encoding : {sys.stderr.encoding}")
print(f"stdin  encoding : {sys.stdin.encoding}")
print("Polish  : ąęćśźżółń ĄĘĆŚŹŻÓŁŃ")
print("Cyrillic: Привет мир")
print("CJK     : 你好世界")
```

Expected output after hook:
```
stdout encoding : utf-8
stderr encoding : utf-8
stdin  encoding : utf-8
Polish  : ąęćśźżółń ĄĘĆŚŹŻÓŁŃ
Cyrillic: Привет мир
CJK     : 你好世界
```

---

## 8. Compatibility Matrix

| Python | Windows | Linux | macOS | Notes |
|--------|---------|-------|-------|-------|
| 3.6    | ⚠️ Partial | ✅ | ✅ | No PYTHONUTF8; reconfigure unavailable |
| 3.7    | ✅ | ✅ | ✅ | Full support |
| 3.8    | ✅ | ✅ | ✅ | Full support |
| 3.9    | ✅ | ✅ | ✅ | Full support |
| 3.10   | ✅ | ✅ | ✅ | Full support |
| 3.11   | ✅ | ✅ | ✅ | Full support |
| 3.12   | ✅ | ✅ | ✅ | Full support |
| 3.13   | ✅ | ✅ | ✅ | Full support |

**PyInstaller:** 3.x, 4.x, 5.x, 6.x — all supported.

---

## 9. Changelog

### v1.1.0 (current — fixed)
- **Added** `sys.stdin` reconfiguration
- **Changed** `sys.stderr` error handler to `backslashreplace`
- **Fixed** silent exception suppression — diagnostic messages now emitted
- **Added** `isinstance(io.TextIOWrapper)` type guard
- **Added** `sys.version_info` guard for `PYTHONUTF8`
- **Added** `__all__ = []` declaration
- **Refactored** repeated reconfigure logic into `_reconfigure()` helper

### v1.0.0 (original)
- Initial implementation
- Sets `PYTHONIOENCODING` and `PYTHONUTF8`
- Reconfigures `sys.stdout` and `sys.stderr`
