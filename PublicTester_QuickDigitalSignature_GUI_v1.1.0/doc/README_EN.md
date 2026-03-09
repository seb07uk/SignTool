# PublicTester QuickDigital Signature GUI

<p align="center">
  <img src="https://img.shields.io/badge/version-1.1.0-blue?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows-0078D4?style=flat-square&logo=windows" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

> A lightweight graphical user interface (GUI) for digitally signing files using **SignTool.exe** from the Windows SDK. Sign `.exe`, `.dll`, `.msi`, and other file types with a `.pfx` certificate in just a few clicks.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Screenshots](#-screenshots)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [FAQ](#-faq)
- [Authors](#-authors)
- [License](#-license)

---

## 📖 Overview

**PublicTester QuickDigital Signature GUI** is a lightweight Python/Tkinter desktop application that wraps Microsoft's `signtool.exe` in a clean, intuitive interface.

Key features:

- 🔍 **Auto-detection of `signtool.exe`** — searches the program directory, PyInstaller bundle, and all standard Windows SDK paths (8.0, 8.1, 10, 11) across x64, x86, and arm64 architectures.
- 📂 **Auto-discovery of `.pfx` certificates** — scans the program directory, a `certs/` subfolder, user profile, `%APPDATA%`, and other standard Windows locations.
- 🔐 **PFX password support** — optional password field for password-protected certificates.
- 🕐 **RFC 3161 timestamping** — automatically applied via `timestamp.digicert.com` using SHA-256.
- 🖥️ **Microsoft Fluent-inspired UI** — blue header (`#0078D4`), clean layout, and clear status messages.
- 📦 **PyInstaller-ready** — works both as a `.py` script and as a bundled standalone `.exe`.

---

## 🖼️ Screenshots

<p align="center">
  <img src="Screenshot.png" alt="PublicTester QuickDigital Signature GUI — screenshot" width="420">
</p>

---

## ✅ Requirements

| Dependency | Minimum Version | Notes |
|------------|----------------|-------|
| Python | 3.10+ | Required for `X \| Y` union type syntax |
| Pillow | 9.0+ | `pip install Pillow` |
| tkinter | built-in | Included with standard Python |
| signtool.exe | any | From Windows SDK or placed next to the app |
| Windows | 10 / 11 | Windows-only application |

> **Note:** This application runs on **Windows only**. `signtool.exe` is not available on Linux or macOS.

---

## 🚀 Installation

### Option 1 — Run from source

```bash
# 1. Clone the repository
git clone https://github.com/YourOrganization/quickdigital-signature-gui.git
cd quickdigital-signature-gui

# 2. Install dependencies
pip install Pillow

# 3. Launch the application
python main.py
```

### Option 2 — Build a standalone EXE (PyInstaller)

```bash
pip install pyinstaller

pyinstaller --onefile --windowed --icon=app_icon.ico ^
  --add-data "app_icon.ico;." ^
  --add-data "certs;certs" ^
  main.py
```

The compiled `.exe` will be placed in the `dist/` folder.

### Option 3 — Download a pre-built EXE

Download the latest release from the [Releases](../../releases) page and run `QuickDigitalSignature.exe` directly — no Python installation required.

---

## 🖱️ Usage

1. **Launch the application** (`python main.py` or `QuickDigitalSignature.exe`).
2. **Certificate** — the app automatically discovers `.pfx` files in the program directory and `certs/` subfolder. Click **Browse...** to point to a custom folder.
3. **PFX Password** — enter the certificate password if protected, or leave blank.
4. **File to sign** — click **Browse...** and select the target file (`.exe`, `.dll`, `.msi`, `.cab`, etc.).
5. **Sign** — click **Sign File**. A dialog will report success or display the error output from SignTool.

### Certificate search order

| Priority | Location |
|----------|----------|
| 1 | PyInstaller internal bundle (`_MEIPASS`) |
| 2 | Program directory (next to the `.exe`) |
| 3 | `<program directory>\certs\` |
| 4 | `%USERPROFILE%\.certificates\` |
| 5 | `%USERPROFILE%\certificates\` |
| 6 | User Desktop |
| 7 | `%APPDATA%\certificates\` |
| 8 | Public Desktop (`%PUBLIC%\Desktop`) |
| 9 | Custom folder provided by the user |

---

## 📁 Project Structure

```
quickdigital-signature-gui/
├── main.py              # Main application file
├── app_icon.ico         # Application icon (optional)
├── certs/               # Optional folder for .pfx certificates
│   └── *.pfx
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── dist/                # Compiled .exe (after running PyInstaller)
```

---

## ⚙️ Configuration

Configuration constants at the top of `main.py`:

```python
APP_NAME    = "PublicTester QuickDigital Signature GUI"
APP_VERSION = "1.1.0"
APP_AUTHOR  = "PublicTester QuickDigital Signature"

MINIMAL_GUI = True   # True = hides advanced UI sections
```

Setting `MINIMAL_GUI = False` reveals additional interface elements (certificate section, SignTool status bar, certificate directory selector).

**Default timestamp server:**
```
http://timestamp.digicert.com
```
To use a different server, edit the `/tr` argument in the `uruchom_signtool()` function.

---

## ❓ FAQ

**Q: I get "SignTool.exe not found".**  
A: Install the [Windows SDK](https://developer.microsoft.com/windows/downloads/windows-sdk/) or place `signtool.exe` in the same directory as `main.py` / the `.exe`.

**Q: "No .pfx certificates found" warning.**  
A: Place your `.pfx` file next to the application or in a `certs/` subfolder. Alternatively, click **Browse...** to select the directory manually.

**Q: Does the app work on Windows 7 / 8?**  
A: Windows 10 and 11 are officially supported. Older versions may work but are not tested.

**Q: Can I sign multiple files at once?**  
A: The current version handles one file at a time. Batch signing support is planned for v1.2.0.

---

## 👤 Authors

| Author | Role |
|--------|------|
| **Sebastian Januchowski** | Creator & Lead Developer |

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

```
MIT License

Copyright (c) 2024 Sebastian Januchowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software...
```

---

<p align="center">
  Made with ❤️ by <strong>Sebastian Januchowski</strong> · PublicTester QuickDigital Signature
</p>
