# app/crawlers/score.py
from typing import List
from app.crawlers.base import BaseCrawler
from app.core.oasis_client import OasisClient
from app.core.constants import SCORE_URL, SCORE_PAYLOAD

class CreditCrawler(BaseCrawler[List[dict]]):
    async def crawl(self, std_no: str, client: OasisClient) -> List[dict]:
        # 요청 페이로드 구성 (제공해주신 값 기반)
        # strUnivCd는 단과대 코드 같은데, 일단 3000000001로 고정하거나 
        # StudentInfo에서 가져온 값을 써야 할 수도 있습니다.
        payload = client.build_payload(std_no, extra_params=SCORE_PAYLOAD)
        
        data = await client.fetch_xml(SCORE_URL, payload)
        
        if not data:
            return []
        
        return data[1:3]