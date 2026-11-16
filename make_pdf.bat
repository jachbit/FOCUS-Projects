@echo off
title F.O.C.U.S. Projects - PDF
rem Builds FOCUS_Projects_GitHub_YYYYMMDD_HHMMSS.pdf in this folder (template layout, clickable links) and opens it.
cd /d "%~dp0"
python build_projects_pdf.py
for /f "delims=" %%f in ('dir /b /o-d FOCUS_Projects_GitHub_*.pdf') do (start "" "%%f" & goto :done)
:done
