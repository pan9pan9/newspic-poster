# 🧠 Newspick Poster

**Newspick Poster**는 뉴스픽 파트너 페이지에서 인기 콘텐츠를 자동으로 수집하고, Threads 플랫폼에 이미지 카드와 링크를 자동으로 업로드하는 파이썬 기반 자동화 도구입니다.  
> Playwright를 활용한 웹 크롤링 + Threads Graph API를 활용한 자동 게시 시스템

---

## 📌 주요 기능

- ✅ 뉴스픽 파트너 페이지 자동 로그인
- ✅ 기사 제목, 대표 이미지, 기사 링크 자동 수집
- ✅ Threads에 카드형 게시물 업로드 + 댓글로 링크 연결

---

## 🔧 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/pan9pan9/newspick-poster.git
cd newspick-poster
```

### 2. 가상환경 설정 (추천)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. 필수 패키지 설치

```bash
pip install -r requirements.txt
```

---

## 🔐 환경변수 설정

`.env` 파일을 루트 디렉토리에 생성하고 아래처럼 입력하세요:

```env
APP_ID=your_app_id
APP_SECRET=your_app_secret
ACCESS_TOKEN=your_threads_access_token
NEWSPICK_ID=your_newspick_login_id
NEWSPICK_PW=your_newspick_login_pw
THREADUSER_ID=your_threads_user_id
```

> 만약 git을 이용하시면 `.env` 파일은 반드시 `.gitignore`에 포함시켜야 합니다.

---

## 🚀 실행 방법

```bash
python main.py
```

- Playwright가 Chromium 브라우저를 열어 자동 로그인 및 크롤링을 수행합니다.
- 제목과 대표 이미지로 Threads에 카드 게시물을 업로드합니다.
- 각 카드 게시물에 기사 링크를 댓글로 추가합니다.

---

## 📁 프로젝트 구조 예시

```
newspick-poster/
├── newspick.py              # 메인 실행 파일 (크롤링 + Threads API 호출)
├── .env                 # 환경 변수 설정 파일 (비공개)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧰 기술 스택

- Python 3.10+
- Playwright (웹 자동화)
- python-dotenv (환경변수 관리)
- Threads Graph API (게시 및 댓글 자동화)
- requests, asyncio 등

---

## ⚠️ 주의사항

- 최초 실행 시 Playwright가 Chromium을 다운로드하므로 시간이 다소 걸릴 수 있습니다.
- Threads API의 access token과 user ID는 정확히 설정해야 하며, 게시 권한이 있어야 합니다.
- 하루에 과도한 게시 요청 시 Threads 측에서 차단될 수 있습니다.

---

## 📝 라이선스

MIT License © 2025 [pan9pan9](https://github.com/pan9pan9)
