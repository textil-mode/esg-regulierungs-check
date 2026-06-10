@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv" (
    echo [Setup] Erstelle virtuelle Umgebung...
    python -m venv .venv
    if errorlevel 1 goto :error
    call ".venv\Scripts\activate.bat"
    echo [Setup] Installiere Abhaengigkeiten...
    pip install -r requirements.txt
    if errorlevel 1 goto :error
) else (
    call ".venv\Scripts\activate.bat"
    REM Stelle sicher, dass neue Deps drin sind (schnell wenn schon installiert)
    pip install -q -r requirements.txt
)

if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo.
    echo [!] .env wurde angelegt. Bitte Provider-Konfig eintragen und erneut starten.
    notepad .env
    goto :eof
)

echo [Start] Starte Flask-App auf http://localhost:5000 ...
python app.py
goto :eof

:error
echo.
echo [Fehler] Setup fehlgeschlagen. Pruefe, ob Python 3.10+ installiert ist.
pause
