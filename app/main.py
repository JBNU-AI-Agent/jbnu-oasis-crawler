from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.mongodb import connect_to_mongo, close_mongo_connection
from app.utils import setup_logging
from app.middleware import LoggingMiddleware
from app.routers import crawler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시: DB 연결
    await connect_to_mongo()
    yield
    # 종료 시: 연결 해제
    await close_mongo_connection()

def create_app() -> FastAPI:
    # 로깅 초기화
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan
    )

    # 미들웨어 등록 (역순으로 실행됨)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # 라우터 등록
    app.include_router(crawler.router, prefix="/oasis", tags=["oasis-crawler"])
    # 예외 핸들러 등록

    return app

app = create_app()

@app.get("/")
def read_root():
    return {"Hello": "World"}
