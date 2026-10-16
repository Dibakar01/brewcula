# brewCula
Menu bar app that keeps a Mac awake. Single Swift file (`app/main.swift`), no dependencies.
Takes the same 4 IOPM power assertions as `caffeinate -dims`; App Sandbox with zero
entitlements + hardened runtime; ad-hoc signed, universal binary.
Name is **brewCula** (lowercase b, capital C). The user rejected "Jaago" and "Count Brewcula".

Build: `./build.sh` → `build/brewCula.app`. Self-test: `build/brewCula.app/Contents/MacOS/brewCula --check`.
App flags: `--setup` (Open at Login + welcome bubble), `--remove-login-item`, `--check`.
Art: `python3 assets/generate.py` regenerates every SVG (mascot, hero, sandbox, icon, site art) light + dark.
Style since 1.1.0: two-ink riso print (black + red on newsprint #ebe9e4), Helvetica Neue, code in mono.
`app/AppIcon.icns` is rendered from `assets/icon.svg` via headless Chrome + sips + iconutil.

## Status (2026-10-16)
Public at github.com/Dibakar01/brewcula, site on GitHub Pages. v1.0.0 shipped; v1.1.0 is the riso
redesign. Release flow: push tag `vX.Y.Z` → CI builds the zip + attestation → pin its SHA-256 and
VERSION in `install.sh` → push. React Bits sources in `site/src/bits/` are MIT + Commons Clause
(keep LICENSE.md there).

## Resuming
Full specs for every remaining step: `docs/handoff/HANDOFF.md` (gitignored). Render helpers for
visual checks: `docs/handoff/tools/`. Skills to load: ponytail:ponytail, graph-sorcerer (before
any parallel agents), design-taste-frontend (site), task-observer.
