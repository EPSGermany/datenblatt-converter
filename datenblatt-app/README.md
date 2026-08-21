# Datenblatt-Converter

Eigenständiges Windows-Programm mit 4 Buttons. Läuft komplett lokal ohne
Internet-/Serverzugriff **und ohne dass Microsoft Word oder LibreOffice
installiert sein muss** - das PDF wird direkt erzeugt (reportlab, reines
Python, in der exe enthalten). Wandelt ein fremdes PDF-Datenblatt
**vollautomatisch** in euer eigenes EPS-Design um, wahlweise als
deutsches oder englisches PDF.

## Bedienung
1. **1. Datenblatt importieren** - fremde PDF auswählen. Erkennt
   automatisch Titel, Serie/Series, Beschreibung sowie alle technischen
   Werte - anhand von Schriftgröße und Textposition, ganz ohne KI. Jeder
   übernommene Wert ist eine wörtliche Kopie aus der PDF.
2. **2. Datenblatt anzeigen** - Kontrollbericht (alle erkannten Werte)
   plus Textvorschau. Ist ein KI-API-Key hinterlegt (siehe unten), läuft
   hier zusätzlich eine KI-Prüfung mit.
3. **3. Export Deutsch** / **4. Export Englisch** - speichert das
   fertige Datenblatt in der gewählten Sprache direkt als PDF.

## Warum kein Word/LibreOffice mehr nötig ist
Frühere Version: Word-Vorlage (.docx) ausfüllen → in PDF umwandeln
(brauchte installiertes Word oder LibreOffice auf JEDEM PC, auf dem das
Programm läuft - unpraktisch bei vielen Firmen-/Homeoffice-Rechnern).

Jetzt: Das PDF wird direkt mit der Python-Bibliothek `reportlab`
gezeichnet (`pdf_export.py`) - keine externe Software nötig, läuft überall
identisch. **Trade-off:** Design-Anpassungen (Farben, Schriftgrößen,
Layout) erfolgen jetzt im Code (`pdf_export.py`), nicht mehr per
Word-Bearbeitung einer Vorlage.

`vorlage.docx`/`vorlage_en.docx` und die docx-Erzeugungsfunktionen in
`lib.py` (`build_draft`, `convert_to_pdf`) sind weiterhin im Projekt
vorhanden, falls ihr mal eine editierbare Word-Version braucht - werden
vom Programm selbst aber nicht mehr verwendet.

## Kategorien (Allgemeine Daten/Schnittstellen/Technische Daten)
Fest vorgegebene Kategorienlisten, keine automatische Erkennung der
Zeilennamen:
- Deutsch: `kategorien.py` - Allgemeine Daten (42), Schnittstellen (11),
  Technische Daten (16)
- Englisch: `kategorien_en.py` - General data (44), Interfaces (11),
  Technical data (19)

Beim Import wird für jede feste Kategorie im Quell-PDF nach einem Label
mit (fast) demselben Text gesucht - Treffer wird wörtlich übernommen,
sonst bleibt die Zeile leer/markiert. Listen bei Bedarf ergänzen (z.B. um
eine neue Kategorie aus einem weiteren Produkt) - wirkt sofort beim
nächsten Import, kein Neubau nötig.

**"Optionen"/"Options" und "Lieferumfang"/"Scope of delivery" bleiben
dynamisch** (Zeilenanzahl passt sich automatisch an die Anzahl im
Quell-PDF an).

## Design anpassen
Layout, Farben, Schriftgrößen stehen in `pdf_export.py`
(`_styles()`-Funktion für Schriften, `SHADE_COLOR` für die
Tabellen-Streifenfarbe, `build_pdf_native()` für die Reihenfolge der
Abschnitte). Firmendaten/Fußzeilentexte stehen in `app.py` in `LANG_DE`
und `LANG_EN` (`fuss1_text`, `fuss2_text`, `kopf_text` usw.).

## Optionale KI-Kontrolle (Internetzugriff)
Über den Button **"⚙ KI-Einstellungen"** kannst du einen eigenen
Anthropic-API-Key hinterlegen (lokal in `config.json`, wird nie
mitgeliefert oder fest im Code hinterlegt). Ist ein Key hinterlegt, prüft
"2. Datenblatt anzeigen" den Entwurf zusätzlich per KI-Aufruf gegen die
Rohdaten und zeigt Auffälligkeiten an - **die KI erzeugt dabei selbst
keine Werte**, sie vergleicht nur und meldet Unstimmigkeiten.

Ohne API-Key läuft alles komplett lokal/offline.

Wichtig zu wissen, bevor du einen Key einträgst:
- Internetzugriff nötig (Aufruf von `api.anthropic.com`)
- Der Inhalt des Entwurfs wird an die Anthropic-API geschickt
- Pro Prüfung fallen API-Kosten an (siehe https://docs.claude.com/en/api/overview)
- Der Key liegt nur lokal in `config.json` - nicht weitergeben, nicht in git einchecken
- Eigenen API-Key: https://console.anthropic.com

## Installation als .exe (einmalig, über GitHub Actions)
Siehe `GITHUB_ACTIONS_SETUP.md` für die Schritt-für-Schritt-Anleitung.
Kurzfassung: Workflow läuft automatisch bei jedem Push, baut die exe auf
einem Windows-Server (inkl. tkinter, ohne dass du selbst Python lokal
brauchst), lädt die fertige `Datenblatt-Converter.exe` als Artifact zum
Download bereit - **eine einzelne Datei, keine weiteren Dateien nötig**
(Banner-Bilder sind mit eingebündelt).

## Grenzen (bewusst, gegen Fehler/Halluzination)
- Funktioniert am zuverlässigsten bei Datenblättern mit klar getrennten
  Label/Wert-Spalten oder "Label: Wert"-Zeilen.
- Reine Bild-Scans (kein eingebetteter PDF-Text) werden nicht erkannt -
  bewusst kein OCR.
- Bei völlig anderen Layouts (z.B. mehrspaltige Fließtext-Datenblätter
  fremder Hersteller) kann die automatische Erkennung Lücken haben -
  über "Datenblatt anzeigen" vor dem Export prüfbar. Alle Werte bleiben
  aber immer wörtliche Kopien aus dem Quell-PDF.

## Dateien
```
app.py              GUI (4 Buttons + Einstellungen), Sprachkonfiguration
lib.py               PDF-Extraktion, Zuordnungslogik, (optional) docx-Erzeugung
pdf_export.py         direkte PDF-Erzeugung (reportlab) - kein Word/LibreOffice
kategorien.py          feste dt. Kategorienlisten
kategorien_en.py        feste engl. Kategorienlisten
ai_check.py             optionale KI-Zusatzkontrolle
config.py               lädt/speichert config.json (API-Key, lokal)
assets/                  Banner-Bilder (DE + EN), in die exe gebündelt
vorlage.docx/vorlage_en.docx   optional, nicht mehr im Hauptablauf verwendet
build_template.py        erzeugt vorlage*.docx neu (optional)
requirements.txt
.github/workflows/build-exe.yml   Cloud-Build ohne lokales Python
```
