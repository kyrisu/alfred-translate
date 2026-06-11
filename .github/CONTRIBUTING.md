# Contributing

Thanks for your interest in improving Alfred Translate.

## Development setup

The build is driven by `make` (see the [Development](../README.md#development)
section of the README):

```sh
make vendor    # build translate-cli from source and refresh bin/translate
make test      # run the translation pipeline against sample input
make package   # produce Translate.alfredworkflow for import
```

`make test` exercises the real Apple Translation framework, so it only runs on
**macOS 26+** with the relevant language packs installed. CI cannot run it (see
below).

## Adding a provider

The translation backend is pluggable. To add one:

1. Subclass `Provider` in `src/providers/` (see `apple.py` for the pattern):
   implement `available()`, `detect()`, and `translate()`.
2. Register it in `src/providers/__init__.py` (`_REGISTRY`).
3. Add it to the Provider dropdown in `info.plist`
   (`userconfigurationconfig` → Provider → `pairs`).

## Editing the Script Filter

The Script Filter is configured as an **External Script** with input passed as
`argv` (not interpolated into a shell). If you change it, prefer editing through
Alfred's GUI and committing the `info.plist` readback, and re-verify that shell
metacharacters in the query stay literal — `make test` bypasses Alfred's input
layer and cannot catch a regression there.

## Continuous integration

CI runs `py_compile` and `plutil -lint` only. GitHub-hosted runners lack the
macOS 26 Translation framework and language packs, so the end-to-end
translation path is **not** exercised in CI — please test translations locally
in Alfred before opening a pull request.
