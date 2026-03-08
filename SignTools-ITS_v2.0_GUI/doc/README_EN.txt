================================================================================
  SignTool's-ITS GUI v2.0
  Graphical Interface for Code Signing and Certificate Generation
  polsoft.ITS™ Group — creative coding
  © 2026 polsoft.ITS™. All rights reserved.
================================================================================

WHAT IS IT?
-----------
SignTool's-ITS GUI v2.0 is a portable graphical application for Windows that
replaces manual command-line usage of signtool.exe and openssl.exe. All
cryptographic operations — code signing, timestamping, signature verification,
and certificate management — are available through a clean, tabbed interface.

SYSTEM REQUIREMENTS
-------------------
  • Operating System  : Windows 7 SP1 / 8 / 8.1 / 10 / 11 (x64)
  • signtool.exe      : Windows SDK (auto-detected)
  • openssl.exe       : OpenSSL for Windows (auto-detected)
  • Privileges        : Standard user account (no UAC prompt)
  • RAM               : 128 MB minimum
  • Disk Space        : ~30 MB

QUICK START — PREBUILT EXECUTABLE
-----------------------------------
1. Open the folder:  app\
2. Run:              "SignTools-ITS v2.0 GUI.exe"
3. On first launch the app will auto-detect signtool.exe and openssl.exe
   across all connected drives.
4. Click "Apply and close" — you're ready!

BUILDING FROM SOURCE (optional)
---------------------------------
Requirement: Python 3.8+ must be in PATH

  cd SignTools-ITS_v2.0_GUI
  SignTool_GUI_v2.0_build.bat

The script automatically:
  [1/6] Verifies Python installation
  [2/6] Installs PyInstaller (if missing)
  [3/6] Verifies source files
  [4/6] Cleans previous build artifacts
  [5/6] Compiles the EXE with PyInstaller
  [6/6] Opens dist\ in Explorer on success

MAIN FEATURES
-------------
  [Sign]              Sign EXE / DLL / SYS / MSI / CAT / PS1 files
                      Certificate from Windows Store or PFX file
                      Hash algorithms: SHA1 / SHA256 / SHA384 / SHA512
                      Timestamp: RFC 3161 or Authenticode protocol

  [Timestamp/Verify]  Add timestamps to already-signed files
                      Verify digital signatures on any file

  [CatDB/Remove]      Manage Windows catalog database (catdb)
                      Strip Authenticode signatures from signed files

  [Batch]             Batch mode using a signtool response file (@file)
                      Built-in text editor with load/save support

  [Generate Cert]     Self-signed, Root CA, and CA-signed certificates
                      Engine: OpenSSL (recommended) or PowerShell
                      PFX export, Windows certificate store installation

SETTINGS & CONFIGURATION
-------------------------
Configuration file:
  %USERPROFILE%\.polsoft\software\SignToolGUI\SignToolGUI.json

Automatically saved:
  • Paths to signtool.exe and openssl.exe
  • UI language (EN / PL)
  • All form field values

NEVER saved (security):
  • PFX passwords
  • CA key passwords

Generated certificates default location:
  %USERPROFILE%\.polsoft\software\SignToolGUI\Certificates\

LANGUAGE SWITCHING
------------------
Click the [PL] button in the bottom-right corner of the status bar
to switch the interface to Polish.
The switch is instant — no restart required.

ANTIVIRUS NOTE
--------------
If building from source: some AV products may flag freshly compiled
PyInstaller executables as suspicious (false positive).
Add the project folder to your AV exclusions before building.

CONTACT & SUPPORT
-----------------
  Author  : Sebastian Januchowski
  Company : polsoft.ITS™ Group
  E-mail  : polsoft.its@fastservice.com
  GitHub  : github.com/seb07uk

LICENSE
-------
Proprietary software. All rights reserved — polsoft.ITS™ Group.
Unauthorized copying, modification, or distribution is strictly prohibited.

================================================================================
  polsoft.ITS™ Group — creative coding — 2026©
================================================================================
