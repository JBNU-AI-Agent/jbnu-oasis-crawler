from app.core.oasis_client import OasisClient
from app.crawlers.base import BaseCrawler
from fastapi import Depends
from app.core.mongodb import get_mongo_db
from app.repositories.credit_repository import CreditRepository
from app.repositories.student_info_repository import StudentInfoRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.crawler import CreditResponse

class OasisService:
    def __init__(
        self, client: OasisClient = Depends(),
        db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
        self.client = client
        self.credit_repo = CreditRepository(db)
        self.student_repo = StudentInfoRepository(db)
        
    async def login_and_get_cookies(self, user_id: str, user_pw: str, otp: str) -> dict | None:
        """로그인 비즈니스 로직"""
        # 복잡한 과정은 client.authenticate 안에 다 숨겨져 있습니다.
        cookies = await self.client.authenticate(user_id, user_pw, otp)
        return cookies

    async def crawl_student_data(self, cookies: dict, crawler: BaseCrawler, std_no: str):
        """데이터 수집 로직"""
        self.client.session.cookies.update(cookies) # 쿠키 복구
        
        return await crawler.crawl(std_no, self.client)
    
    # --- [1] 동기화 (Sync): 크롤링 후 저장만 수행 ---
    async def sync_student_info(self, cookies: dict, crawler: BaseCrawler, std_no: str):
        self.client.session.cookies.update(cookies)
        raw_data = await crawler.crawl(std_no, self.client)
        
        if raw_data:
            await self.student_repo.save_student_info(std_no, raw_data)
            return True
        return False
    
    async def sync_credits(self, cookies: dict, crawler: BaseCrawler, std_no: str):
        self.client.session.cookies.update(cookies)
        raw_data = await crawler.crawl(std_no, self.client)
        
        if raw_data:
            await self.credit_repo.save_credits(std_no, raw_data)
            return True
        return False

    # --- [2] 조회 (Read): DB에서 데이터만 가져옴 ---
    async def get_student_info_from_db(self, std_no: str):
        doc = await self.student_repo.get_student_info(std_no)
        return doc["data"] if doc else None

    async def get_credits_from_db(self, std_no: str):
        doc = await self.credit_repo.get_credits(std_no)
        return doc["data"] if doc else []