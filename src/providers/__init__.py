"""Provider registry and selection."""

from __future__ import annotations

from .apple import AppleProvider
from .base import Provider, Result, TranslationError
from .kagi import KagiProvider

__all__ = ["Provider", "Result", "TranslationError", "get_provider"]

_REGISTRY: dict[str, type[Provider]] = {
    "apple": AppleProvider,
    "kagi": KagiProvider,
}


def get_provider(name: str) -> Provider:
    """Resolve a provider by name.

    ``auto`` prefers the first available online provider and falls back to the
    offline Apple provider, so the workflow keeps working without a network.
    """
    name = (name or "apple").strip().lower()

    if name == "auto":
        kagi = KagiProvider()
        return kagi if kagi.available() else AppleProvider()

    factory = _REGISTRY.get(name, AppleProvider)
    return factory()
