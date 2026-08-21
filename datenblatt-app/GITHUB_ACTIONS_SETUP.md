# EXE über GitHub Actions bauen (ohne eigenes Python)

Der Workflow `.github/workflows/build-exe.yml` baut die exe automatisch
in der Cloud auf einem Windows-Server mit vollständigem Python
(inklusive tkinter) - du brauchst dafür selbst kein Python installieren.

## Einmaliges Setup

1. **GitHub-Account anlegen** (falls noch nicht vorhanden): https://github.com/signup
   (kostenlos, reicht für dieses Vorhaben völlig aus).

2. **Neues Repository anlegen:**
   - Auf https://github.com/new gehen
   - Name z.B. `datenblatt-converter`
   - **Private** auswählen (deine Vorlage/Firmendaten sollen nicht
     öffentlich einsehbar sein)
   - "Create repository" klicken

3. **Diesen Ordner hochladen** - am einfachsten über den Browser, kein
   Git-Kommandozeilen-Wissen nötig:
   - Auf der neuen Repo-Seite auf **"uploading an existing file"** klicken
   - Alle Dateien/Ordner aus diesem `datenblatt-app`-Ordner per Drag&Drop
     hineinziehen (inklusive des unsichtbaren `.github`-Ordners - falls
     dein Dateimanager versteckte Ordner ausblendet, in den
     Ordnereinstellungen "versteckte Dateien anzeigen" aktivieren)
   - Unten auf "Commit changes" klicken

   *(Alternative für später, wenn du Änderungen an `vorlage.docx`
   hochladen willst: einfach die Datei im Repo im Browser öffnen und über
   den Stift/"Edit"-Button bzw. "Upload files" ersetzen - jeder Upload
   löst automatisch einen neuen Build aus.)*

4. **Build abwarten:**
   - Oben im Repo auf den Reiter **"Actions"** klicken
   - Der Workflow "Build Datenblatt-Converter.exe" startet automatisch
     (dauert ca. 2-4 Minuten)
   - Ist er fertig (grüner Haken), auf den Lauf klicken

5. **EXE herunterladen:**
   - Unten auf der Laufseite unter **"Artifacts"** auf
     "Datenblatt-Converter" klicken - lädt eine .zip mit
     `Datenblatt-Converter.exe` und `vorlage.docx` herunter
   - Entpacken, beide Dateien gemeinsam an den gewünschten Ort
     verschieben (z.B. Desktop)

## Danach: neue Version bauen

Jedes Mal, wenn du `app.py`, `lib.py` oder `vorlage.docx` im Repo
aktualisierst (Upload im Browser reicht), baut GitHub automatisch eine
neue exe. Alternativ jederzeit manuell: Actions-Tab -> "Build
Datenblatt-Converter.exe" -> "Run workflow".

## Kosten
Private Repos bekommen im GitHub-Free-Plan 2.000 Freiminuten/Monat für
GitHub-gehostete Runner (Stand August 2026, siehe
https://docs.github.com/en/actions/concepts/billing-and-usage). Wichtig:
Windows-Runner (die wir hier nutzen) zählen mit **doppeltem** Verbrauch
gegen dieses Kontingent, effektiv also ca. 1.000 Windows-Minuten/Monat
frei. Ein Build dauert ca. 2-4 Minuten (= 4-8 Minuten Verbrauch) - das
reicht für gut 100+ Builds im Monat, für gelegentliches Neubauen der exe
also mehr als ausreichend.
