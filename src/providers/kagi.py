"""Online provider for Kagi Translate.

The Kagi Translation API is in private beta as of mid-2026 and not publicly
documented. Request a key by emailing support@kagi.com, set KAGI_API_KEY, and
fill in the endpoint/payload below once the shape is confirmed. Until then the
provider reports itself unavailable so routing falls back to Apple.
"""

from __future__ import annotations

import os

from .base import Provider, Result, TranslationError

ENDPOINT = "https://translate.kagi.com/api/v0/translate"  # placeholder until beta docs land


class KagiProvider(Provider):
    name = "kagi"

    def __init__(self) -> None:
        self.api_key = os.environ.get("KAGI_API_KEY", "").strip()

    def available(self) -> bool:
        # Stub: report unavailable until translate() is implemented, so `auto`
        # falls back to Apple even when a key is present.
        return False

    def detect(self, text: str) -> str | None:
        return None

    def translate(self, text: str, dst: str, src: str | None = None) -> Result:
        raise TranslationError(
            "Kagi provider not wired yet — needs a beta API key and the "
            "confirmed endpoint. See src/providers/kagi.py."
        )
