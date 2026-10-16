#!/bin/sh
# brewCula installer. Read it before you run it; it is short on purpose.
#
#   curl -fsSL https://raw.githubusercontent.com/Dibakar01/brewcula/main/install.sh | sh
#
# What it does, in order:
#   1. downloads brewCula-$VERSION.zip from this repo's GitHub release, HTTPS only
#   2. stops unless the zip's SHA-256 matches the value pinned below
#   3. stops unless the app's code signature is intact
#   4. puts brewCula.app in ~/Applications (your folder, no admin password)
#   5. opens it with --setup: Open at Login on (macOS 13+), and a one-time hint under the mug
# What it never does: sudo, write outside ~/Applications and a temp folder, send anything anywhere.
# (The app then adds its own login item and macOS gives it an empty sandbox folder.)
# BREWCULA_DEST=<dir> installs somewhere else instead (used to test this script).
#
# Uninstall:
#   curl -fsSL https://raw.githubusercontent.com/Dibakar01/brewcula/main/install.sh | sh -s -- --uninstall
set -eu

# Everything runs inside main, so a download cut off mid-file runs nothing.
main() {
  VERSION="1.1.0"
  SHA256="778e1da0f9e714531974c34c84124f32d2f5546148c99463d84884d43776215b"
  URL="https://github.com/Dibakar01/brewcula/releases/download/v$VERSION/brewCula-$VERSION.zip"
  DEST="${BREWCULA_DEST:-$HOME/Applications}"
  APP="$DEST/brewCula.app"

  [ "$(uname -s)" = Darwin ] || { echo "brewCula is a macOS app."; exit 1; }

  if [ "${1:-}" = "--uninstall" ]; then
    if [ -x "$APP/Contents/MacOS/brewCula" ]; then "$APP/Contents/MacOS/brewCula" --remove-login-item || true; fi
    pkill -x brewCula 2>/dev/null || true
    rm -rf "$APP"
    echo "brewCula removed. Its empty sandbox folder stays in ~/Library/Containers until you delete it."
    exit 0
  fi

  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT

  echo "Downloading brewCula $VERSION"
  curl -fsSL --proto '=https' --tlsv1.2 -o "$tmp/brewCula.zip" "$URL"

  got=$(shasum -a 256 "$tmp/brewCula.zip" | cut -d' ' -f1)
  if [ "$got" != "$SHA256" ]; then
    echo "Checksum mismatch, nothing installed."
    echo "  expected $SHA256"
    echo "  got      $got"
    exit 1
  fi
  echo "Checksum OK"

  ditto -x -k "$tmp/brewCula.zip" "$tmp/out"
  codesign --verify --strict "$tmp/out/brewCula.app"
  echo "Signature intact"

  mkdir -p "$DEST"
  pkill -x brewCula 2>/dev/null || true
  for _ in 1 2 3 4 5 6 7 8 9 10; do pgrep -x brewCula >/dev/null || break; sleep 0.3; done  # else open fails with -600
  rm -rf "$APP"
  mv "$tmp/out/brewCula.app" "$APP"
  echo "Installed $APP"
  open "$APP" --args --setup
  echo "brewCula is in your menu bar. Click the mug to keep your Mac awake."
}

main "$@"
