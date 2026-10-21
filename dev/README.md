# dev/ — 끝말잇기 개발 소스

`www/index.html`은 빌드 산출물입니다. 수정은 이 폴더의 소스에서 하고 다시 빌드합니다.

| 파일 | 역할 |
|---|---|
| part1.html | CSS / head |
| part2_logic.html | 순수 게임 로직 (단어목록, 두음법칙, 연결 검사, 컴퓨터 단어 선택) |
| part3.html | HTML 본문 + UI 스크립트 |
| dict/stdict_nouns.txt | 표준국어대사전 일반어 명사 212,632개 (CC BY-SA 2.0 KR, 출처는 dict/NOTICE.md) |
| build.js | 위 3개와 사전을 합쳐 HTML 생성 (사전은 `<script id="dict">`로 내장) |
| test_logic.js | 로직 검사: `node test_logic.js <생성된 html>` |
| ui_test.py | Playwright UI 테스트(타이머·사전 메시지·출처창): `python3 ui_test.py <html> <출력폴더>` |
| shot.py, native_test.py | Playwright 화면/네이티브 스텁 테스트 (아래 주의 참고) |

## 빌드 절차
1. `cd dev && node build.js` → `dev/kkeutmal-app/www/index.html` 생성 (`kkeutmal.html`, `끝말잇기.html`도 생성됨)
2. 생성된 `dev/kkeutmal-app/www/index.html`을 저장소 루트 `www/index.html`로 복사
3. 저장소 루트에서 `npm run sync`, 승인 후 main에 push → GitHub Actions가 APK 빌드

## 주의
- `build.js`의 출력 경로(`kkeutmal-app/www/`)는 저장소 구조(루트 `www/`)와 다릅니다. 위 2단계 복사가 필요합니다.
- `shot.py`, `native_test.py`에는 이전 작업 환경의 임시 경로(file:///tmp/...)가 하드코딩되어 있습니다. 사용 전 경로를 바꾸세요.
- 생성물(`kkeutmal.html`, `끝말잇기.html`, `kkeutmal-app/`)은 `dev/.gitignore`로 제외합니다.
- 이 폴더의 파일은 백업 V1 `src_dev/`와 SHA-256이 동일합니다.
- 사전을 내장하므로 `index.html`이 약 2.2MB 커집니다. 사전 데이터는 CC BY-SA 2.0 KR 동일조건 적용 대상이며, 저장소가 공개이므로 `dict/NOTICE.md`를 유지해야 합니다.
- 이 폴더의 `build.js`·`part*.html`은 V1 `src_dev/`와 더 이상 동일하지 않습니다(FIX-01/02, 사전 반영).
