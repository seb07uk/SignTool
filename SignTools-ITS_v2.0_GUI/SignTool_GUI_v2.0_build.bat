@echo off
setlocal EnableDelayedExpansion

::  SignTool GUI v2.0 - Build Script
::  polsoft.ITS Group  |  2026 polsoft.ITS. All rights reserved.
::  Project Manager: Sebastian Januchowski
::  polsoft.its@fastservice.com  |  https://github.com/seb07uk

title SignTool GUI v2.0 - Build

echo.
echo  ================================================
echo   PolSoft.ITS Group - SignTool GUI v2.0 - Build
echo   2026(c) polsoft.ITS. All rights reserved.
echo  ================================================
echo.

:: [1/6] Python
echo [1/6] Sprawdzanie Python...
where python >nul 2>&1
if errorlevel 1 (
    echo  [BLAD] Python nie znaleziony w PATH!
    echo  Pobierz z: https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=*" %%V in ('python --version 2^>^&1') do echo  Znaleziono: %%V

:: [2/6] PyInstaller
echo [2/6] Sprawdzanie PyInstaller...
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo  PyInstaller nie znaleziony - instalowanie...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo  [BLAD] Instalacja PyInstaller nieudana!
        pause
        exit /b 1
    )
)
for /f "tokens=*" %%V in ('python -m PyInstaller --version 2^>^&1') do echo  PyInstaller: %%V

:: [3/6] Wymagane pliki
echo [3/6] Sprawdzanie plikow...
set MISSING=0
for %%F in (main.py SignTool-ico.ico hook_utf8.py SignTool.spec version_info.txt SignTool.manifest) do (
    if not exist "%%F" (
        echo  [BRAK] %%F
        set MISSING=1
    ) else (
        echo  [OK]   %%F
    )
)
if !MISSING!==1 (
    echo.
    echo  [BLAD] Brakujace pliki - przerwano!
    pause
    exit /b 1
)

:: [4/6] Czyszczenie
echo [4/6] Czyszczenie...
if exist dist  rmdir /s /q dist
if exist build rmdir /s /q build
echo  Gotowe.

:: [5/6] Kompilacja
echo [5/6] Kompilacja...
echo.
python -m PyInstaller SignTool.spec --clean --noconfirm
echo.

if errorlevel 1 (
    echo  [BLAD] Kompilacja nieudana!
    echo  - Dodaj wyjatek AV dla tego folderu
    echo  - Sprawdz bledy powyzej
    pause
    exit /b 1
)

:: [6/6] Sprzatanie
echo [6/6] Sprzatanie po kompilacji...

if exist build (
    rmdir /s /q build
    echo  Usunieto: build\
)

if exist "dist\SignTool\_internal" (
    rmdir /s /q "dist\SignTool\_internal"
    echo  Usunieto: dist\SignTool\_internal\
)

if exist "dist\SignTool\SignTool.exe" (
    move /Y "dist\SignTool\SignTool.exe" "dist\SignTool.exe" >nul
    rmdir /s /q "dist\SignTool" >nul 2>&1
    echo  Przeniesiono EXE do dist\
)

:: Weryfikacja
if not exist "dist\SignTool.exe" (
    echo.
    echo  [BLAD] dist\SignTool.exe nie znaleziony!
    dir dist\ 2>nul
    pause
    exit /b 1
)

for %%A in ("dist\SignTool.exe") do set BYTES=%%~zA
set /a MB=!BYTES! / 1048576

echo.
echo  ================================================
echo   BUILD UKONCZONY POMYSLNIE
echo.
echo   Plik   : dist\SignTool.exe
echo   Rozmiar: !MB! MB
echo.
echo   Wlasciwosci EXE (PPM > Szczegoly):
echo    Firma  : polsoft.ITS Group
echo    Wersja : 2.0.0.0
echo  ================================================
echo.

start "" "dist"
pause
endlocal
