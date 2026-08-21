# Struktur-Checkliste für erzeugte Datenblätter

Diese Checkliste definiert, was ein korrekt erzeugtes Datenblatt (Ausgabe
von `build_draft()`) erfüllen MUSS - unabhängig davon, wie das jeweilige
Quell-PDF aufgebaut ist. Sie ist die einzige Referenz für "stimmt die
Struktur" - nicht eine vage Ähnlichkeit zu Beispielbildern.

Bei jedem Testlauf (siehe `.claude/commands/struktur-loop.md`) wird jeder
Punkt für JEDES PDF in `test-pdfs/` geprüft.

## 1. Kopf & Titel
- [ ] `{{SERIE}}` ist befüllt (nicht leer, kein `-- nicht gefunden --`)
- [ ] `{{TITEL}}` ist ein plausibler Produktname/Modellbezeichner - KEIN
      Datum (Muster wie "Month DD, YYYY" oder "DD.MM.YYYY"), KEINE
      Personen-Initialen (z.B. "TS/kv"), KEINE Firmen-Kopfzeile
- [ ] `{{PRODUKTTYP}}` ist entweder plausibel befüllt oder leer (leer ist
      okay, falsch befüllt nicht - z.B. darf hier kein Wertepaar-Label wie
      "Input Voltage" hineinrutschen)

## 2. Beschreibung
- [ ] `{{BESCHREIBUNG}}` ist nicht leer und enthält mindestens 2
      zusammenhängende Sätze
- [ ] Enthält KEINE technischen Label/Wert-Fragmente, die eigentlich in
      eine Tabelle gehören (z.B. nicht "Input Voltage 95-264Vac" mitten im
      Fließtext)
- [ ] Bricht nicht mitten im Satz ab (letztes Zeichen ist Satzzeichen oder
      sinnvolles Wortende, kein abgeschnittener Halbsatz)

## 3. Datentabellen (Allgemeine Daten / Schnittstellen / Technische Daten /
   Optionen bzw. bei Fremdformaten die sinngemäß nächstliegende Zuordnung)
- [ ] JEDE Zeile hat genau EIN Label und GENAU EINEN dazugehörigen Wert -
      kein Wert, der eigentlich aus einer anderen, benachbarten Spalte der
      Quelle stammt (das war der Absopulse-Bug: "Input Voltage" bekam den
      Wert einer Spalte, die eigentlich zu "Line/Load Regulation" gehörte)
- [ ] Kein Tabellen-Label taucht identisch auch als Wert in einer anderen
      Zeile auf (starkes Indiz für Spalten-Vermischung)
- [ ] Wenn eine Quelle "Überschrift + mehrzeiliger Fließtext" statt
      "Label: Wert" nutzt (z.B. "Input Voltage" gefolgt von 3 Textzeilen
      Beschreibung), wird die Überschrift als Label und der gesamte
      folgende Text (bis zur nächsten Überschrift) als EIN zusammen-
      hängender Wert übernommen - nicht abgeschnitten, nicht vermischt
- [ ] Keine Tabelle enthält offensichtliche Kopf-/Fußzeilen-Reste
      (Seitenzahlen, Firmenname der Quelle als Tabellenzeile, o.ä.)

## 4. Listen (z.B. Lieferumfang)
- [ ] Enthält nur tatsächlich in der Quelle als Liste erkennbare Einträge
- [ ] Keine Vermischung mit dem Produkttitel oder anderen Überschriften

## 5. Allgemein
- [ ] KEIN `{{...}}`-Platzhalter bleibt im erzeugten Dokument übrig
- [ ] KEIN Platzhaltertext wie `[HIER ... EINFÜGEN]` oder
      `[EIGENE FIRMA GmbH]` taucht auf, WENN die Vorlage bereits mit
      echten Firmendaten befüllt wurde (falls die Vorlage selbst noch
      Platzhalter enthält, ist das ein Vorlagen-Problem, kein Extraktions-
      Problem - im Bericht klar benennen, WELCHE der beiden Ursachen es
      ist)
- [ ] Jeder eingesetzte Wert ist eine wörtliche Kopie aus dem Quell-PDF
      (Stichprobe: 5 zufällige Werte manuell mit dem Quelltext
      abgleichen)

## Bekannte Layout-Typen (zur Diagnose, nicht abschließend)
- **Typ A - einspaltige Label:Wert-Tabelle** (z.B. EPS-Datenblätter):
  farbige Zellen ohne Rahmen, Label und Wert durch großen horizontalen
  Abstand oder Doppelpunkt getrennt. Funktioniert bereits zuverlässig.
- **Typ B - mehrspaltiges Fließtext-Layout** (z.B. Absopulse SCD):
  mehrere Spalten nebeneinander, jede Spalte enthält abwechselnd fette
  Überschriften und mehrzeiligen Beschreibungstext. Erfordert
  Spaltenerkennung (Wörter nach x-Position in Spalten clustern, dann
  jede Spalte separat von oben nach unten lesen, BEVOR die bestehende
  Zeilen-für-Zeilen-Logik angewendet wird) UND Erkennung von
  "Überschrift + Fließtext" als Label/Wert-Paar (nicht nur "Überschrift +
  weitere Label:Wert-Paare" wie bisher).
