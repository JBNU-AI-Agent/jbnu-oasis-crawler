# OASIS LMS 크롤러 서비스

이 프로젝트는 대학의 OASIS 시스템에서 학생 정보와 성적 데이터를 크롤링하고 관리하기 위해 설계된 FastAPI 기반의 백엔드 서비스입니다. 외부 OASIS 시스템의 데이터를 로컬 MongoDB 데이터베이스로 동기화하고 효율적으로 조회할 수 있는 RESTful API를 제공합니다.

## 🚀 주요 기능

- **인증 (Authentication)**: OASIS 시스템에 로그인하여 세션 쿠키를 발급받습니다.
- **학생 정보 동기화**: 학생의 개인 정보를 크롤링하여 데이터베이스에 동기화합니다.
- **성적/학점 동기화**: 학업 성적 및 학점 정보를 크롤링하여 데이터베이스에 동기화합니다.
- **데이터 조회**: MongoDB에 저장된 학생 및 성적 데이터를 빠르게 조회합니다.
- **비동기 아키텍처**: `FastAPI`와 `Motor` (비동기 MongoDB 드라이버)를 사용하여 고성능을 보장합니다.
- **계층형 아키텍처 (Layered Architecture)**: 유지보수성을 위해 라우터(Router), 서비스(Service), 리포지토리(Repository), 크롤러(Crawler) 계층으로 구조화되었습니다.

## 🛠️ 기술 스택

- **프레임워크**: [FastAPI](https://fastapi.tiangolo.com/)
- **데이터베이스**: [MongoDB](https://www.mongodb.com/)
- **ODM/드라이버**: [Motor](https://motor.readthedocs.io/) (Async), [PyMongo](https://pymongo.readthedocs.io/)
- **크롤링**: `requests`, `lxml`
- **검증**: [Pydantic](https://docs.pydantic.dev/)
- **컨테이너화**: Docker, Docker Compose

## 📂 프로젝트 구조

```bash
lms-crawler/
├── app/
│   ├── core/           # 설정 및 DB 연결
│   ├── crawlers/       # 스크래핑 로직 (Base, Student, Score)
│   ├── middleware/     # 커스텀 미들웨어 (Logging 등)
│   ├── models/         # 데이터베이스 모델
│   ├── repositories/   # DB 접근 계층
│   ├── routers/        # API 라우트 정의
│   ├── schemas/        # Pydantic 스키마 (요청/응답)
│   ├── services/       # 비즈니스 로직
│   ├── utils/          # 유틸리티 함수
│   ├── main.py         # 앱 진입점
│   └── __init__.py
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 📋 사전 요구 사항

- Python 3.12 이상
- MongoDB (로컬 또는 Atlas)
- Docker & Docker Compose (선택 사항, 컨테이너 배포 시)

## ⚙️ 설치 및 설정

### 1. 로컬 개발 환경

1.  **저장소 복제 (Clone)**
    ```bash
    git clone <repository-url>
    cd lms_cralwer
    ```

2.  **가상 환경 생성**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows의 경우: venv\Scripts\activate
    ```

3.  **의존성 설치**
    ```bash
    pip install -r requirements.txt
    ```

4.  **환경 변수 설정**
    루트 디렉토리에 `.env` 파일을 생성합니다 (`.env.example` 참고):
    ```ini
    APP_NAME="LMS Crawler"
    APP_VERSION="0.1.0"
    DEBUG=True
    
    # MongoDB 설정
    MONGODB_URL="mongodb://localhost:27017"
    MONGODB_DB_NAME="oasis_db"
    
    # 로깅 설정
    LOG_LEVEL="DEBUG"
    ```

5.  **애플리케이션 실행**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

### 2. Docker 배포

1.  위와 같이 `.env` 파일을 설정합니다.
2.  **컨테이너 빌드 및 실행**
    ```bash
    docker-compose up --build -d
    ```

API는 `http://localhost:8080`에서 접속 가능합니다.

## 🔌 API 엔드포인트

모든 엔드포인트의 기본 경로는 `/oasis`입니다.

### 인증 (Authentication)
- `POST /oasis/auth/session`: 사용자 ID, 비밀번호, OTP로 로그인하여 세션 쿠키를 획득합니다.

### 학생 정보 (Student Information)
- `POST /oasis/student/info/sync`: OASIS에서 학생 정보를 크롤링하여 DB에 동기화합니다 (쿠키 필요).
- `GET /oasis/student/info/{std_no}`: DB에 저장된 학생 정보를 조회합니다.

### 성적/학점 (Academic Credits)
- `POST /oasis/credits/sync`: OASIS에서 성적 정보를 크롤링하여 DB에 동기화합니다 (쿠키 필요).
- `GET /oasis/credits/{std_no}`: DB에 저장된 성적 정보를 조회합니다.

## 📝 사용 흐름

1.  **로그인**: `/auth/session`을 호출하여 자격 증명을 제공하고 세션 쿠키를 받습니다.
2.  **데이터 동기화**: 받은 쿠키와 학번(`std_no`)을 사용하여 `/student/info/sync` 또는 `/credits/sync`를 호출합니다. 이 과정에서 학교 포털의 데이터를 스크래핑하고 MongoDB를 업데이트합니다.
3.  **데이터 조회**: `/student/info/{std_no}` 또는 `/credits/{std_no}`를 사용하여 다시 크롤링할 필요 없이 데이터베이스에 캐시된 데이터를 즉시 조회합니다.

## 🤝 기여하기 (Contributing)

1. 이 프로젝트를 포크합니다 (Fork).
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`).
3. 변경 사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`).
4. 브랜치에 푸시합니다 (`git push origin feature/AmazingFeature`).
5. 풀 리퀘스트(Pull Request)를 엽니다.
