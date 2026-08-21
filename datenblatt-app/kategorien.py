"""
kategorien.py
=============
Feste Kategorienlisten für die Tabellen "Allgemeine Daten", "Schnittstellen"
und "Technische Daten". Diese Listen bestimmen die linke Spalte (Label) in
vorlage.docx - sie werden dort als feste Zeilen eingetragen, nicht mehr
automatisch aus dem Quell-PDF erkannt.

Grundlage: Vereinigungsmenge aus 4 eigenen EPS-Datenblättern
(E/PS 9000T, EPS/MP, E/PSB 10000, EPS/B). Bei Bedarf hier einfach weitere
Kategorien ergänzen (Reihenfolge = Reihenfolge in der Tabelle) - danach
`python3 build_template.py` erneut ausführen, um vorlage.docx neu zu
erzeugen (ACHTUNG: das überschreibt eine ggf. bereits von Hand angepasste
vorlage.docx - vorher sichern falls nötig).

"Optionen" und "Lieferumfang" stehen bewusst NICHT hier - die bleiben
dynamisch (Zeilenanzahl variiert je Produkt zu stark für eine feste Liste).
"""

ALLGEMEINE_DATEN = [
    "Technologie", "Betriebsarten", "Netzanschluss", "Eingangsfrequenz",
    "Leistungsfaktor", "Anzeige", "Spannungsauflösung", "Spannungsgenauigkeit",
    "Spannungsstabilität Last", "Spannungsstabilität Netz",
    "Spannungsausregelung Last", "Anstiegszeit Spannung", "Stromauflösung",
    "Stromgenauigkeit", "Stromstabilität Last", "Stromstabilität Netz",
    "Begrenzung Ausgangsstrom", "Leistungsgenauigkeit",
    "Überspannungskategorie", "Überhitzungsschutz",
    "Spannungsfestigkeit Eingang zu Ausgang",
    "Spannungsfestigkeit Ausgang zu Gehäuse", "Schutzklasse",
    "Reihenschaltung", "Parallelschaltung", "Kühlung", "Betriebstemperatur",
    "Lagertemperatur", "Luftfeuchtigkeit", "Betriebshöhe", "Bauform",
    "Normen", "Power fail", "Voreinstellung Ausgang", "Speicherplätze",
    "Current Sharing", "Netzrückspeisung", "Anstiegszeit Strom",
    "Innenwiderstandsregelung", "Alarmmanagement", "Funktionsgenerator",
    "Kapazität",
]

SCHNITTSTELLEN = [
    "Analoge Programmierung ISO", "Genauigkeit Schnittstelle",
    "USB Schnittstelle", "Ethernet Schnittstelle", "Software",
    "RS232 Schnittstelle", "RS485 Schnittstelle", "GBIP Schnittstelle",
    "CAN Schnittstelle", "Profibus", "Ethercat Schnittstelle",
]

TECHNISCHE_DATEN = [
    "Ausgangsspannung", "Ausgangsstrom", "Ausgangsleistung", "Wirkungsgrad",
    "Restwelligkeit U", "Restwelligkeit I", "Fernfühlungsausregelung",
    "Abmessung in mm (B x H x T)", "Gewicht", "Bestellnummer",
    "Widerstand Einstellbereich 1", "Widerstand Auflösung", "Scheitelfaktor",
    "Klirrfaktor", "Ausgangsfrequenz", "Frequenzgenauigkeit",
]
