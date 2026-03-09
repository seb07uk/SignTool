hook_utf8.py — PyInstaller UTF-8 Runtime Hook
==============================================
Version: 1.1.0 (fixed)

WHAT IT DOES
------------
Forces UTF-8 encoding on stdin/stdout/stderr BEFORE any application code runs.
Prevents garbled Polish/Cyrillic/CJK characters in Windows executables.

QUICK START
-----------
1. Copy hook_utf8.py to your project (e.g. hooks/ folder)
2. Add to your .spec file:
     runtime_hooks=['hooks/hook_utf8.py']
   OR use CLI:
     pyinstaller myapp.py --runtime-hook hooks/hook_utf8.py

BUGS FIXED vs ORIGINAL
-----------------------
- sys.stdin was not reconfigured (reading UTF-8 input could fail)
- stderr used errors='replace' (now uses backslashreplace for safer diagnostics)
- Exceptions were silently swallowed (now logs a diagnostic message)
- Only hasattr() check used (now also isinstance(io.TextIOWrapper))
- PYTHONUTF8 set unconditionally (now guarded: Python >= 3.7 only)
- Missing __all__ declaration (added)

REQUIREMENTS
------------
- Python 3.6+ (full support from 3.7+)
- PyInstaller 3.x or newer
- Windows / Linux / macOS

FILES
-----
hook_utf8.py         Fixed runtime hook (use this one)

CONTACT
-------
See project repository for issues and contributions.
