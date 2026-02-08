from pymongo import AsyncMongoClient
from app.core.config import settings

class MongoDB:
    client: AsyncMongoClient = None
    db: None

db_instance = MongoDB()

async def connect_to_mongo():
    db_instance.client = AsyncMongoClient(settings.MONGODB_URL)
    db_instance.db = db_instance.client[settings.MONGODB_DB_NAME]
    try:
        await db_instance.client.admin.command('ping')
        print("✅ MongoDB Connected! (PyMongo Native Async)")
    except Exception as e:
        print(f"❌ MongoDB Connection Error: {e}")

async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()
        print("❌ MongoDB Closed!")

# 의존성 주입용 함수
def get_mongo_db():
    return db_instance.db
