"""Common provider contract shared by every translation backend."""

from __future__ import annotations

from dataclasses import dataclass


class TranslationError(Exception):
    """Raised when a provider cannot produce a translation.

    The message is surfaced verbatim to the user in Alfred, so it should be
    short and actionable (e.g. point at a missing language pack).
    """


@dataclass
class Result:
    text: str
    src: str
    dst: str
    provider: str


class Provider:
    name = "base"

    def available(self) -> bool:
        """Whether this provider can be used right now (binary present,
        network reachable, key configured, ...)."""
        return True

    def detect(self, text: str) -> str | None:
        """Return the dominant language code of ``text`` or ``None``."""
        raise NotImplementedError

    def translate(self, text: str, dst: str, src: str | None = None) -> Result:
        raise NotImplementedError
