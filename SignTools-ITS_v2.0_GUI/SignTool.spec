# -*- mode: python ; coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────────────
#  SignTool GUI – PyInstaller build spec  (ONE-FILE / single portable EXE)
#  Project Manager : Sebastian Januchowski
#  Firma           : polsoft.ITS™ Group
#  Kontakt         : polsoft.its@fastservice.com
#  GitHub          : https://github.com/seb07uk
#  Copyright       : 2026© polsoft.ITS™. All rights reserved.
#
#  NAPRAWA MIGANIA KONSOLI:
#  Przyczyna: runtime_tmpdir='.' powoduje ze bootloader startuje chwilowo
#             jako proces konsolowy zanim przelacza na GUI subsystem.
#  Rozwiazanie:
#    1. runtime_tmpdir=None  – standardowy %TEMP% (brak console-switch)
#    2. windowed=True        – jawne wymuszenie podsystemu Windows
#    3. manifest XML         – utrwala subsystem windows od pierwszego bajtu
#    4. console=False        – bez okna konsoli
# ──────────────────────────────────────────────────────────────────────────────

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('SignTool-ico.ico', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'json',
        'threading',
        'subprocess',
        'pathlib',
        'tempfile',
        'base64',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['hook_utf8.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SignTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    # None = standardowy %TEMP% – NIE powoduje przejscia console->GUI
    # runtime_tmpdir='.' bylo przyczyna migania konsoli!
    runtime_tmpdir=None,
    console=False,       # brak okna konsoli
    windowed=True,       # jawne wymuszenie GUI subsystem od startu
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='SignTool-ico.ico',
    version='version_info.txt',
    # Manifest wymusza subsystem WINDOWS i DPI awareness
    manifest='SignTool.manifest',
)
