# brewCula
Menu bar app that keeps a Mac awake. Single Swift file (`app/main.swift`), no dependencies.
Takes the same 4 IOPM power assertions as `caffeinate -dims`; App Sandbox with zero
entitlements + hardened runtime; ad-hoc signed, universal binary.
Name is **brewCula** (lowercase b, capital C). The user rejected "Jaago" and "Count Brewcula".

Build: `./build.sh` → `build/brewCula.app`. Self-test: `build/brewCula.app/Contents/MacOS/brewCula --check`.
App flags: `--setup` (Open at Login + welcome bubble), `--remove-login-item`, `--check`.
Art: `python3 assets/generate.py` regenerates every SVG (mascot, hero, sandbox, icon) light + dark.
`app/AppIcon.icns` is rendered from `assets/icon.svg` via headless Chrome + sips + iconutil.

## Status (2026-10-16)
Done and verified locally: app, menu bar icon, Open at Login (live-tested), welcome bubble, all art
(`assets/generate.py`), icns, `install.sh` (end-to-end tested against a local zip), CI workflow
`.github/workflows/build.yml` (not yet run on GitHub), README, SECURITY.md, LICENSE, CHANGELOG.
React Bits sources reviewed and saved in `site/src/bits/` (MIT + Commons Clause, keep LICENSE.md there).
Left: landing site in `site/` + Pages workflow; independent security review; publish
(`gh repo create Dibakar01/brewcula --public`, tag v1.0.0, pin SHA-256, enable Pages, e2e install).

## Resuming
Full specs for every remaining step: `docs/handoff/HANDOFF.md` (gitignored). Render helpers for
visual checks: `docs/handoff/tools/`. Skills to load: ponytail:ponytail, graph-sorcerer (before
any parallel agents), design-taste-frontend (site), task-observer.
