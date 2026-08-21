"""
app.py - Datenblatt-Converter, einfache Bedienoberfläche
==========================================================
Drei Schritte, drei Buttons - kein manuelles Zuordnen nötig:

1. "Datenblatt importieren"   -> PDF wählen, automatische Erkennung läuft
2. "Datenblatt anzeigen"      -> Entwurf + Kontrollbericht ansehen
3. "Datenblatt exportieren"   -> fertiges PDF speichern (lokal aus der
                                  .docx-Vorlage erzeugt, über installiertes
                                  Microsoft Word oder ersatzweise
                                  LibreOffice - kein Internet nötig)

Alles läuft lokal, ohne Internet-/Serverzugriff. Es wird nichts erfunden:
jeder Wert im Ergebnis ist eine wörtliche Kopie aus dem importierten PDF
(siehe lib.py). Vor jedem Export kannst du über "Anzeigen" den
Kontrollbericht prüfen.
"""
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox

from lib import extract_pdf, build_draft, read_docx_text, build_control_report, convert_to_pdf, PdfConversionError
from ai_check import ai_verify
import config as cfgmod

BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
RUN_DIR = Path(sys.argv[0]).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
TEMPLATE_PATH_DE = RUN_DIR / "vorlage.docx"
TEMPLATE_PATH_EN = RUN_DIR / "vorlage_en.docx"
OUTPUT_DIR = RUN_DIR / "ausgabe"
OUTPUT_DIR.mkdir(exist_ok=True)

# Sprachspezifische Einstellungen für build_draft() - siehe lib.py
LANG_DE = dict(
    template=TEMPLATE_PATH_DE, kategorien_module="kategorien",
    not_found_text="-- nicht gefunden --",
    lieferumfang_marker="LIEFERUMFANG", optionen_marker="OPTIONEN",
)
LANG_EN = dict(
    template=TEMPLATE_PATH_EN, kategorien_module="kategorien_en",
    not_found_text="-- not found --",
    lieferumfang_marker="SCOPEOFDELIVERY", optionen_marker="OPTIONS",
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Datenblatt-Converter")
        self.geometry("800x600")

        self.config_data = cfgmod.load_config(RUN_DIR)
        self.extracted = None          # zuletzt automatisch erkannte Daten
        self.draft_path_de = None      # Pfad zum deutschen Entwurf (temp)
        self.draft_path_en = None      # Pfad zum englischen Entwurf (temp)
        self.import_name = None

        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Button(top, text="1. Datenblatt importieren", command=self.import_pdf, width=26).pack(side="left", padx=3)
        ttk.Button(top, text="2. Datenblatt anzeigen", command=self.show_result, width=22).pack(side="left", padx=3)
        ttk.Button(top, text="3. Export Deutsch", command=lambda: self.export_result("de"), width=18).pack(side="left", padx=3)
        ttk.Button(top, text="4. Export Englisch", command=lambda: self.export_result("en"), width=18).pack(side="left", padx=3)
        ttk.Button(top, text="⚙ KI-Einstellungen", command=self.open_settings, width=16).pack(side="left", padx=3)

        ki_status = "aktiv" if self.config_data.get("anthropic_api_key") else "deaktiviert (kein API-Key)"
        self.status = ttk.Label(self, text=f"Bereit.  |  KI-Kontrolle: {ki_status}")
        self.status.pack(anchor="w", padx=10)

        self.text = tk.Text(self, wrap="word")
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

        fehlend = [p.name for p in (TEMPLATE_PATH_DE, TEMPLATE_PATH_EN) if not p.exists()]
        if fehlend:
            messagebox.showwarning(
                "Vorlage fehlt",
                f"Folgende Vorlage(n) wurden nicht gefunden: {', '.join(fehlend)}\n"
                "Bitte im Programmordner ablegen (siehe README).",
            )

    # -- Schritt 1 ----------------------------------------------------
    def import_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF-Dateien", "*.pdf")])
        if not path:
            return
        if not TEMPLATE_PATH_DE.exists() or not TEMPLATE_PATH_EN.exists():
            messagebox.showerror("Vorlage fehlt", "vorlage.docx und/oder vorlage_en.docx wurden nicht gefunden.")
            return
        try:
            self.extracted = extract_pdf(path)
            self.import_name = Path(path).stem
            self.draft_path_de = RUN_DIR / f"_entwurf_de_{self.import_name}.docx"
            self.draft_path_en = RUN_DIR / f"_entwurf_en_{self.import_name}.docx"
            build_draft(
                str(LANG_DE["template"]), self.extracted, str(self.draft_path_de),
                kategorien_module=LANG_DE["kategorien_module"], not_found_text=LANG_DE["not_found_text"],
                lieferumfang_marker=LANG_DE["lieferumfang_marker"], optionen_marker=LANG_DE["optionen_marker"],
            )
            build_draft(
                str(LANG_EN["template"]), self.extracted, str(self.draft_path_en),
                kategorien_module=LANG_EN["kategorien_module"], not_found_text=LANG_EN["not_found_text"],
                lieferumfang_marker=LANG_EN["lieferumfang_marker"], optionen_marker=LANG_EN["optionen_marker"],
            )
        except Exception as e:
            messagebox.showerror("Fehler beim Import", str(e))
            return

        n_pairs = sum(len(s["items"]) for s in self.extracted["sections"] if s["type"] == "pairs")
        self.status.config(
            text=f"Importiert: {Path(path).name}  |  {n_pairs} Werte automatisch erkannt und übertragen "
            "(Deutsch + Englisch). Weiter mit 'Datenblatt anzeigen'."
        )
        self.text.delete("1.0", "end")
        self.text.insert("end", "Import erfolgreich (beide Sprachversionen erzeugt). Klicke auf 'Datenblatt anzeigen' für die Kontrolle.")

    # -- Schritt 2 ----------------------------------------------------
    def show_result(self):
        if not self.extracted or not self.draft_path_de:
            messagebox.showwarning("Kein Import", "Bitte zuerst ein Datenblatt importieren.")
            return
        report = build_control_report(self.extracted)
        preview = read_docx_text(str(self.draft_path_de))

        self.text.delete("1.0", "end")
        self.text.insert("end", "=== KONTROLLBERICHT (Werte wörtlich aus dem PDF) ===\n\n")
        self.text.insert("end", report)

        api_key = self.config_data.get("anthropic_api_key", "")
        if api_key:
            self.status.config(text="Prüfe mit KI (Internetzugriff)...")
            self.update_idletasks()
            raw_text = "\n".join(self.extracted.get("raw_lines", []))
            ai_result = ai_verify(raw_text, preview, api_key, self.config_data.get("model", "claude-sonnet-5"))
            self.text.insert("end", "\n\n=== ZUSÄTZLICHE KI-KONTROLLE ===\n\n")
            self.text.insert("end", ai_result)
            self.status.config(text="KI-Kontrolle abgeschlossen.")

        self.text.insert("end", "\n\n=== VORSCHAU DES ERGEBNIS-DOKUMENTS (Deutsch) ===\n\n")
        self.text.insert("end", preview)

    # -- Einstellungen (optionaler API-Key) ----------------------------
    def open_settings(self):
        win = tk.Toplevel(self)
        win.title("KI-Einstellungen")
        win.geometry("500x220")

        ttk.Label(
            win,
            text=(
                "Optional: eigener Anthropic-API-Key für eine zusätzliche KI-Kontrolle\n"
                "(Entwurf wird dabei zur Anthropic-API geschickt - Internetzugriff nötig,\n"
                "Kosten pro Prüfung siehe docs.claude.com/en/api/overview). Ohne Key läuft\n"
                "alles wie bisher rein lokal, die KI-Kontrolle wird dann übersprungen."
            ),
            wraplength=460, justify="left",
        ).pack(padx=10, pady=10)

        ttk.Label(win, text="API-Key:").pack(anchor="w", padx=10)
        key_var = tk.StringVar(value=self.config_data.get("anthropic_api_key", ""))
        ttk.Entry(win, textvariable=key_var, width=60, show="*").pack(padx=10, pady=5)

        ttk.Label(win, text="Modell:").pack(anchor="w", padx=10)
        model_var = tk.StringVar(value=self.config_data.get("model", "claude-sonnet-5"))
        ttk.Entry(win, textvariable=model_var, width=30).pack(anchor="w", padx=10, pady=5)

        def save():
            self.config_data["anthropic_api_key"] = key_var.get().strip()
            self.config_data["model"] = model_var.get().strip() or "claude-sonnet-5"
            cfgmod.save_config(RUN_DIR, self.config_data)
            ki_status = "aktiv" if self.config_data["anthropic_api_key"] else "deaktiviert (kein API-Key)"
            self.status.config(text=f"Einstellungen gespeichert. KI-Kontrolle: {ki_status}")
            win.destroy()

        ttk.Button(win, text="Speichern", command=save).pack(pady=10)

    # -- Schritt 3/4 ----------------------------------------------------
    def export_result(self, lang: str):
        draft_path = self.draft_path_de if lang == "de" else self.draft_path_en
        lang_label = "Deutsch" if lang == "de" else "Englisch"
        if not draft_path or not draft_path.exists():
            messagebox.showwarning("Kein Entwurf", "Bitte zuerst importieren (und optional anzeigen).")
            return
        suffix = "" if lang == "de" else "_EN"
        default_name = f"{self.import_name}{suffix}.pdf" if self.import_name else f"datenblatt{suffix}.pdf"
        dest = filedialog.asksaveasfilename(
            initialdir=str(OUTPUT_DIR),
            initialfile=default_name,
            defaultextension=".pdf",
            filetypes=[("PDF-Dokument", "*.pdf")],
        )
        if not dest:
            return

        self.status.config(text=f"Wandle in PDF um ({lang_label})...")
        self.update_idletasks()
        try:
            convert_to_pdf(str(draft_path), dest)
        except PdfConversionError as e:
            messagebox.showerror("PDF-Umwandlung fehlgeschlagen", str(e))
            self.status.config(text="Export fehlgeschlagen (siehe Fehlermeldung).")
            return
        except Exception as e:
            messagebox.showerror("Fehler beim Export", str(e))
            self.status.config(text="Export fehlgeschlagen (siehe Fehlermeldung).")
            return

        self.status.config(text=f"Exportiert ({lang_label}) nach: {dest}")
        messagebox.showinfo("Fertig", f"Datenblatt ({lang_label}) gespeichert unter:\n{dest}")


if __name__ == "__main__":
    App().mainloop()
