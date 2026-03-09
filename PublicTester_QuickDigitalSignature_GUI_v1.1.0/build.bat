@echo off
setlocal
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"
if not exist "app_icon.ico" exit /b 1
where pyinstaller >nul 2>&1 || (
  py -m pip install --upgrade pip
  py -m pip install pyinstaller pillow
)
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
pyinstaller PublicTester_QuickDigitalSignature.spec --noconfirm
if errorlevel 1 exit /b %errorlevel%
echo dist\PublicTester_QuickDigitalSignature.exe
endlocal
