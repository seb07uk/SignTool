<div align="center">

<img src="Ikona SignTool's-ITS2.ico" alt="SignTool's-ITS Logo" width="96"/>

# SignTool's-ITS GUI v2.0

**Graphical interface for code signing and certificate generation**

*Microsoft SignTool & OpenSSL — Windows 7 / 8 / 10 / 11*

[![Version](https://img.shields.io/badge/version-2.0.0-0078D4?style=flat-square)](https://github.com/seb07uk)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D4?style=flat-square&logo=windows)](https://github.com/seb07uk)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/license-Proprietary-c0392b?style=flat-square)](LICENSE)
[![Company](https://img.shields.io/badge/polsoft.ITS™-Group-0a1a2e?style=flat-square)](https://github.com/seb07uk)
[![Language](https://img.shields.io/badge/UI-PL%20%2F%20EN-27ae60?style=flat-square)](#bilingual-interface-ple)

---

*A professional, single-file portable executable that brings the full power of Microsoft SignTool and OpenSSL into a clean, modern graphical interface — no command line required.*

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features at a Glance](#features-at-a-glance)
- [System Requirements](#system-requirements)
- [Installation & Build](#installation--build)
- [Tabs & Modules — Full Reference](#tabs--modules--full-reference)
  - [Sign — Code Signing](#1--sign--code-signing)
  - [Timestamp / Verify](#2--timestamp--verify)
  - [CatDB / Remove](#3--catdb--remove)
  - [Batch — Response File](#4--batch--response-file)
  - [Generate Certificate](#5--generate-certificate)
- [Signing Types & Methods](#signing-types--methods)
- [Certificate Types](#certificate-types)
- [Cryptographic Parameters](#cryptographic-parameters)
- [Auto-Detection of Tools](#auto-detection-of-tools)
- [Configuration & Persistence](#configuration--persistence)
- [Bilingual Interface PL/EN](#bilingual-interface-ple)
- [Project Structure](#project-structure)
- [Build System](#build-system)
- [Architecture & Technical Notes](#architecture--technical-notes)
- [Author & Contact](#author--contact)
- [License](#license)

---

## Overview

**SignTool's-ITS GUI v2.0** is a comprehensive graphical front-end developed by **polsoft.ITS™ Group** for two industry-standard tools:

- **Microsoft `signtool.exe`** — the official Windows code-signing utility from the Windows SDK
- **`openssl.exe`** — the cross-platform cryptographic toolkit

The application eliminates the need to memorize complex command-line flags by exposing every signing, timestamping, verification, and certificate-generation capability through a clearly organized tabbed interface. All operations execute asynchronously — the GUI remains responsive while commands run in the background, with live, color-coded output streamed directly into the result pane.

The application ships as a **single portable `.exe`** — no installer, no runtime dependencies, no administrator rights required.

> **Target users:** Software developers, IT administrators, DevOps engineers, code-signing officers, and security professionals who sign binaries, drivers, installers, scripts, or catalog files on Windows on a daily basis.

---

## Features at a Glance

| Feature | Detail |
|---|---|
| 🔎 **Tool Auto-detection** | Scans all drives for `signtool.exe` and `openssl.exe` at startup; shows LED status indicators |
| 🖊️ **Code Signing** | Full `signtool sign` support — EXE, DLL, SYS, MSI, CAT, PS1, and any signable format |
| ⏱️ **Timestamping** | RFC 3161 (`/tr`) and Authenticode (`/t`) timestamp protocols, selectable per operation |
| ✅ **Signature Verification** | `signtool verify` with `/pa`, `/pg`, `/v`, and catalog file (`/c`) options |
| 🗂️ **CatDB Management** | Add (`/u`) or remove (`/r`) catalog files from the Windows catalog database |
| 🗑️ **Signature Removal** | Strip Authenticode signatures from any signed file (`signtool remove /s`) |
| 📦 **Batch / Response File** | Full `signtool @response_file` support with built-in editor, load, and save |
| 🔑 **Certificate Generation** | Self-signed, Root CA, and CA-signed certificates via OpenSSL or PowerShell |
| 🌐 **Bilingual UI** | Polish and English with runtime language switching — no restart required |
| 🔐 **Certificate Store** | Sign from Windows Certificate Store (by name or SHA1) or directly from a PFX file |
| 📋 **Cross-certification** | Additional certificate (`/ac`) support for cross-certification chains |
| 🛑 **Stop Button** | Terminate any running `signtool`/`openssl`/`powershell` process instantly |
| 💾 **Persistent Settings** | Form state, tool paths, and language preference saved to `SignToolGUI.json` |
| 🖥️ **DPI Aware** | Per-Monitor DPI V2 awareness — sharp rendering on HiDPI and 4K displays |
| 🚀 **Portable EXE** | Single-file PyInstaller build — copy and run anywhere |
| 🔇 **No Console Flash** | Windows manifest + `CREATE_NO_WINDOW` eliminate subprocess console flickering |
| 🎨 **Color-coded Output** | Success (green), error (red), warning (orange), command (cyan) in dark terminal theme |
| ⚙️ **Tooltip System** | 2-second hover tooltips on every control, dynamically translated on language switch |

---

## System Requirements

| Component | Requirement |
|---|---|
| **Operating System** | Windows 7 SP1 / 8 / 8.1 / 10 / 11 (x64) |
| **Python** *(source build only)* | Python 3.8 or newer |
| **PyInstaller** *(source build only)* | Installed automatically by build script |
| **signtool.exe** | Windows SDK — auto-detected on startup, or specified manually |
| **openssl.exe** | OpenSSL for Windows — auto-detected on startup, or specified manually |
| **PowerShell** | Required only for the PowerShell certificate generation method |
| **Privileges** | Standard user — **no administrator rights required** (admin needed only for certificate store installation) |

> The compiled `SignTool.exe` requires **no Python installation**. Python is only needed when building from source.

---

## Installation & Build

### Option A — Use Prebuilt Executable

The `app/` directory contains a ready-to-run executable:

```
SignTools-ITS_v2.0_GUI/
└── app/
    └── SignTools-ITS v2.0 GUI.exe   ← run directly, no installation
```

Copy it anywhere and launch. The application will auto-detect tools on first run.

### Option B — Build from Source

**Prerequisites:** Python 3.8+ must be in `PATH`.

```batch
cd SignTools-ITS_v2.0_GUI
SignTool_GUI_v2.0_build.bat
```

The build script performs the following six steps automatically:

```
[1/6]  Verify Python installation
[2/6]  Install PyInstaller (if not already present)
[3/6]  Verify all required source files are present
[4/6]  Clean previous build artifacts (dist/, build/)
[5/6]  Compile with PyInstaller using SignTool.spec
[6/6]  Post-build cleanup → output: dist\SignTool.exe
```

On success, `dist\SignTool.exe` is opened automatically in Explorer.

> **Antivirus note:** Some AV products flag freshly compiled PyInstaller executables as suspicious. Add the project folder to your AV exclusions before building.

---

## Tabs & Modules — Full Reference

The application is organized into five main tabs, each with an inner **Options** sub-tab (for configuration) and a **Output** sub-tab (for live command output).

---

### 1 · Sign — Code Signing

The Sign tab exposes the full `signtool sign` command through a scrollable form.

#### Files to Sign

A multi-file listbox accepts EXE, DLL, SYS, MSI, CAT, PS1, and any other signable format. Files are added via the **Add files** button (opens a multi-select dialog) and can be removed individually or all at once.

#### Certificate Section

Two mutually exclusive certificate sources are available, selected via radio buttons:

**From Windows Certificate Store**

| Field | SignTool flag | Description |
|---|---|---|
| Certificate name | `/n` | Subject name substring match against the store |
| Certificate SHA1 | `/sha1` | Exact 40-character hexadecimal thumbprint |

Both fields can be used simultaneously — SignTool will use them together to narrow the selection.

**From PFX File**

| Field | SignTool flag | Description |
|---|---|---|
| Certificate file | `/f` | Path to the `.pfx` file |
| Password | `/p` | PFX private key password (masked input, never saved to disk) |

**Additional Certificate (Cross-certification)**

| Field | SignTool flag | Description |
|---|---|---|
| Additional cert | `/ac` | Path to an additional `.cer` or `.crt` file for cross-certification chains |

#### Signing Options

| Option | SignTool flag | Description |
|---|---|---|
| Hash algorithm | `/fd` | File digest algorithm: SHA1, SHA256, SHA384, SHA512 |
| Description | `/d` | Human-readable description embedded in the signature |
| URL | `/du` | URL embedded in the signature (authenticode description URL) |

#### Timestamp Options

| Option | SignTool flag | Description |
|---|---|---|
| Timestamp server URL | `/tr` or `/t` | URL of the TSA server |
| **RFC 3161** (radio) | `/tr` + `/td` | Modern RFC 3161 protocol — recommended for all new signing |
| **Authenticode** (radio) | `/t` | Legacy Authenticode timestamp — for Windows XP / Server 2003 compatibility |
| Timestamp hash | `/td` | Timestamp digest algorithm (SHA1 / SHA256 / SHA384 / SHA512) — RFC 3161 only |

> **Best practice:** Always use RFC 3161 (`/tr`) unless you specifically need to support pre-Vista systems. Authenticode timestamps (`/t`) use SHA1 and are not compatible with the `/td` hash option.

#### Additional Flags

| Checkbox | SignTool flag | Description |
|---|---|---|
| Append signature | `/as` | Add a second signature without removing the existing one (dual-signing) |
| Verbose mode | `/v` | Print detailed signing information |
| Debug mode | `/debug` | Print debugging information for troubleshooting |

#### Actions

- **🔏 Sign** — Executes `signtool sign` with all configured options; switches to the Output tab automatically
- **Show command** — Renders the full command string in the Output tab without executing it

---

### 2 · Timestamp / Verify

This tab combines two operations in a single vertically split pane, each with its own output section.

#### Timestamp Section

Adds an RFC 3161 or Authenticode timestamp to already-signed files (without re-signing).

| Field | SignTool flag | Description |
|---|---|---|
| Files | — | Multi-file listbox (EXE, DLL, SYS) |
| Server URL | `/tr` or `/t` | TSA server address |
| **RFC 3161** (radio) | `/tr` | Modern timestamp protocol |
| **Authenticode** (radio) | `/t` | Legacy timestamp protocol |
| Hash (`/td`) | `/td` | Timestamp digest (RFC 3161 only): SHA1, SHA256, SHA384, SHA512 |
| Verbose | `/v` | Detailed output |

**Action:** **Add timestamp** — runs `signtool timestamp` in a background thread.

#### Verify Section

Verifies the digital signature on one or more files.

| Field | SignTool flag | Description |
|---|---|---|
| Files | — | Multi-file listbox |
| Verify all signatures | `/pa` | Use the default authentication policy to verify all signatures |
| Verify page signature | `/pg` | Verify the page hash embedded in the signature |
| Verbose | `/v` | Print complete chain and signature details |
| Catalog file | `/c` | Specify a `.cat` catalog file to verify against |

**Action:** **Verify** — runs `signtool verify` and streams the result to the Verify Output pane.

---

### 3 · CatDB / Remove

Another combined tab with two independent operation sections.

#### CatDB Section

Manages entries in the Windows catalog database (`catdb`).

| Field | SignTool flag | Description |
|---|---|---|
| Catalog file | — | Path to the `.cat` catalog file |
| Action | `/u` or `/r` | **Add** (`/u` — assign unique ID) or **Remove** (`/r`) the catalog |
| Verbose | `/v` | Detailed output |
| Default catalog DB | `/d` | Always included — uses the default system catalog database |

**Action:** **Execute CatDB** — runs `signtool catdb /d [/u|/r] <file>`.

#### Remove — Strip Signatures

Removes all Authenticode signatures from signed files.

| Field | SignTool flag | Description |
|---|---|---|
| Files | — | Multi-file listbox |
| Remove signatures | `/s` | **Always active** — required flag; `signtool remove` always requires `/s` |
| Verbose | `/v` | Detailed output |

> **Note:** The `/s` flag is mandatory and cannot be deselected — this is a `signtool` requirement, not a GUI restriction.

**Action:** **Remove signatures** — runs `signtool remove /s [/v] <files>`.

---

### 4 · Batch — Response File

Executes `signtool` using a response file (also called an "answer file"), where the entire command is defined as one argument per line.

#### Response File Format

```
sign
/n
My Code Signing Certificate
/fd
SHA256
/tr
http://timestamp.digicert.com
/td
SHA256
MyApplication.exe
```

The first line is the `signtool` subcommand; subsequent lines are its arguments in order.

#### Features

- **Built-in text editor** — Edit the response file directly in the GUI with a monospace font and horizontal scroll
- **Load** — Import any existing `.txt` response file from disk
- **Save** — Export the current editor content to a `.txt` file
- **Clear** — Empty the editor in one click
- **Execute response file** — Writes the editor content to a temporary file and runs `signtool @<tempfile>` in a background thread; the temp file is deleted only after the process exits (no race condition)

---

### 5 · Generate Certificate

The most feature-rich tab — supports three certificate types and two generation engines.

#### Generation Method

| Method | Description |
|---|---|
| **OpenSSL** *(recommended)* | Cross-platform, full control over all parameters; supports RSA and EC key algorithms, SAN extensions, and CA chains |
| **PowerShell** `New-SelfSignedCertificate` | Windows-native; generates directly into the Windows certificate store; exports to PFX and CRT |

When OpenSSL is selected, the path to `openssl.exe` is shown and can be adjusted (auto-detected from config, application folder, `_MEIPASS`, system PATH, and common install locations).

#### Certificate Type

| Type | Description |
|---|---|
| **Self-signed** | Standalone certificate; includes `extendedKeyUsage=codeSigning` and `keyUsage=digitalSignature` extensions |
| **Root CA** | Certification Authority certificate; includes `basicConstraints=critical,CA:TRUE` and `keyUsage=critical,keyCertSign,cRLSign` |
| **Signed by CA** | End-entity certificate signed by an existing Root CA; generates a CSR first, then signs it using the provided CA cert and key |

#### Certificate Data (Subject)

| Field | OpenSSL flag | Description |
|---|---|---|
| Name (CN) | `CN=` | Common Name — required |
| Organization (O) | `O=` | Organization name |
| Country (C) | `C=` | Two-letter ISO country code (e.g. `PL`, `US`) — validated |
| City (L) | `L=` | Locality / city |
| State (ST) | `ST=` | State or province |
| E-mail | `emailAddress=` | Contact e-mail — validated for `@` presence |

#### Cryptographic Parameters

| Parameter | Options | Description |
|---|---|---|
| Key algorithm | RSA / EC | RSA uses a fixed key size; EC uses a named curve |
| RSA key size | 2048 / 3072 / 4096 | Bits; 2048 is the minimum recommended today |
| EC curve | prime256v1 / secp384r1 / secp521r1 | NIST P-256, P-384, P-521 |
| Hash algorithm | sha256 / sha384 / sha512 | Signature digest algorithm |
| Validity | 1 – N days | Certificate lifetime in days; validated as positive integer |

#### Subject Alternative Names (SAN) — Optional

| Field | Extension | Description |
|---|---|---|
| DNS names | `DNS:` | One hostname per line (e.g. `localhost`, `myapp.example.com`) |
| IP addresses | `IP:` | One IP per line (e.g. `127.0.0.1`, `192.168.1.10`) |

SAN extensions are written to a temporary file (Windows-compatible; avoids the `/dev/stdin` limitation).

#### CA Certificate (Signed by CA mode only)

| Field | OpenSSL flag | Description |
|---|---|---|
| CA cert file | `-CA` | Path to Root CA certificate (`.crt`, `.pem`, `.cer`) |
| CA key file | `-CAkey` | Path to Root CA private key (`.key`, `.pem`) |
| CA key password | `-passin pass:` | Password for the CA private key (masked, never saved) |

#### Output Files

| Field | Description |
|---|---|
| Output folder | Directory where all generated files are saved; defaults to `~\.polsoft\software\SignToolGUI\Certificates` |
| Base file name | Prefix for all output files (e.g. `mycert` → `mycert.key`, `mycert.crt`, `mycert.pfx`) |
| PFX password | Password to protect the exported PFX file (empty = no password) |
| Export PFX | Runs `openssl pkcs12 -export` to bundle the key + certificate into a `.pfx` |
| Install in Windows store | Imports the PFX into `Cert:\CurrentUser\My` using PowerShell `Import-PfxCertificate` (requires admin for machine store) |

#### Actions

- **Generate certificate** — Executes all OpenSSL commands (or the PowerShell script) sequentially in a background thread with step-by-step progress output
- **Show commands** — Displays the full set of OpenSSL commands or the PowerShell script in the Output pane without executing them; useful for review or manual use

---

## Signing Types & Methods

### Timestamp Protocols

| Protocol | Flag | Standard | Compatibility | Notes |
|---|---|---|---|---|
| RFC 3161 | `/tr` + `/td` | IETF RFC 3161 | Windows Vista+ | **Recommended.** Supports SHA-256 timestamps, long-term validity |
| Authenticode | `/t` | Microsoft proprietary | Windows XP+ | Legacy only. SHA1-based. No `/td` support |

### Hash Algorithms for Signing (`/fd`)

| Algorithm | Security level | Recommended for |
|---|---|---|
| SHA1 | Deprecated | Legacy systems only (Windows XP) |
| SHA256 | Current standard | All modern Windows versions (**default**) |
| SHA384 | High security | High-assurance applications |
| SHA512 | Maximum | Maximum security requirements |

### Certificate Sources

| Source | How specified | Use case |
|---|---|---|
| Windows Store by name | `/n <SubjectName>` | Certificate stored in the local certificate store |
| Windows Store by SHA1 | `/sha1 <thumbprint>` | Precise selection when multiple certs match the name |
| PFX file | `/f <path> /p <pass>` | Certificate on disk or removable media |
| Additional cert | `/ac <path>` | Cross-certification or chain completion |

---

## Certificate Types

| Type | OpenSSL extensions | Use case |
|---|---|---|
| Self-signed | `extendedKeyUsage=codeSigning`, `keyUsage=digitalSignature` | Development, testing, internal signing |
| Root CA | `basicConstraints=critical,CA:TRUE`, `keyUsage=critical,keyCertSign,cRLSign` | Build an internal PKI hierarchy |
| Signed by CA | `extendedKeyUsage=codeSigning`, `keyUsage=digitalSignature`, optional SAN | Production signing by an internal CA |

---

## Cryptographic Parameters

### Key Algorithms

| Algorithm | Key sizes / curves | Notes |
|---|---|---|
| RSA | 2048, 3072, 4096 bits | Universal compatibility; 2048 minimum for code signing |
| EC (Elliptic Curve) | prime256v1, secp384r1, secp521r1 | Smaller keys, equivalent or better security; not supported on all platforms |

### Hash Algorithms

| Algorithm | Output size | Suitable for |
|---|---|---|
| sha256 | 256 bits | Standard (**default**) |
| sha384 | 384 bits | High-security applications |
| sha512 | 512 bits | Maximum security |

---

## Auto-Detection of Tools

On startup (200 ms after the UI loads), the application launches a background scan for both required tools. The detection dialog shows:

- **signtool.exe** — searched in saved config → application folder → `_MEIPASS` → system `PATH` → Windows SDK installation paths across all drives (`A:` through `Z:`)
- **openssl.exe** — searched in saved config → application folder → `_MEIPASS` → system `PATH` → common OpenSSL install directories and Git distributions

Detection results are shown with ✅ / ❌ indicators. The **Apply and close** button saves the found paths and updates the LED indicators in the status bar. **Retry scan** re-runs the full disk scan.

### Status Bar LEDs

Two colored LEDs in the bottom-right corner indicate tool availability at a glance:

- 🟢 **Green** — tool found and path saved
- 🔴 **Red** — tool not found

---

## Configuration & Persistence

All settings are stored in `%USERPROFILE%\.polsoft\software\SignToolGUI\SignToolGUI.json`.

**Saved on close:**

- Tool paths (`signtool_path`, `openssl_path`)
- UI language (`"pl"` or `"en"`)
- All form field values (server URLs, hash algorithms, certificate paths, SAN entries, output directories, etc.)

**Never saved (security):**

- `sign_cert_password` — PFX password
- `certgen_pfx_pass` — generated PFX password
- `certgen_ca_key_pass` — CA key password

Certificates generated via OpenSSL are stored in `%USERPROFILE%\.polsoft\software\SignToolGUI\Certificates\` by default.

---

## Bilingual Interface PL/EN

The interface is fully bilingual with all strings defined in an internal translation dictionary (`_TR`). Language switching happens at runtime without restarting — the application:

1. Saves the current form state
2. Rebuilds all tabs with the new language
3. Restores form state
4. Saves the language preference to `SignToolGUI.json`

The language toggle button (bottom-right of the status bar) shows the language you will switch **to** (e.g., clicking `EN` when in Polish mode switches to English).

All tooltips are dynamically translated — they always reflect the current language, even for tooltips on widgets created before the switch.

---

## Project Structure

```
SignTools-ITS_v2.0_GUI/
│
├── main.py                    # Application source — 5 360 lines
├── SignTool.spec              # PyInstaller build specification (one-file, windowed)
├── SignTool_GUI_v2.0_build.bat # Build script (6-step automated build)
├── SignTool.manifest          # Windows application manifest
│                              #   • Enforces Windows GUI subsystem from byte 0
│                              #   • PerMonitorV2 DPI awareness
│                              #   • Long path support (>260 chars)
│                              #   • Compatibility: Windows 7 / 8 / 8.1 / 10 / 11
│                              #   • Execution level: asInvoker (no UAC prompt)
├── version_info.txt           # PE version info (FileVersion 2.0.0.0)
├── hook_utf8.py               # PyInstaller runtime hook — forces UTF-8 encoding
├── SignTool-ico.ico           # Application icon (used by PyInstaller for EXE)
├── Ikona SignTool's-ITS2.ico  # Source icon file
│
├── app/
│   └── SignTools-ITS v2.0 GUI.exe   # Prebuilt portable executable
│
└── doc/                       # Documentation folder
```

---

## Build System

The build is driven by `SignTool.spec` (PyInstaller spec file) and `SignTool_GUI_v2.0_build.bat`:

| Setting | Value |
|---|---|
| Build mode | One-file (`onefile`) |
| Window mode | `windowed=True`, `console=False` |
| Icon | `SignTool-ico.ico` (embedded in EXE) |
| Runtime tmpdir | `None` (uses `%TEMP%` — eliminates console flash) |
| UPX compression | Disabled |
| Version info | `version_info.txt` (PE metadata) |
| Manifest | `SignTool.manifest` (DPI + subsystem) |
| Runtime hook | `hook_utf8.py` (UTF-8 encoding) |
| Hidden imports | `tkinter`, `tkinter.ttk`, `tkinter.filedialog`, `tkinter.messagebox`, `tkinter.scrolledtext`, `json`, `threading`, `subprocess`, `pathlib`, `tempfile`, `base64` |

The application icon and logo PNG are embedded as Base64 strings inside `main.py` — the EXE requires no external asset files at runtime.

---

## Architecture & Technical Notes

- **Threading model:** Every `signtool`/`openssl`/`powershell` subprocess runs in a `daemon=True` background thread. Output is streamed line-by-line and posted to the main thread via `root.after(0, ...)` to avoid Tkinter threading violations.
- **Stop button:** Stores a reference to `subprocess.Popen` in `self._current_process`; calls `proc.kill()` on demand.
- **No console flash:** `subprocess.Popen` is monkey-patched at module level on Windows to always include `CREATE_NO_WINDOW` in `creationflags`.
- **Icon embedding:** The application icon is Base64-decoded at runtime, written to a temp `.ico` file, set via `root.iconbitmap()`, then deleted after 1 second.
- **SAN temp files:** For CA-signed certificate generation, OpenSSL extension files are written to a temp file in the output directory (Windows has no `/dev/stdin`). The file is deleted after the signing step completes.
- **UTF-8 throughout:** `hook_utf8.py` reconfigures `sys.stdout` and `sys.stderr`; `PYTHONIOENCODING=utf-8` is set in the environment; all file I/O uses `encoding='utf-8'`.
- **Password security:** PFX and CA key passwords are never written to the JSON config file, even across language switches or window close events.

---

## Author & Contact

| Field | Value |
|---|---|
| **Project Manager** | Sebastian Januchowski |
| **Company** | polsoft.ITS™ Group |
| **E-mail** | polsoft.its@fastservice.com |
| **GitHub** | [github.com/seb07uk](https://github.com/seb07uk) |
| **Copyright** | 2026© polsoft.ITS™. All rights reserved. |

---

## License

This software is **proprietary**. All rights reserved by polsoft.ITS™ Group.

Unauthorized copying, modification, distribution, or use of this software, in whole or in part, without the express written permission of polsoft.ITS™ Group is strictly prohibited.

---

<div align="center">

*Made with ❤️ by polsoft.ITS™ Group — 2026©*

</div>
