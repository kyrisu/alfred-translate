#!/usr/bin/env python3
"""Alfred Script Filter entry point.

Reads the query (argv), routes it to a translation provider, and emits the
Alfred Script Filter JSON format on stdout. Never raises: any failure becomes
a non-actionable result item so Alfred always renders something useful.
"""

from __future__ import annotations

import json
import sys

from config import Settings
from providers import TranslationError, get_provider


def _emit(items: list[dict]) -> None:
    json.dump({"items": items}, sys.stdout)


def _message(title: str, subtitle: str = "") -> dict:
    return {"title": title, "subtitle": subtitle, "valid": False}


def main() -> None:
    query = (sys.argv[1] if len(sys.argv) > 1 else "").strip()
    if not query:
        _emit([_message("Type text to translate", "Auto-detects language and direction")])
        return

    settings = Settings.load()
    provider = get_provider(settings.provider)

    if not provider.available():
        _emit([_message(f"Provider '{provider.name}' unavailable",
                        "Check binary, API key, or network")])
        return

    try:
        # Detection is only needed for bidirectional routing; skip it (and the
        # extra subprocess) when the target language is pinned.
        detected = provider.detect(query) if not settings.target_lang else None
        target = settings.resolve_target(detected)
        result = provider.translate(query, dst=target, src=detected)
    except TranslationError as exc:
        _emit([_message("Translation failed", str(exc))])
        return
    except Exception as exc:  # noqa: BLE001 - last resort so Alfred never sees a crash
        _emit([_message("Unexpected error", str(exc))])
        return

    _emit([{
        "title": result.text,
        "subtitle": f"{result.src} → {result.dst} · {result.provider}",
        "arg": result.text,
        "valid": True,
        "text": {"copy": result.text, "largetype": result.text},
    }])


if __name__ == "__main__":
    main()
