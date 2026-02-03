from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db = MongoDB()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.db = db.client[settings.MONGODB_DB_NAME]
    print("✅ MongoDB Connected!")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("❌ MongoDB Closed!")

# 의존성 주입용 함수
def get_mongo_db():
    return db.db