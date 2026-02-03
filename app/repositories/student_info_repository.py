from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from datetime import datetime

class StudentInfoRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["students"] # 컬렉션 이름 분리

    # [저장]
    async def save_student_info(self, std_no: str, data: dict):
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
        return await self.collection.find_one({"std_no": std_no}, {"_id": 0})