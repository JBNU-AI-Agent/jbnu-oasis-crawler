from typing import List, Any
from datetime import datetime
from fastapi import Depends
from app.core.mongodb import get_mongo_db

class CreditRepository:
    def __init__(self, db: Any = Depends(get_mongo_db)):
        self.db = db
        self.collection = db["credits"]

    async def save_credits(self, std_no: str, data: list):
        """학점 정보 저장"""
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
    
    async def get_credits(self, std_no: str) -> dict | None:
        """학점 정보 조회"""
        return await self.collection.find_one({"std_no": std_no}, {"_id": 0})