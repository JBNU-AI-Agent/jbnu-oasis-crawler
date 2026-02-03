from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime

class CreditRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["credits"]

    # [저장]
    async def save_credits(self, std_no: str, data: list):
        document = {
            "std_no": std_no,
            "data": data,
            "updated_at": datetime.now()
        }
        await self.collection.update_one(
            {"std_no": std_no},
            {"$set": document},
            upsert=True
        )
    
    # [조회] 추가된 메서드
    async def get_credits(self, std_no: str) -> dict | None:
        return await self.collection.find_one({"std_no": std_no}, {"_id": 0})