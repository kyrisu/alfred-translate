"""Workflow settings, read from Alfred workflow environment variables.

All values are configurable in Alfred's workflow UI (Configure Workflow)
without editing code; the defaults below apply when a variable is unset.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    provider: str
    pair_a: str
    pair_b: str
    target_lang: str  # explicit override; empty means use bidirectional routing

    @classmethod
    def load(cls) -> "Settings":
        return cls(
            provider=os.environ.get("provider", "apple"),
            pair_a=os.environ.get("pair_a", "en").strip().lower(),
            pair_b=os.environ.get("pair_b", "es").strip().lower(),
            target_lang=os.environ.get("target_lang", "").strip().lower(),
        )

    def resolve_target(self, detected: str | None) -> str:
        """Pick the target language.

        With an explicit ``target_lang`` set, always use it. Otherwise route
        bidirectionally: text in one half of the pair translates to the other.
        Anything outside the pair goes to ``pair_a``.
        """
        if self.target_lang:
            return self.target_lang
        if detected == self.pair_a:
            return self.pair_b
        if detected == self.pair_b:
            return self.pair_a
        return self.pair_a
