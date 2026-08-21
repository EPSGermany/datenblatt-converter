"""
pdf_export.py - Direkte PDF-Erzeugung ohne Word/LibreOffice
===============================================================
Erzeugt das Ergebnis-Datenblatt als PDF, komplett ohne externe
Abhängigkeit auf installierte Office-Software. Nutzt reportlab (reines
Python, wird von PyInstaller problemlos mitgebündelt - kein COM/DLL-
Ärger wie bei docx2pdf).

Design-Hinweis: Anpassungen am Layout (Farben, Schriftgrößen, Reihenfolge)
erfolgen hier im Code, nicht mehr per Word-Bearbeitung wie bei
vorlage.docx. Der docx-Export bleibt separat bestehen, falls ihr in Word
weiterarbeiten wollt.

Nutzt dieselben Zuordnungs-Funktionen wie build_draft() in lib.py
(resolve_categories, find_matching_list_items, find_matching_pairs_items)
- identische Werte, nur andere Ausgabeform.
"""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, KeepTogether,
)

from lib import resolve_categories, find_matching_list_items, find_matching_pairs_items

SHADE_COLOR = colors.HexColor("#DCE9F7")
NOT_FOUND_GRAY = colors.HexColor("#767676")


def _styles():
    ss = getSampleStyleSheet()
    styles = {
        "kopf": ParagraphStyle("kopf", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10),
        "serie": ParagraphStyle(
            "serie", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13,
            alignment=TA_CENTER, spaceAfter=6,
        ),
        "body": ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13),
        "titel": ParagraphStyle("titel", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=11),
        "abschnitt": ParagraphStyle(
            "abschnitt", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=10, spaceAfter=4,
        ),
        "zelle": ParagraphStyle("zelle", parent=ss["Normal"], fontName="Helvetica", fontSize=9, leading=11),
        "fuss": ParagraphStyle("fuss", parent=ss["Normal"], fontName="Helvetica", fontSize=7.5, leading=10),
    }
    return styles


def _make_category_table(pairs, styles, not_found_text):
    """pairs: Liste von (label, value). Baut eine 2-spaltige Tabelle mit
    alternierender Hintergrundfarbe (wie im Word-Design)."""
    rows = [[Paragraph(label, styles["zelle"]), Paragraph(value, styles["zelle"])] for label, value in pairs]
    t = Table(rows, colWidths=[6.5 * cm, 10.5 * cm])
    style_cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
    ]
    for i, (label, value) in enumerate(pairs):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), SHADE_COLOR))
        if value == not_found_text:
            style_cmds.append(("TEXTCOLOR", (1, i), (1, i), NOT_FOUND_GRAY))
    t.setStyle(TableStyle(style_cmds))
    return t


def build_preview_text(extracted: dict, lang_cfg: dict) -> str:
    """Textvorschau des Ergebnisses, ohne docx zu erzeugen - nutzt
    dieselben Zuordnungsfunktionen wie build_pdf_native()."""
    not_found = lang_cfg["not_found_text"]
    lines = [
        lang_cfg["kopf_text"],
        f"{lang_cfg['serie_label']} {extracted.get('serie', '') or not_found}",
        "",
        extracted.get("beschreibung", "") or not_found,
        "",
        lang_cfg["lieferumfang_label"],
    ]
    lines += find_matching_list_items(extracted["sections"], lang_cfg["lieferumfang_marker"]) or [not_found]
    lines += ["", extracted.get("titel", "") or not_found, extracted.get("produkttyp", "") or not_found, ""]

    resolved = resolve_categories(extracted, lang_cfg["kategorien_module"], not_found)
    for heading, kategorien_liste in lang_cfg["tabellen"]:
        lines.append(heading)
        for kat in kategorien_liste:
            lines.append(f"  {kat}: {resolved.get(kat, not_found)}")
        lines.append("")

    options_items = find_matching_pairs_items(extracted["sections"], lang_cfg["optionen_marker"])
    if options_items:
        lines.append(lang_cfg["optionen_label"])
        for label, value in options_items:
            lines.append(f"  {label}: {value}")

    return "\n".join(lines)


def build_pdf_native(extracted: dict, output_path: str, lang_cfg: dict):
    """Erzeugt das Ergebnis-Datenblatt direkt als PDF (reportlab), ohne
    Word/LibreOffice. `lang_cfg` ist LANG_DE oder LANG_EN aus app.py
    (enthält Vorlagentexte, Kategorienlisten, Marker-Namen)."""
    not_found_text = lang_cfg["not_found_text"]
    styles = _styles()
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.5 * cm, bottomMargin=1.5 * cm,
    )
    story = []

    banner_path = lang_cfg.get("banner_path")
    if banner_path and Path(banner_path).exists():
        img = Image(banner_path, width=17 * cm, height=17 * cm * (525 / 3132))
        story.append(img)
        story.append(Spacer(1, 10))

    story.append(Paragraph(lang_cfg["kopf_text"], styles["kopf"]))
    story.append(Spacer(1, 4))
    serie_value = extracted.get("serie", "") or not_found_text
    story.append(Paragraph(f"<u>{lang_cfg['serie_label']} {serie_value}</u>", styles["serie"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(extracted.get("beschreibung", "") or not_found_text, styles["body"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(lang_cfg["lieferumfang_label"], styles["body"]))
    lieferumfang_items = find_matching_list_items(extracted["sections"], lang_cfg["lieferumfang_marker"])
    for item in lieferumfang_items:
        story.append(Paragraph(item, styles["body"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(extracted.get("titel", "") or not_found_text, styles["titel"]))
    story.append(Paragraph(extracted.get("produkttyp", "") or not_found_text, styles["titel"]))
    story.append(Spacer(1, 10))

    resolved = resolve_categories(extracted, lang_cfg["kategorien_module"], not_found_text)
    for heading, kategorien_liste in lang_cfg["tabellen"]:
        pairs = [(kat, resolved.get(kat, not_found_text)) for kat in kategorien_liste]
        story.append(Paragraph(f"<u>{heading}</u>", styles["abschnitt"]))
        story.append(_make_category_table(pairs, styles, not_found_text))
        story.append(Spacer(1, 6))

    options_items = find_matching_pairs_items(extracted["sections"], lang_cfg["optionen_marker"])
    if options_items:
        story.append(Paragraph(f"<u>{lang_cfg['optionen_label']}</u>", styles["abschnitt"]))
        story.append(_make_category_table(options_items, styles, not_found_text))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 14))
    story.append(Paragraph(lang_cfg["fuss1_text"], styles["fuss"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(lang_cfg["fuss2_text"].replace("\n", "<br/>"), styles["fuss"]))

    doc.build(story)
