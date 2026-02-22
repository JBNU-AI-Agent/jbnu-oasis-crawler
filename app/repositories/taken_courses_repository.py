from typing import List, Any, Optional
from datetime import datetime, timezone
from fastapi import Depends
from app.core.mongodb import get_mongo_db
from app.schemas.crawler import ScoreItem

class TakenCoursesRepository:
    def __init__(self, db: Any = Depends(get_mongo_db)):
        self.db = db
        self.collection = db["courses"]

    async def create_indexes(self):
        """
        std_no에 인덱스를 생성합니다. (앱 시작 시 한 번만 호출하면 됨)
        """
        # std_no를 기준으로 오름차순(1) 정렬, 유니크 제약조건 설정
        await self.collection.create_index("std_no", unique=True)
    
    async def save_courses(self, std_no: str, data: List[ScoreItem]):
        """수강 과목 정보 저장"""
        
        serialized_data = [item.model_dump() for item in data]
        
        document = {
            "std_no": std_no,
            "data": serialized_data,
            "updated_at": datetime.now(timezone.utc)
        }
        
        await self.collection.update_one(
            {"std_no": std_no},
            {"$set": document},
            upsert=True
        )
    
    async def get_courses(self, std_no: str) -> Optional[List[ScoreItem]]:
        """수강 과목 정보 조회"""
        doc = await self.collection.find_one({"std_no": std_no}, {"_id": 0})
        
        # 조회된 문서가 아예 없을시 None반환
        if doc is None:
            return None
            
        raw_data = doc.get("data", [])
        
        return [ScoreItem.model_validate(item) for item in raw_data]