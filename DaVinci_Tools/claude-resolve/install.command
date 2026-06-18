#!/bin/bash
# Claude Resolve - double-click installer launcher for macOS.
# Opens in Terminal and hands off to install.sh.
cd "$(dirname "$0")" || exit 1

# A ZIP/web download can strip the executable bit, which makes Finder refuse to
# run this on double-click. Restore +x on both the launcher and the installer
# so this run (when started via `bash install.command`) and future double-clicks
# both work, regardless of how the files arrived.
chmod +x ./install.command ./install.sh 2>/dev/null || true

bash ./install.sh
