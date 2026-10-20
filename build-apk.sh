#!/usr/bin/env bash
# macOS / Linux: debug APK 만들기. JDK 21 과 Android SDK(ANDROID_HOME)가 필요해요.
set -e
cd "$(dirname "$0")/android"
if [ ! -f local.properties ] && [ -n "$ANDROID_HOME" ]; then echo "sdk.dir=$ANDROID_HOME" > local.properties; fi
chmod +x gradlew
./gradlew assembleDebug
echo
echo "APK: $(pwd)/app/build/outputs/apk/debug/app-debug.apk"
