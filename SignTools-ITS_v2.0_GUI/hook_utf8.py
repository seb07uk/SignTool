# -*- coding: utf-8 -*-
# Runtime hook – wymusza UTF-8 PRZED importem jakiegokolwiek modułu aplikacji.
# Bez tego Windows używa cp1250/cp852 i polskie znaki są uszkodzone.
import os
import sys

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
