#!/bin/sh
# Builds build/brewCula.app: universal (Apple silicon + Intel), sandboxed, hardened runtime, ad-hoc signed.
# Needs only the Xcode Command Line Tools (`xcode-select --install`). No dependencies.
set -eu
cd "$(dirname "$0")"
VERSION="${VERSION:-1.0.0}"
case "$VERSION" in *[!0-9.]*|"") echo "bad VERSION: $VERSION"; exit 1;; esac
APP=build/brewCula.app
rm -rf build
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
for arch in arm64 x86_64; do
  xcrun swiftc -O -target "$arch-apple-macos11" -o "build/brewCula-$arch" app/main.swift
done
lipo -create -output "$APP/Contents/MacOS/brewCula" build/brewCula-arm64 build/brewCula-x86_64
rm build/brewCula-arm64 build/brewCula-x86_64
sed "s/__VERSION__/$VERSION/g" app/Info.plist > "$APP/Contents/Info.plist"
[ -f app/AppIcon.icns ] && cp app/AppIcon.icns "$APP/Contents/Resources/"
codesign --force --options runtime --entitlements app/brewCula.entitlements --sign - "$APP"
codesign --verify --strict "$APP"
echo "built $APP ($VERSION)"
