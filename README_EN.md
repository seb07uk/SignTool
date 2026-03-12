<div align="center">

<img src="readme_assets/icon_polsoft.png" width="64" alt="polsoft.ITS Logo"/>

# 🔏 SignTool Suite — Code Signing Tools

**Professional GUI for signtool.exe and OpenSSL | polsoft.ITS™ Group**

*By: Sebastian Januchowski*

---

</div>

A set of three Windows desktop applications that turn complex command-line operations into a clear, intuitive graphical interface. Each tool addresses different needs — from quick signature testing, through daily certificate work, to a full production environment with OpenSSL support and a built-in certificate generator.

---

## 1. PublicTester QuickDigital Signature GUI `v1.1.0`

<img src="readme_assets/icon_publictester.png" width="36" align="left" style="margin-right:12px"/>

**Lightweight tool for quick digital signature verification**

<br clear="left"/>

Designed for testers and developers who want to sign a file in seconds and verify that the entire chain works correctly — with zero configuration. The application automatically detects `signtool.exe` (Windows SDK) and `.pfx` certificates in nearby folders.

<div align="center">
<img src="readme_assets/PublicTester_QuickDigitalSignature_GUI_v1_1.png" width="420" alt="PublicTester GUI Screenshot"/>
</div>

### ✅ Key Features

| Feature | Description |
|---|---|
| 🔍 Auto-detection | Automatically locates `signtool.exe` and `.pfx` certificates |
| ⚡ One click | Sign any file with a single **Sign File** button |
| 🔄 Timestamp fallback | Automatic retry with a backup timestamp server |
| 🧵 Background thread | Signing never freezes the UI |
| 📋 File logging | Detailed log files for diagnostics |

**Who is it for?** QA testers, developers verifying CI/CD pipelines, and anyone taking their first steps with code signing.

---

## 2. Quick DigitalSignature GUI `v1.9`

<img src="readme_assets/icon_quickds.png" width="36" align="left" style="margin-right:12px"/>

**Complete tool for everyday file signing**

<br clear="left"/>

An expanded tool with a full set of operations: signing, verification with Policy Authority and timestamp server, and CA certificate installation. Supports light and dark mode, password saving via DPAPI, and files can be dragged directly into the window.

<div align="center">
<img src="readme_assets/Quick_DigitalSignature_v1_9_GUI.png" width="440" alt="Quick DigitalSignature GUI Screenshot"/>
</div>

### ✅ Key Features

| Feature | Description |
|---|---|
| 🖱️ Drag & Drop | Drag a file directly into the application window |
| 🔐 Secure password | PFX password encryption via Windows DPAPI |
| ✔️ Verify PA / PA+TS | Signature verification with Policy Authority and Timestamp |
| 🏛️ CA Installation | Install Root CA / Intermediate CA in one click |
| 🌗 Dark mode | Full light and dark theme support |
| 💾 Session save | Remembers last used files and certificate |

**Who is it for?** Developers and release engineers who regularly sign multiple files and need full control over the process.

---

## 3. SignTool's-ITS GUI `v2.0`

<img src="readme_assets/icon_signtools.png" width="36" align="left" style="margin-right:12px"/>

**Professional production environment — Microsoft signtool + OpenSSL**

<br clear="left"/>

The most advanced tool in the suite. It combines `signtool.exe` (Microsoft) with `openssl` in a single, multi-tab interface with full Polish and English language support. It enables not only signing and verification, but also generating your own certificates and batch processing.

<div align="center">
<img src="readme_assets/SignTools-ITS_v2.png" width="600" alt="SignTools-ITS GUI v2.0 Screenshot"/>
</div>

### ✅ Key Features

| Feature | Description |
|---|---|
| 📑 5 tabs | Sign, Timestamp/Verify, CatDB/Remove, Batch, Generate Certificate |
| 🔑 Certificate generator | Create self-signed certificates via OpenSSL |
| 📦 Batch mode | Sign multiple files at once |
| 🌍 PL / EN | Built-in Polish and English language support |
| 🔎 Tool auto-detection | Scans drives for `signtool.exe` and `openssl.exe` |
| 🛡️ SHA256 / RFC3161 | Modern signing algorithms and timestamps |
| 📋 Command preview | **Show command** button before execution |
| 🗃️ CatDB | Windows certificate catalog (.cat) management |
| ⚙️ Cross-certification | Additional certificate `/ac` support |

**Who is it for?** Software companies, release managers, and PKI administrators — everyone who needs a complete code-signing environment in one place.

---

## 📦 Feature Comparison

| | PublicTester v1.1.0 | Quick DS v1.9 | SignTools-ITS v2.0 |
|---|:---:|:---:|:---:|
| File signing | ✅ | ✅ | ✅ |
| Signature verification | — | ✅ | ✅ |
| Drag & Drop | — | ✅ | — |
| Dark mode | — | ✅ | — |
| Certificate generation | — | — | ✅ |
| Batch processing | — | — | ✅ |
| OpenSSL support | — | — | ✅ |
| PL/EN language | — | — | ✅ |
| Difficulty level | 🟢 Beginner | 🟡 Intermediate | 🔴 Advanced |

---

<div align="center">

**polsoft.ITS™ Group** • polsoft.its@fastservice.com • [github.com/seb07uk](https://github.com/seb07uk)

*Copyright © 2026 polsoft.ITS™. All rights reserved.*

<img src="readme_assets/icon_polsoft.png" width="32" alt="polsoft.ITS"/>

</div>
