@echo off
setlocal enabledelayedexpansion

set /p "url=Enter URL: "

call ../venv/Scripts/activate.bat

python ..\test\testShortcut.py

endlocal