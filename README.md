# Alfred Translate

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS%2026%2B-lightgrey.svg)](#requirements)

An [Alfred](https://www.alfredapp.com/) workflow that translates text using
Apple's **on-device** Translation framework (macOS 26+), with a pluggable
provider layer so online backends like Kagi can be added later.

The `translate` binary (a build of
[scriptingosx/translate-cli](https://github.com/scriptingosx/translate-cli)) is
vendored into `bin/`, so the workflow runs fully offline with no install step.

## Install

Download `Translate.alfredworkflow` from the
[latest release](https://github.com/kyrisu/alfred-translate/releases/latest) and
double-click it to import into Alfred. The vendored binary runs offline, so
there's no further install step — but see [Requirements](#requirements) for the
macOS version and language packs the Translation framework needs.

To build from source instead, see [Development](#development).

## Usage

In Alfred, type the keyword then your text:

```
tr Buenos días, ¿cómo estás?
```

Press Enter to copy the translation to the clipboard.

Direction is automatic: the workflow detects the input language and translates
toward the other half of your configured language pair (default `en` ↔ `es`).
Text outside the pair translates to Language A.

## Configuration

In Alfred, right-click the workflow → **Configure Workflow**:

| Setting | Default | Meaning |
|:--|:--|:--|
| Provider | `apple` | Backend: `apple` (offline), `kagi` (online), or `auto` |
| Language A | `en` | First language of the pair |
| Language B | `es` | Second language of the pair |
| Fixed target | _(empty)_ | Pin one target language and skip auto-routing |

## Requirements

- **macOS 26+** — the Translation framework is unavailable on earlier versions.
- **Language packs** must be downloaded once before first use:
  System Settings → General → Language & Region → Translation Languages.
  Without the pack you'll see "Language pack not downloaded".

## Caveats

- Single ambiguous words can mis-detect (e.g. "gato" reads as Portuguese as
  easily as Spanish). Pin a fixed target, or give more context, to avoid this.
- The vendored binary is built locally, so it carries no Gatekeeper quarantine.
  If you redistribute the `.alfredworkflow` by download, the recipient may need
  to clear the quarantine flag (`xattr -d com.apple.quarantine bin/translate`).

## Development

```sh
make vendor    # build translate-cli from source and refresh bin/translate
make test      # run the pipeline against sample input
make package   # produce Translate.alfredworkflow for import
```

### Adding a provider

1. Subclass `Provider` in `src/providers/` (see `apple.py` for the pattern).
   Implement `available()`, `detect()`, and `translate()`.
2. Register it in `src/providers/__init__.py` (`_REGISTRY`).
3. Add it to the Provider dropdown in `info.plist`
   (`userconfigurationconfig` → Provider → `pairs`).

`src/providers/kagi.py` is a stubbed example waiting on a Kagi Translation API
beta key (request one from `support@kagi.com`); set `KAGI_API_KEY` and fill in
the endpoint once its shape is confirmed.

## Layout

```
info.plist           Alfred workflow definition (Script Filter → Clipboard)
bin/translate        Vendored translate-cli binary (Apple Translation framework)
src/translate.py     Script Filter entry point: query in, Alfred JSON out
src/config.py        Settings + bidirectional routing
src/providers/       Provider interface and implementations
Makefile             vendor / test / package
```

## License

This workflow's own code (everything under `src/`, the `Makefile`, `info.plist`,
and this README) is released under the [MIT License](LICENSE).

### Third-party attribution

The vendored `bin/translate` binary is a build of
[scriptingosx/translate-cli](https://github.com/scriptingosx/translate-cli) by
Armin Briegel, distributed under the **Apache License, Version 2.0**. Its full
license text is reproduced in [`THIRD_PARTY_LICENSES`](THIRD_PARTY_LICENSES),
which travels inside the packaged `.alfredworkflow` alongside the binary.
