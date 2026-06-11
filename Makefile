REPO    := https://github.com/scriptingosx/translate-cli.git
SRCDIR  := build/translate-cli
WORKDIR := $(shell pwd)
PKG     := Translate.alfredworkflow

.PHONY: help vendor package clean test

help:
	@echo "make vendor   - build translate-cli from source and vendor the binary into bin/"
	@echo "make test     - run the translation pipeline against sample input"
	@echo "make package  - zip the workflow into $(PKG)"
	@echo "make clean     - remove build artifacts and the packaged workflow"

vendor:
	@rm -rf $(SRCDIR)
	@git clone --depth 1 $(REPO) $(SRCDIR)
	@cd $(SRCDIR) && swift build -c release
	@cp $(SRCDIR)/.build/release/translate bin/translate
	@chmod +x bin/translate
	@xattr -d com.apple.quarantine bin/translate 2>/dev/null || true
	@echo "Vendored $$(file -b bin/translate)"

test:
	@./src/translate.py "Buenos días" && echo
	@./src/translate.py "The quick brown fox" && echo

package:
	@rm -f $(PKG)
	@files="info.plist bin src README.md"; [ -f icon.png ] && files="$$files icon.png"; \
		zip -r -q $(PKG) $$files -x '*.pyc' -x '*/__pycache__/*' -x '*.DS_Store'
	@echo "Built $(PKG) — double-click to import into Alfred."

clean:
	@rm -rf build $(PKG)
	@find src -name __pycache__ -type d -exec rm -rf {} +
