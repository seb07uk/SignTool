# SignTool's-ITS GUI v2.0

> **Graphical interface for code signing and certificate generation**  
> Microsoft SignTool & OpenSSL — Windows | v2.0

---

![SignTool's-ITS GUI](https://raw.githubusercontent.com/seb07uk/seb07uk/main/signtool_preview.png)

> *Screenshot: Main application window — Sign tab with certificate selection and signing options*

---

## Overview

**SignTool's-ITS GUI** is a professional graphical front-end for `signtool.exe` (Microsoft) and `openssl.exe`, delivering a complete code-signing workflow through a clean, bilingual (PL/EN) interface built on Python Tkinter.

No command-line knowledge required — all signing, timestamping, verification, and certificate operations are accessible through intuitive tabs and form fields.

---

## Features

| Category | Capabilities |
|---|---|
| **Sign** | Sign executables, DLLs, scripts; PFX file or Windows Certificate Store; SHA-256/SHA-512 hash algorithms |
| **Timestamp** | RFC3161 (modern) and Authenticode (legacy) timestamp servers |
| **Verify** | Verify all signatures (`/pa`), page signatures (`/pg`), optional catalog file |
| **CatDB** | Add/remove catalog files to/from the Windows catalog database |
| **Remove** | Strip Authenticode signatures from binaries |
| **Batch** | Response file editor — execute signtool response files directly from the GUI |
| **Certificate Generator** | Generate self-signed, Root CA, or CA-signed certificates via OpenSSL or PowerShell |
| **Language** | Full PL / EN bilingual UI switchable at runtime |

---

## Requirements

- **OS:** Windows 10 / 11 (64-bit)
- **Python:** 3.9+ (standard library only — no external packages required)
- **signtool.exe:** Part of Windows SDK — auto-detected at startup
- **openssl.exe:** Required for certificate generation — auto-detected at startup

> The application scans all drives at launch and reports which tools were found. Missing tools can be pointed to manually via a file dialog.

---

## Installation & Launch

```bash
# Clone or download main.py
git clone https://github.com/seb07uk/signtool-its-gui

# Run directly — no install needed
python main.py
```

Or build a standalone EXE:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile main.py
```

---

## Application Tabs

### Sign
Select files to sign, choose a certificate (from the Windows store by name/SHA1 or from a PFX file with password), configure hash algorithm, description, URL, and timestamp server. Dual signing (append `/as`) and debug mode are supported.

### Timestamp / Verify
Add a timestamp to already-signed files, or verify existing signatures against a catalog.

### CatDB / Remove
Manage the Windows catalog database and strip signatures from binaries.

### Batch
Load, edit, and execute signtool response files. Each argument goes on a separate line; the first line is the command (`sign`, `verify`, etc.).

### 🔑 Generate Certificate
Generate certificates using OpenSSL or PowerShell's `New-SelfSignedCertificate`. Supports:
- **Self-signed** — for testing
- **Root CA** — certification authority
- **Signed by CA** — requires existing Root CA files

Configurable: key algorithm (RSA / EC), key size, hash algorithm, validity period, Subject fields (CN, O, C, L, ST, email), SAN (DNS + IP), PFX export, and Windows store installation.

### Options
Language switcher (Polski / English) and tool path configuration.

---

## Auto-Detection of Tools

At startup, SignTool's-ITS GUI searches all available drives for `signtool.exe` and `openssl.exe`. A summary dialog reports:

- ✅ Found — path displayed
- ⚠️ Not found — option to locate manually

---

## Architecture Notes

- **Single-file application** — all logic in `main.py` (~5 500 lines)
- **Built-in translation system** — `_TR` dictionary with `pl`/`en` keys; no external i18n library needed
- **UTF-8 enforcement** — stdout/stderr reconfigured on startup; `CREATE_NO_WINDOW` flag applied globally to all subprocess calls on Windows to prevent console flash
- **Threading** — all subprocess calls run in daemon threads; output is streamed line-by-line to the GUI text widget with color-coded tags (success / error / command / info)
- **Embedded assets** — icons and images stored as Base64 strings

---

## Author & License

| Field | Value |
|---|---|
| **Author** | Sebastian Januchowski |
| **Company** | polsoft.ITS™ Group |
| **Contact** | polsoft.its@fastservice.com |
| **GitHub** | https://github.com/seb07uk |
| **Copyright** | 2026© polsoft.ITS™. All rights reserved. |
| **License** | Proprietary |

---

> © 2026 polsoft.ITS™ Group. All rights reserved. Unauthorized distribution prohibited.
