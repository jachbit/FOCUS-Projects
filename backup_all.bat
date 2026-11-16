@echo off
title F.O.C.U.S. Projects - backup
rem Timestamped copies of the project files into backups\ (run before every edit session).
cd /d "%~dp0"
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set TS=%%i
if not exist backups mkdir backups
copy "index.html"            "backups\index_%TS%.html" >nul && echo   [OK] index.html
copy "projects.json"         "backups\projects_%TS%.json" >nul && echo   [OK] projects.json
copy "build_projects_pdf.py" "backups\build_projects_pdf_%TS%.py" >nul && echo   [OK] build_projects_pdf.py
copy "README.md"             "backups\README_%TS%.md" >nul && echo   [OK] README.md
copy "start.bat"             "backups\start_%TS%.bat" >nul && echo   [OK] start.bat
copy "make_pdf.bat"          "backups\make_pdf_%TS%.bat" >nul && echo   [OK] make_pdf.bat
copy ".github\workflows\pdf.yml" "backups\pdf_%TS%.yml" >nul && echo   [OK] pdf.yml
echo.
echo Backup done: backups\*_%TS%.*
