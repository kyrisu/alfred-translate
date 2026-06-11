"""Offline provider backed by the vendored `translate` binary, which wraps
Apple's on-device Translation framework (macOS 26+)."""

from __future__ import annotations

import os
import subprocess

from .base import Provider, Result, TranslationError

# bin/translate sits next to the src/ tree, resolved from this file rather than
# the working directory so the provider works no matter how it is invoked.
_BIN = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "bin",
    "translate",
)


class AppleProvider(Provider):
    name = "apple"

    def available(self) -> bool:
        return os.path.isfile(_BIN) and os.access(_BIN, os.X_OK)

    def _run(self, args: list[str], text: str) -> str:
        try:
            proc = subprocess.run(
                [_BIN, *args, text],
                capture_output=True,
                text=True,
                timeout=15,
            )
        except FileNotFoundError as exc:
            raise TranslationError("translate binary missing from bin/") from exc
        except subprocess.TimeoutExpired as exc:
            raise TranslationError("translation timed out") from exc

        if proc.returncode != 0:
            stderr = proc.stderr.strip()
            if "Unable to Translate" in stderr:
                raise TranslationError(
                    "Language pack not downloaded. System Settings > "
                    "General > Language & Region > Translation Languages."
                )
            raise TranslationError(stderr or "translation failed")
        return proc.stdout.strip()

    def detect(self, text: str) -> str | None:
        code = self._run(["detect"], text)
        return code or None

    def translate(self, text: str, dst: str, src: str | None = None) -> Result:
        args = ["--to", dst]
        if src:
            args += ["--from", src]
        out = self._run(args, text)
        return Result(text=out, src=src or "auto", dst=dst, provider=self.name)
