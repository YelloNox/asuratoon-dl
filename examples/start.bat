@echo off
setlocal enabledelayedexpansion

set /p "url=Enter URL: "

call "../venv/Scripts/activate.bat"

python "../asuratoon_dl.py" --path ../downloads/Asuratoon --cbz --link !url!

endlocal