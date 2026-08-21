"""
kategorien_en.py
=================
Englisches Gegenstück zu kategorien.py. Feste Kategorienlisten für die
Tabellen "General data", "Interfaces" und "Technical data" der englischen
Vorlage (vorlage_en.docx).

Grundlage: Vereinigungsmenge aus 4 eigenen englischen EPS-Datenblättern
(EPS/FTP/T, EPS/MCTSR, EPS/PUB 10000, EPS/PV). Bei Bedarf hier ergänzen,
danach `python3 build_template_en.py` erneut ausführen.
"""

GENERAL_DATA = [
    "Technology", "Operation modes", "Mains", "Input frequency",
    "Power factor", "Input Current Limitation", "Voltage Stability Load",
    "Voltage Stability Mains", "Cooling", "Operation temperature",
    "Humidity", "Design", "Standards", "ruggedized", "Behavior",
    "Power feed back", "Display", "Voltage resolution", "Voltage accuracy",
    "Current Resolution", "Current Accuracy", "Rise time Current",
    "Overheat protection", "Isolation In-/Output",
    "Isolation Output/Enclosure", "Protection class", "Parallel operation",
    "Attitude", "Response time Voltage", "Rise time Voltage",
    "Current Stability Load", "Current Stability Mains",
    "Output Current Limitation", "Internal Resistance Regulation",
    "Overvoltage category", "Current sharing", "Storage temperature",
    "Power fail", "Alarmmanagement", "Function generator",
    "Output Preset", "Capacity", "Power Accuracy", "Memory",
]

INTERFACES = [
    "Analog Programming", "Analog Isolation", "CAN Interface", "Profibus",
    "Ethernet Interface", "Ethercat Interface", "Accuracy Interface",
    "USB Interface", "RS232 Interface", "Software", "RS485 Interface",
]

TECHNICAL_DATA = [
    "Output Voltage", "Output Current", "Output Power", "Distortion",
    "Output Frequency", "Efficiency", "Ripple U",
    "Dimensions in mm (WxHxD)", "Weight", "Order code", "Ripple I",
    "Remote Sensing", "Input Current", "Resistance Adjustment Range 1",
    "Output Voltage 2", "Output Current 2", "Input Voltage",
    "Crest factor", "Frequency Accuracy",
]
