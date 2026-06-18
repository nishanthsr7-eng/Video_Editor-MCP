@echo off
:: Onepiece Audio-1 — DaVinci Resolve Import Script Launcher
:: Wires the correct paths for a non-default DaVinci install at D:\DaVinci
:: Run AFTER enabling: Preferences > System > General > Enable local scripting API

set RESOLVE_SCRIPT_API=C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting
set RESOLVE_SCRIPT_LIB=D:\DaVinci\fusionscript.dll
set PYTHONPATH=C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules
set PATH=D:\DaVinci;%PATH%

echo.
echo  Onepiece Audio-1 — DaVinci Resolve Import Script
echo  -------------------------------------------------
echo  Connecting to Resolve...
echo.

python "%~dp0Output\Onepiece_analysis_clips\Onepiece_Audio1_Import.py"

echo.
pause
