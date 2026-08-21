@echo off
REM Erzeugt Datenblatt-Converter.exe. Einmalig auf einem Windows-PC mit
REM installiertem Python ausfuehren (im Ordner mit app.py, lib.py, vorlage.docx).

echo === Abhaengigkeiten installieren ===
pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo === EXE bauen ===
pyinstaller --noconfirm --onefile --windowed ^
    --name "Datenblatt-Converter" ^
    app.py
if errorlevel 1 goto :error

echo.
echo === Fertig ===
echo Kopiere jetzt aus diesem Ordner sowohl
echo   dist\Datenblatt-Converter.exe
echo als auch
echo   vorlage.docx
echo gemeinsam in einen neuen Zielordner (z.B. Desktop). Die exe liest
echo vorlage.docx aus ihrem eigenen Ordner - beide Dateien muessen also
echo immer nebeneinander liegen. Passt du die Vorlage in Word an, reicht
echo das direkte Bearbeiten von vorlage.docx - kein Neubauen der exe noetig.
pause
goto :eof

:error
echo Fehler beim Bauen - siehe Meldung oben.
pause
