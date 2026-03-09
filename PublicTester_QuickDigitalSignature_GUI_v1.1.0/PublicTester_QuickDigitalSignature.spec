# -*- mode: python ; coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════════
#  PublicTester QuickDigital Signature — PyInstaller SPEC
#  Author  : Sebastian Januchowski
#  Company : polsoft.ITS™ Group
#  Contact : polsoft.its@fastservice.com
#  GitHub  : https://github.com/seb07uk
#  2026© polsoft.ITS™. All rights reserved.
#
#  Kompilacja:
#    pip install pyinstaller pillow
#    pyinstaller PublicTester_QuickDigitalSignature.spec --noconfirm
#
#  EXE -> dist\PublicTester_QuickDigitalSignature.exe
# ══════════════════════════════════════════════════════════════════

import os
import glob
block_cipher = None

bin_files = []
for f in ['SignTool.exe']:
    if os.path.isfile(f):
        bin_files.append((f, '.'))

data_files = []
# include all .pfx from root
for f in glob.glob('*.pfx'):
    data_files.append((f, '.'))
# include all .pfx from certs/ subdir
for f in glob.glob(os.path.join('certs', '*.pfx')):
    data_files.append((f, 'certs'))
# include icon
if os.path.isfile('app_icon.ico'):
    data_files.append(('app_icon.ico', '.'))

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=bin_files,
    datas=data_files,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'scipy', 'pandas', 'PyQt5', 'wx'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

icon_path = 'app_icon.ico' if os.path.isfile('app_icon.ico') else None

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PublicTester_QuickDigitalSignature',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,           # GUI only — brak okna cmd
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
    version='version_info.txt',  # version info (Properties → Details)
)
