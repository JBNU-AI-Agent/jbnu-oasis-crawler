from typing import List, Any
from datetime import datetime
from fastapi import Depends
from app.core.mongodb import get_mongo_db

class CreditRepository:
    def __init__(self, db: Any = Depends(get_mongo_db)):
        self.db = db
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