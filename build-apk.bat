@echo off
rem Windows: debug APK 만들기. JDK 21 과 Android SDK(ANDROID_HOME)가 필요해요.
cd /d "%~dp0android"
if not exist local.properties if defined ANDROID_HOME (
  setlocal
  set "P=%ANDROID_HOME:\=/%"
  echo sdk.dir=%P%> local.properties
  endlocal
)
call gradlew.bat assembleDebug
echo.
echo APK: %cd%\app\build\outputs\apk\debug\app-debug.apk
pause
