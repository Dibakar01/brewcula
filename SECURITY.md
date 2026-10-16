# Security

## Reporting

Report vulnerabilities through
[GitHub's private advisory form](../../security/advisories/new), or by email to
the address on the repository owner's profile. Please do not open a public issue
for anything exploitable.

## What the app can touch

Worth stating plainly, because it is very little, and macOS enforces it:

- **App Sandbox, nothing granted.** The only entitlement is the sandbox itself
  (`codesign -d --entitlements - brewCula.app` prints it). No network, no files
  outside its own empty container, no Apple Events, no camera, no microphone.
- **No child processes.** It does not run `caffeinate` or a shell. It asks IOKit
  for four power assertions and releases them when you click again, quit, or it
  crashes (macOS drops them with the process).
- **No data.** Nothing is collected, stored, or sent. There is no analytics and
  no update check.
- **One optional login item**, registered through `SMAppService.mainApp`. macOS
  shows a notice when it is added and lists it under System Settings › General ›
  Login Items, where you can remove it. The app's menu has the same switch.

## The installer

- Downloads one file over HTTPS only (`--proto '=https' --tlsv1.2`).
- Refuses to install unless its SHA-256 matches the value pinned in `install.sh`,
  and unless the app's code signature verifies.
- Never uses `sudo`. Writes only to `~/Applications` (or `$BREWCULA_DEST`, used to test it)
  and a temporary folder it deletes. The app itself adds one login item, which you can
  turn off, and macOS gives it an empty sandbox folder in `~/Library/Containers`.
- Release zips are built by GitHub Actions from the tagged source, never on a
  laptop, and carry a build-provenance attestation:
  `gh attestation verify brewCula-<version>.zip --repo Dibakar01/brewcula`.
  Every action in the workflows is pinned to a commit SHA. Only the release job (on a
  tag) and the Pages deploy job (on main) get write permissions.

## Known limits

- **Ad-hoc signed, not notarized.** Notarization needs a paid Apple Developer
  account. `curl` does not set the quarantine flag, so the installer opens the
  app without a Gatekeeper prompt; the pinned checksum is what guards it. A zip
  downloaded in a browser is blocked once by Gatekeeper (Privacy & Security ›
  Open Anyway).
- **`curl | sh` trusts GitHub and this repository's `main` branch.** If that is
  more trust than you want to extend, read `install.sh` first, or build from
  source with `./build.sh` (Xcode Command Line Tools, no dependencies).
