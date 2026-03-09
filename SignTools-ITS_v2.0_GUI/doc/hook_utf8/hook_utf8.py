# -*- coding: utf-8 -*-
# Runtime hook – wymusza UTF-8 PRZED importem jakiegokolwiek modułu aplikacji.
# Bez tego Windows używa cp1250/cp852 i polskie znaki są uszkodzone.
#
# FIXES applied:
#   1. Added sys.stdin reconfiguration (was missing – reading UTF-8 input could fail)
#   2. Changed errors='replace' → errors='backslashreplace' on stderr (safer for diagnostics)
#      and kept errors='replace' only on stdout (user-facing output, acceptable)
#   3. Replaced bare `except Exception: pass` with explicit logging to sys.stderr
#   4. Added isinstance(io.TextIOWrapper) guard before reconfigure (safer than hasattr only)
#   5. Added sys.version_info guard for PYTHONUTF8 (requires Python >= 3.7)
#   6. Added __all__ = [] so PyInstaller hook scanner finds no accidental exports

import io
import os
import sys
import warnings

__all__: list = []

# ── Environment variables ────────────────────────────────────────────────────
# Must be set as early as possible; affects child processes spawned later.
os.environ["PYTHONIOENCODING"] = "utf-8"

if sys.version_info >= (3, 7):
    os.environ["PYTHONUTF8"] = "1"
else:
    warnings.warn(
        "hook_utf8: PYTHONUTF8 requires Python >= 3.7 – skipped.",
        RuntimeWarning,
        stacklevel=1,
    )

# ── Stream reconfiguration ───────────────────────────────────────────────────
def _reconfigure(stream: object, name: str, errors: str = "replace") -> None:
    """Reconfigure a text stream to UTF-8 if possible."""
    if not isinstance(stream, io.TextIOWrapper):
        return
    if not hasattr(stream, "reconfigure"):
        return
    try:
        stream.reconfigure(encoding="utf-8", errors=errors)
    except Exception as exc:  # noqa: BLE001
        # Do NOT silently pass – write a diagnostic so the problem is visible.
        try:
            sys.stderr.write(
                f"hook_utf8: could not reconfigure {name} to UTF-8: {exc}\n"
            )
        except Exception:
            pass  # last-resort: nothing more we can do


# stdin: use 'replace' – better than crashing on unexpected bytes from piped input
_reconfigure(sys.stdin, "stdin", errors="replace")

# stdout: user-facing output – 'replace' keeps the app running, replaces bad chars with '?'
_reconfigure(sys.stdout, "stdout", errors="replace")

# stderr: diagnostic stream – 'backslashreplace' preserves raw byte info for debugging
_reconfigure(sys.stderr, "stderr", errors="backslashreplace")
