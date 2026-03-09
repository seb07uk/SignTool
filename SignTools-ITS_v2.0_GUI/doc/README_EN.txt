================================================================================
  SignTool's-ITS GUI v2.0
  Code Signing & Certificate Generation — Microsoft SignTool & OpenSSL
  Copyright 2026© polsoft.ITS™ Group. All rights reserved.
================================================================================

QUICK START
-----------
  python main.py

  Requirements:  Python 3.9+  |  Windows 10/11  |  No external packages needed

  signtool.exe  — Windows SDK (auto-detected at launch)
  openssl.exe   — Required for cert generation (auto-detected at launch)

  Missing tools? The startup dialog lets you locate them manually.

BUILD STANDALONE EXE
--------------------
  pip install pyinstaller
  pyinstaller --noconsole --onefile main.py
  -> Output: dist/main.exe  (no Python required on target machine)

TABS
----
  Sign               Sign EXE, DLL, scripts (cert store or PFX, SHA-256/SHA-512)
  Timestamp/Verify   Add RFC3161 / Authenticode timestamps; verify signatures
  CatDB / Remove     Manage Windows catalog DB; strip signatures from binaries
  Batch              Execute signtool response files (one arg per line)
  Generate Cert      Self-signed / Root CA / CA-signed via OpenSSL or PowerShell
  Options            Switch language PL <-> EN; adjust tool paths
  Output             Colour-coded streaming output for all operations

NOTES
-----
  - Language switchable at runtime (PL / EN)
  - Console flash suppressed on Windows (CREATE_NO_WINDOW)
  - All subprocess calls run in daemon threads — GUI stays responsive
  - Admin rights required for CatDB and Windows cert store operations
  - Settings are not saved between sessions

--------------------------------------------------------------------------------
  Author  : Sebastian Januchowski
  Company : polsoft.ITS™ Group
  Contact : polsoft.its@fastservice.com
  GitHub  : https://github.com/seb07uk
  License : Proprietary
================================================================================
