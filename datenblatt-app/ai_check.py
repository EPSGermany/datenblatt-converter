"""
ai_check.py - optionale KI-gestützte Zusatzkontrolle
======================================================
Diese Funktion ist rein additiv und optional (nur aktiv, wenn ein eigener
Anthropic-API-Key in config.json hinterlegt ist). Sie ERSETZT NICHT die
deterministische Extraktion aus lib.py - die bleibt immer die alleinige
Quelle für die tatsächlich eingesetzten Werte. Die KI bekommt hier nur eine
reine PRÜF-Aufgabe: Entwurf gegen Rohdaten abgleichen und Auffälligkeiten
benennen. Sie generiert oder verändert selbst keine Werte im Dokument.

Erfordert Internetzugriff und einen eigenen Anthropic-API-Key (siehe
config.json). Ohne Key wird dieser Schritt automatisch übersprungen.
"""
import json
import urllib.request
import urllib.error

API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-sonnet-5"

SYSTEM_PROMPT = (
    "Du bist ein reiner PRÜFER, kein Generator. Du bekommst zwei Texte: "
    "(1) die wörtlich aus einem PDF-Datenblatt extrahierten Rohdaten und "
    "(2) einen daraus automatisch erzeugten Entwurf in einem anderen Layout. "
    "Deine einzige Aufgabe: prüfe, ob jeder Wert im Entwurf wörtlich in den "
    "Rohdaten vorkommt, und ob ein eindeutig zuordenbarer Wert aus den "
    "Rohdaten im Entwurf fehlt oder falsch zugeordnet wurde. "
    "Antworte NUR mit einer kurzen Liste von Auffälligkeiten (oder 'Keine "
    "Auffälligkeiten gefunden.'). Erfinde, ergänze oder formuliere NIEMALS "
    "eigene Werte - du gibst ausschließlich eine Prüf-Einschätzung ab."
)


def ai_verify(raw_text: str, draft_text: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    """Schickt Rohdaten + Entwurf zur Prüfung an die Anthropic API.
    Gibt den Prüftext zurück oder eine Fehlermeldung, falls der Aufruf
    fehlschlägt (z.B. kein Internet, ungültiger Key)."""
    if not api_key:
        return "KI-Kontrolle übersprungen (kein API-Key in config.json hinterlegt)."

    user_content = (
        f"=== ROHDATEN (wörtlich aus dem PDF) ===\n{raw_text}\n\n"
        f"=== ENTWURF (automatisch erzeugt) ===\n{draft_text}"
    )
    payload = {
        "model": model,
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": user_content}],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        parts = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
        return "\n".join(parts) if parts else "(Keine Textantwort erhalten.)"
    except urllib.error.HTTPError as e:
        return f"KI-Kontrolle fehlgeschlagen (HTTP {e.code}): {e.read().decode('utf-8', 'ignore')[:300]}"
    except Exception as e:
        return f"KI-Kontrolle fehlgeschlagen: {e}"
