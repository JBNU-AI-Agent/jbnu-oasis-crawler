# app/crawlers/score.py
from typing import List
from app.crawlers.base import BaseCrawler
from app.core.oasis_client import OasisClient

class CreditCrawler(BaseCrawler):
    async def crawl(self, std_no: str, client: OasisClient) -> List[dict]:
        url = "https://oasis.jbnu.ac.kr/uni/uni/scor/view/findCmpltScoreInq.action?version=0"
        
        # 요청 페이로드 구성 (제공해주신 값 기반)
        # strUnivCd는 단과대 코드 같은데, 일단 3000000001로 고정하거나 
        # StudentInfo에서 가져온 값을 써야 할 수도 있습니다.
        payload = client.build_payload(std_no, extra_params={
            "rType": "B1",
            "strUnivCd": "3000000001",  # 공대 코드일 가능성 높음
            "strmjDeepCourYn": "Y"
        })
        
        data = await client.fetch_xml(url, payload)
        
        if not data:
            return []
        
        return data[1:3]