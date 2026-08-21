# Datenblatt-Converter

Eigenständiges Windows-Programm mit 4 Buttons. Läuft standardmäßig
komplett lokal ohne Internet-/Serverzugriff. Wandelt ein fremdes
PDF-Datenblatt **vollautomatisch** in euer eigenes Word-Design um - du
musst nichts mehr manuell zuordnen. Export wahlweise als **deutsches
oder englisches** PDF. Optional lässt sich eine zusätzliche KI-Kontrolle
per Internetzugriff aktivieren (siehe unten).

## Bedienung
1. **1. Datenblatt importieren** - fremde PDF auswählen. Das Programm
   erkennt automatisch Titel, Serie/Series, Beschreibung sowie alle
   Abschnitte mit technischen Werten - anhand von Schriftgröße und
   Textposition, ganz ohne KI. Erzeugt dabei GLEICHZEITIG einen
   deutschen und einen englischen Entwurf. Jeder übernommene Wert ist
   eine wörtliche Kopie aus der PDF.
2. **2. Datenblatt anzeigen** - zeigt einen Kontrollbericht (alle
   erkannten Werte, Quelle: wörtlich aus dem PDF) sowie eine Vorschau der
   deutschen Version. Ist ein KI-API-Key hinterlegt (siehe unten), läuft
   hier zusätzlich eine KI-Prüfung mit.
3. **3. Export Deutsch** / **4. Export Englisch** - speichert das
   fertige Datenblatt in der gewählten Sprache als **PDF**. Die
   Umwandlung passiert lokal: zuerst wird versucht, installiertes
   Microsoft Word zu nutzen (beste Qualität, 1:1 originalgetreu),
   ersatzweise LibreOffice, falls das installiert ist.


## Optionale KI-Kontrolle (Internetzugriff)
Über den Button **"⚙ KI-Einstellungen"** kannst du einen eigenen
Anthropic-API-Key hinterlegen (lokal in `config.json`, wird nie
mitgeliefert oder fest im Code hinterlegt). Ist ein Key hinterlegt, prüft
"2. Datenblatt anzeigen" den Entwurf zusätzlich per KI-Aufruf gegen die
Rohdaten und zeigt Auffälligkeiten an - **die KI erzeugt dabei selbst
keine Werte**, sie vergleicht nur und meldet Unstimmigkeiten. Die
eigentlichen Werte im Dokument stammen weiterhin ausschließlich aus der
deterministischen Erkennung in `lib.py`. So bleibt die "keine
Halluzination"-Garantie strukturell erhalten, auch mit KI-Zusatzprüfung.

Ohne API-Key läuft alles wie gehabt komplett lokal/offline - die
KI-Kontrolle wird dann automatisch übersprungen.

Wichtig zu wissen, bevor du einen Key einträgst:
- Es wird dabei Internetzugriff benötigt (Aufruf von `api.anthropic.com`).
- Der Inhalt des Entwurfs (also Daten aus dem fremden Datenblatt) wird an
  die Anthropic-API geschickt.
- Pro Prüfung fallen API-Kosten an (aktuelle Preise:
  https://docs.claude.com/en/api/overview bzw. deine Anthropic-Console).
- Der Key liegt nur lokal in `config.json` neben dem Programm - diese
  Datei nicht weitergeben, nicht in git einchecken.
- Einen eigenen API-Key erhältst du über die Anthropic-Console
  (https://console.anthropic.com).

## Vorlagen (Deutsch + Englisch)
`vorlage.docx` (Deutsch) und `vorlage_en.docx` (Englisch) sind die festen
"Baupläne" fürs Ergebnis-Datenblatt - abgeleitet aus euren eigenen
Beispiel-Datenblättern (Banner mit echtem Logo, "EPS - Datenblatt"/
"EPS - Datasheet"-Kopf, feste Fußzeile mit den echten EPS-Firmendaten,
leicht unterschiedlicher Wortlaut je Sprache wie im Original).

**Drei Tabellen mit fest vorausgefüllten Kategorien** pro Sprache (linke
Spalte steht fix in der Vorlage, kommt NICHT aus dem Quell-PDF):
- Deutsch: "Allgemeine Daten" (42), "Schnittstellen" (11), "Technische
  Daten" (16) - Kategorienliste in `kategorien.py`
- Englisch: "General data" (44), "Interfaces" (11), "Technical data" (19)
  - Kategorienliste in `kategorien_en.py`

Beim Import wird für jede feste Kategorie im Quell-PDF nach einem Label
mit (fast) demselben Text gesucht - Treffer wird wörtlich übernommen,
sonst bleibt die Zeile leer/markiert. Listen ergänzen/anpassen und
danach `python3 build_template.py` laufen lassen, um BEIDE Vorlagen neu
zu erzeugen (überschreibt ggf. von Hand angepasste Versionen, vorher
sichern).

**"Optionen"/"Options" und "Lieferumfang"/"Scope of delivery" bleiben
dynamisch** (Zeilenanzahl passt sich automatisch an die Anzahl im
Quell-PDF an).

Falls du das Design (Farben, Schriftart, Logo) anpassen willst: die
jeweilige .docx direkt in Word öffnen. Platzhalter, die dabei erhalten
bleiben müssen: `{{TITEL}}`, `{{SERIE}}`, `{{PRODUKTTYP}}`,
`{{BESCHREIBUNG}}`, `{{VAL:<Kategorie>}}` (eine pro fester Zeile),
`{{TABLE:OPTIONEN}}`/`{{TABLE:OPTIONS}}`,
`{{TABLE:LIEFERUMFANG}}`/`{{TABLE:SCOPEOFDELIVERY}}`.



## Installation als .exe (einmalig auf einem Windows-PC)
1. Python installieren (falls nicht vorhanden): https://www.python.org/downloads/
   - beim Installer "Add python.exe to PATH" ankreuzen.
2. Diesen Ordner auf den Windows-PC kopieren.
3. Doppelklick auf `build_exe.bat`.
4. Nach ca. 1-2 Minuten liegt in `dist\` die Datei `Datenblatt-Converter.exe`.
5. `Datenblatt-Converter.exe` UND `vorlage.docx` gemeinsam an den
   gewünschten Ort verschieben (z.B. Desktop) - beide müssen im selben
   Ordner liegen.
6. Für Startmenü-Verknüpfung: Rechtsklick auf die exe -> Verknüpfung
   erstellen -> die Verknüpfung nach
   `C:\Users\<Name>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs`
   verschieben.

## Grenzen (bewusst, gegen Fehler/Halluzination)
- Funktioniert am zuverlässigsten bei Datenblättern mit klar getrennten
  Label/Wert-Spalten oder "Label: Wert"-Zeilen (deckt die meisten
  technischen B2B-Datenblätter ab, inkl. farbiger Tabellenzellen ohne
  sichtbare Linien).
- Reine Bild-Scans (kein eingebetteter PDF-Text) werden nicht erkannt -
  bewusst kein OCR, um keine unsichere Texterkennung einzubauen.
- Bei ungewöhnlichen Layouts kann die automatische Abschnittserkennung
  vereinzelt Zeilen falsch zuordnen (prüfbar über "Datenblatt anzeigen"
  vor dem Export). Alle Werte bleiben aber immer wörtliche Kopien aus dem
  Quell-PDF - es wird nie etwas erfunden oder umformuliert.

## Dateien
```
app.py             GUI mit den 3 Buttons
lib.py              automatische Erkennung + Vorlage befüllen
vorlage.docx         deine Design-Vorlage (hier anpassen)
build_template.py    erzeugt bei Bedarf eine neue Start-Vorlage
build_exe.bat         Windows-Build-Skript
requirements.txt
```
