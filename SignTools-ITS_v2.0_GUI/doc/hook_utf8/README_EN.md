# hook_utf8.py

> **PyInstaller runtime hook** — forces UTF-8 encoding *before* any application module is imported.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Screenshot

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
*Without this hook, Windows (cp1250/cp852) would render the last line as garbled text.*

---

## 🔍 Problem

On Windows, Python defaults to the system code page (`cp1250`, `cp852`, etc.).  
When a PyInstaller-bundled application prints non-ASCII characters — Polish, Cyrillic, CJK — the output is corrupted or raises a `UnicodeEncodeError`.

## ✅ Solution

`hook_utf8.py` is injected by PyInstaller as a **runtime hook**, executed before `__main__` and all application imports. It:

1. Sets `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` in the process environment.
2. Reconfigures `sys.stdin`, `sys.stdout`, and `sys.stderr` to UTF-8 in-process.
3. Uses distinct `errors=` strategies per stream for maximum safety.

---

## 🐛 Bugs Fixed (vs. original)

| # | Issue | Fix |
|---|-------|-----|
| 1 | `sys.stdin` not reconfigured | Added `_reconfigure(sys.stdin, ...)` |
| 2 | `errors='replace'` on stderr silently hid diagnostic bytes | stderr uses `errors='backslashreplace'` |
| 3 | `except Exception: pass` swallowed errors silently | Now writes a diagnostic message to stderr |
| 4 | Only `hasattr` check before `reconfigure()` | Added `isinstance(io.TextIOWrapper)` guard |
| 5 | `PYTHONUTF8` set unconditionally (requires ≥ 3.7) | Guarded by `sys.version_info >= (3, 7)` |
| 6 | No `__all__` declaration | Added `__all__ = []` for clean hook scanning |

---

## 🚀 Installation

### 1. Copy the file

Place `hook_utf8.py` in your project, e.g. `hooks/hook_utf8.py`.

### 2. Reference it in your `.spec` file

```python
# myapp.spec
a = Analysis(
    ['myapp.py'],
    ...
    runtime_hooks=['hooks/hook_utf8.py'],
    ...
)
```

### 3. Or pass it on the command line

```bash
pyinstaller myapp.py --runtime-hook hooks/hook_utf8.py
```

---

## ⚙️ How It Works

```
PyInstaller bootstrap
        │
        ▼
  hook_utf8.py  ◄── runs HERE, before everything
        │
        ├─ os.environ["PYTHONIOENCODING"] = "utf-8"
        ├─ os.environ["PYTHONUTF8"]       = "1"       (Python ≥ 3.7)
        ├─ sys.stdin.reconfigure(utf-8,  errors="replace")
        ├─ sys.stdout.reconfigure(utf-8, errors="replace")
        └─ sys.stderr.reconfigure(utf-8, errors="backslashreplace")
        │
        ▼
   myapp.__main__   ◄── runs with UTF-8 streams guaranteed
```

### Error strategy per stream

| Stream | `errors=` | Rationale |
|--------|-----------|-----------|
| `stdin` | `replace` | Unexpected bytes become `?` — app keeps running |
| `stdout` | `replace` | User-facing output stays readable |
| `stderr` | `backslashreplace` | Diagnostic bytes preserved as `\xNN` for debugging |

---

## 📋 Requirements

- Python **3.6+** (stdin/stdout/stderr reconfigure requires 3.7+; file runs on 3.6 with a warning)
- PyInstaller **3.x** or newer
- Works on **Windows**, **Linux**, **macOS**

---

## 📁 File Structure

```
project/
├── myapp.py
├── myapp.spec
└── hooks/
    └── hook_utf8.py   ← this file
```

---

## 📄 License

MIT © 2024
