Quick DigitalSignature GUI v1.9
================================
by Sebastian Januchowski | polsoft.ITS(tm) Group
Contact: polsoft.its@fastservice.com
Website: https://github.com/seb07uk
Copyright (c) 2026 polsoft.ITS(tm). All rights reserved.

WHAT IT DOES
------------
A lightweight Windows GUI for signing and verifying executables
(.exe, .dll, .msi, .cab) using Microsoft SignTool and a PFX certificate.
No command-line knowledge required.

QUICK START
-----------
1. Place QuickDigitalSignature.exe in the same folder as your .pfx file.
2. Double-click to launch.
3. Select your file, pick a certificate, enter password (if any).
4. Click "Sign File".

REQUIREMENTS
------------
- Windows 10 / 11 (64-bit recommended)
- SignTool.exe (bundled, or installed via Windows SDK, or in PATH)
- Python 3.8+ + Pillow + tkinterdnd2 (only when running from source)

KEY FEATURES
------------
- Sign files with SHA-256
- Verify signature (PA) or signature + timestamp (PA+TS, RFC 3161)
- Secure password storage via Windows DPAPI
- Auto-scan for .pfx certificates
- Drag & drop file selection
- Install Root CA / Intermediate CA
- Dark / Light theme (remembered across sessions)
- Always-on-top toggle
- Session restore (last file, cert, password)
- Rotating log: %APPDATA%\QuickDigitalSignature\app.log

TROUBLESHOOTING
---------------
SignTool not found:
  Place signtool.exe next to the app, or install Windows SDK.

Signature verification fails (untrusted root):
  Use "Install Root CA" / "Install Intermediate CA" buttons,
  or run in PowerShell:
    Import-Certificate -FilePath root.cer -CertStoreLocation Cert:\LocalMachine\Root
    Import-Certificate -FilePath inter.cer -CertStoreLocation Cert:\LocalMachine\CA

Save password greyed out:
  Windows DPAPI unavailable for this session. Enter password manually.
