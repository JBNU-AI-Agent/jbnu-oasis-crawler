from typing import List, Any
from datetime import datetime
from fastapi import Depends
from app.core.mongodb import get_mongo_db

class StudentInfoRepository:
    def __init__(self, db: Any = Depends(get_mongo_db)):
        self.db = db
        self.collection = db["students"] # 컬렉션 이름 분리

    # [저장]
    async def save_student_info(self, std_no: str, data: dict):
        """학생 정보 저장"""
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
    async def get_student_info(self, std_no: str) -> dict | None:
        """학생 정보 조회"""
        return await self.collection.find_one({"std_no": std_no}, {"_id": 0})