# Projekt: Datenblatt-Converter (GUI-Programm)

## Zweck
Fremde technische Datenblätter (PDF) werden automatisch in das eigene
EPS-Firmen-Design übertragen und wahlweise als deutsches oder englisches
PDF exportiert. Bedienung über 4 Buttons in `app.py` (Tkinter-GUI):
importieren (erzeugt automatisch beide Sprachentwürfe), anzeigen/
kontrollieren, Export Deutsch, Export Englisch. Kein Server-/
Internetzugriff nötig (außer optionaler KI-Zusatzkontrolle, siehe
`ai_check.py`). Build als Windows-.exe über GitHub Actions
(`.github/workflows/build-exe.yml`).

## Dateien
```
app.py                 GUI (4 Buttons + Einstellungen)
lib.py                  Kernlogik: PDF-Extraktion, Vorlage befüllen, PDF-Export
kategorien.py            feste dt. Kategorienlisten (Allgemeine Daten/
                         Schnittstellen/Technische Daten)
kategorien_en.py         feste engl. Kategorienlisten (General data/
                         Interfaces/Technical data)
ai_check.py              optionale KI-Zusatzkontrolle (nur mit eigenem API-Key)
config.py                lädt/speichert config.json (API-Key etc., lokal)
vorlage.docx              deutsche Design-Vorlage (Banner, 3 feste
                         Kategorien-Tabellen + Optionen/Lieferumfang, Fußzeile)
vorlage_en.docx           englisches Gegenstück (eigenes Banner, engl.
                         Kategorien/Fußzeilentext)
build_template.py         erzeugt BEIDE Vorlagen neu aus kategorien*.py +
                         assets/banner*.jpg
assets/                   Banner/Logo-Bilder (DE + EN) für die Vorlagen
beispiel-pdfs/             deutsche Beispiel-Datenblätter (Ziel-Layout DE)
test-pdfs/                 Test-Datenblätter Deutsch (+ fremde/schwierige
                         Layouts, z.B. Absopulse SCD) für den Struktur-Loop
test-pdfs-en/               Test-Datenblätter Englisch
spec/struktur-checkliste.md     feste Prüfkriterien für erzeugte Entwürfe
.claude/commands/struktur-loop.md     iterativer Test-/Fix-Loop (Slash-Command)
```

## Feste Regeln (nicht verhandelbar)

1. **Keine Erfindung von Inhalten.** Jeder Wert im erzeugten Dokument
   muss wörtlich aus dem Quell-PDF stammen. Fehlt ein Wert eindeutig,
   bleibt das Feld leer/markiert - niemals schätzen, übersetzen oder
   umformulieren (auch nicht zwischen Deutsch und Englisch - die
   Kategorie-Zuordnung erfolgt rein über Textabgleich, es wird nie
   automatisch übersetzt).
2. **Erkennung ist rein positions-/formatbasiert** (Schriftgröße,
   Wortposition, Zeilenabstände), keine KI-Textgenerierung in `lib.py`.
   Die einzige KI-Komponente ist die optionale, rein prüfende
   Zusatzkontrolle in `ai_check.py` (erzeugt selbst keine Werte).
3. **Docx-Mechanik läuft über python-docx-Funktionen in `lib.py`**, nie
   durch direktes Bearbeiten der Docx-XML per Hand.
4. **Neue Erkennungslogik muss gegen ALLE Dateien in `test-pdfs/` UND
   `test-pdfs-en/` getestet werden**, nicht nur gegen die Datei, die
   gerade ein Problem zeigt - eine Änderung darf bestehende, bereits
   funktionierende Fälle (in keiner der beiden Sprachen) nicht kaputt
   machen.
5. **Kategorienlisten (`kategorien.py`/`kategorien_en.py`) und
   Vorlagen (`vorlage.docx`/`vorlage_en.docx`) werden nicht automatisch
   überschrieben.** Änderungen daran nur nach expliziter Absprache, da
   sie das persönliche, personalisierte Firmenlayout des Nutzers
   enthalten. `build_template.py` überschreibt bei Ausführung IMMER
   beide Vorlagen - vorher sichern, falls von Hand angepasst.

## Entwicklungs-Loop
Für iterative Verbesserungen der Erkennung: `/struktur-loop` ausführen
(siehe `.claude/commands/struktur-loop.md`). Der Loop erzeugt Entwürfe für
alle `test-pdfs/` (und sollte auf `test-pdfs-en/` erweitert werden, falls
noch nicht geschehen), prüft sie gegen `spec/struktur-checkliste.md`,
behebt gefundene Probleme in `lib.py`, und wiederholt das bis alles passt
oder die Rundenzahl aufgebraucht ist.

