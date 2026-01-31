# FastAPI Layered Architecture Template

FastAPI를 사용한 클린 아키텍처 템플릿입니다. 레이어 분리, 의존성 주입, 예외 처리 등 모범 사례를 적용했습니다.

## 🏗️ 아키텍처

```
app/
├── api/                # Presentation Layer
│   ├── routers/        # API 엔드포인트
│   └── dependencies.py # 의존성 주입
├── services/           # Business Logic Layer
├── repositories/       # Data Access Layer
├── models/             # Database Models (SQLAlchemy ORM)
├── schemas/            # Pydantic Schemas (DTO)
├── core/               # 핵심 설정
│   ├── config.py       # 환경 설정
│   └── database.py     # DB 연결
├── middleware/         # HTTP 미들웨어
│   └── logging_middleware.py
├── utils/              # 유틸리티
│   └── logging.py      # 로깅 설정
├── exceptions/         # Custom Exceptions & Handlers
└── main.py             # Application Entry Point
```

## ✨ 주요 특징

- **레이어 분리**: API, Service, Repository 레이어로 명확히 분리
- **의존성 주입**: FastAPI의 Depends를 활용한 DI 패턴
- **예외 처리**: 커스텀 예외와 전역 예외 핸들러
- **타입 안정성**: Pydantic을 통한 요청/응답 검증
- **환경 설정**: 환경변수를 통한 설정 관리
- **로깅 시스템**: 요청/응답 자동 로깅 미들웨어
- **CORS 지원**: 환경변수로 설정 가능한 CORS
- **Docker 지원**: Dockerfile 포함

## 📋 요구사항

- Python 3.12+
- FastAPI
- SQLAlchemy
- Pydantic v2

## 🚀 시작하기

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/fastapi-webservice.git
cd fastapi-webservice
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env` 파일을 생성하고 필요한 설정을 추가합니다:

```bash
cp .env.example .env
```

`.env` 파일 예시:
```env
DATABASE_URL=sqlite:///./test.db
DEBUG=True
LOG_LEVEL=DEBUG
CORS_ORIGINS=["http://localhost:3000"]
```

### 5. 애플리케이션 실행

```bash
uvicorn app.main:app --reload
```

API 문서: http://localhost:8000/docs

## 🐳 Docker로 실행

```bash
docker build -t fastapi-webservice .
docker run -p 8000:8000 fastapi-webservice
```

## 📚 API 엔드포인트

### Items

- `POST /items/` - 아이템 생성
- `GET /items/` - 아이템 목록 조회 (페이지네이션)
- `GET /items/{item_id}` - 특정 아이템 조회
- `PUT /items/{item_id}` - 아이템 수정
- `DELETE /items/{item_id}` - 아이템 삭제

## 🗂️ 프로젝트 구조 설명

### API Layer (`app/api/`)
- HTTP 요청/응답 처리
- 라우팅 및 엔드포인트 정의
- 의존성 주입을 통한 서비스 연결

### Service Layer (`app/services/`)
- 비즈니스 로직 구현
- 트랜잭션 관리
- 예외 발생 및 처리

### Repository Layer (`app/repositories/`)
- 데이터베이스 쿼리
- ORM 작업
- 데이터 접근 추상화

### Models (`app/models/`)
- SQLAlchemy ORM 모델
- 데이터베이스 테이블 정의

### Schemas (`app/schemas/`)
- Pydantic 모델
- 요청/응답 데이터 검증
- 직렬화/역직렬화

### Middleware (`app/middleware/`)
- HTTP 요청/응답 처리 미들웨어
- 로깅, 인증, 에러 처리 등

### Utils (`app/utils/`)
- 공통 유틸리티 함수
- 로깅 설정, 헬퍼 함수 등

## 🔧 설정

`app/core/config.py`에서 애플리케이션 설정을 관리합니다.

```python
class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Layered Architecture"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"
    LOG_LEVEL: str = "DEBUG"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
```

환경변수나 `.env` 파일로 설정을 오버라이드할 수 있습니다.

## 📝 로깅

요청/응답이 자동으로 로깅됩니다:

```
2025-01-15 10:30:00 | INFO     | → GET /items/
2025-01-15 10:30:00 | INFO     | ← 200 (12.34ms)
```

로그 레벨 설정:
```env
LOG_LEVEL=DEBUG   # 개발 환경
LOG_LEVEL=INFO    # 프로덕션 환경
LOG_LEVEL=WARNING # 경고 이상만
```

## 🌐 CORS 설정

프론트엔드 연동을 위한 CORS 설정:

```env
CORS_ORIGINS=["http://localhost:3000", "https://your-domain.com"]
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=["*"]
CORS_ALLOW_HEADERS=["*"]
```

## 🗃️ 데이터베이스

### 기본 설정
기본적으로 SQLite를 사용합니다.

### PostgreSQL 사용
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### MySQL 사용
```env
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
```

requirements.txt에 해당 드라이버를 추가해야 합니다:
- PostgreSQL: `psycopg2-binary`
- MySQL: `pymysql`

## 🧪 새로운 엔티티 추가하기

1. **Model 생성** (`app/models/your_model.py`)
2. **Schema 정의** (`app/schemas/your_schema.py`)
3. **Repository 구현** (`app/repositories/your_repository.py`)
4. **Service 작성** (`app/services/your_service.py`)
5. **Router 추가** (`app/api/routers/your_router.py`)
6. **main.py에 라우터 등록**

## 📝 개발 가이드

### 레이어 간 의존성 규칙
- API → Service → Repository → Model
- 상위 레이어만 하위 레이어를 참조
- 하위 레이어는 상위 레이어를 알지 못함

### 예외 처리
- Service 레이어에서 비즈니스 예외 발생
- `app/exceptions/`에 커스텀 예외 정의
- `handlers.py`에서 전역 핸들러 등록

## 🤝 기여

이슈와 풀 리퀘스트를 환영합니다!

## 📄 라이선스

MIT License

## 👤 작성자

Your Name - [@your_username](https://github.com/your_username)
