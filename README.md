# 끝말잇기 안드로이드 앱 (개인용)

웹으로 만든 끝말잇기를 Capacitor로 감싼 프로젝트예요. 이미 들어 있는 플러그인:

| 플러그인 | 용도 |
| --- | --- |
| @capacitor-community/speech-recognition | 마이크로 단어 말하기(음성 입력) |
| @capacitor-community/text-to-speech | 앱이 단어를 소리로 말하기(음성 출력) |

마이크 권한(RECORD_AUDIO)과 음성 서비스 조회 설정은 플러그인이 알아서 추가해요.

## 방법 1. Android Studio로 폰에 바로 설치 (가장 쉬움)

1. [Android Studio](https://developer.android.com/studio)를 설치해요. JDK와 SDK도 함께 설치돼요.
2. Android Studio에서 **Open** → 이 폴더 안의 `android` 폴더를 선택해요.
3. 처음에는 Gradle 동기화가 끝날 때까지 기다려요(몇 분). SDK 플랫폼 36 설치를 물으면 **Install**을 눌러요.
4. 폰에서 **설정 → 개발자 옵션 → USB 디버깅**을 켜고 PC에 USB로 연결해요.
5. 위쪽 기기 목록에서 폰을 고르고 ▶ **Run**을 눌러요.

## 방법 2. APK 파일만 만들기

- Android Studio: **Build → Build Bundle(s) / APK(s) → Build APK(s)**
- 명령줄: Windows는 `build-apk.bat`, macOS/Linux는 `./build-apk.sh` (JDK 21, `ANDROID_HOME` 필요)

결과 파일: `android/app/build/outputs/apk/debug/app-debug.apk`
폰으로 옮긴 뒤 열면 설치돼요. "출처를 알 수 없는 앱" 허용을 물으면 허용해 주세요.

## 방법 3. GitHub에서 자동 빌드

이 폴더를 GitHub 저장소에 올리면 `.github/workflows/build-apk.yml`이 APK를 만들어 줘요
(Actions 탭 → Build APK → Run workflow → 결과 파일 다운로드).

## 게임 화면을 고치고 싶을 때

1. `www/index.html`을 고쳐요.
2. 이 폴더에서 `npm install` (처음 한 번) → `npx cap sync android`
3. 위 방법으로 다시 빌드해요.

## 알아둘 점

- 음성 입력은 폰의 Google 음성 인식을 써요. 한국어 인식은 보통 인터넷이 필요해요.
- 음성 출력은 폰의 텍스트 음성 변환(TTS) 설정을 따라요.
- 상단의 Claude 사전 확인 스위치는 Claude 앱 안에서만 작동해서 이 앱에서는 꺼져 있어요.
  이 앱에서는 한글 두 글자 이상이면 단어로 인정해요.
- 글꼴(블랙한산스)은 인터넷이 있을 때 받아 와요. 오프라인이면 기본 글꼴로 보여요.
- 개인용 debug 빌드라 스토어 등록은 안 돼요.
