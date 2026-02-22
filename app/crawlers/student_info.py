from app.crawlers.base import BaseCrawler
from app.core.oasis_client import OasisClient
from app.core.constants import STD_INFO_URL
from typing import List

class StudentInfoCrawler(BaseCrawler[dict[str, str]]):
    async def crawl(self, std_no: str, client: OasisClient) -> dict[str, str]:
        payload = client.build_payload(std_no, None)
        data = await client.fetch_xml(STD_INFO_URL, payload)
        
        if data is None:
            return {}
        
        # 리스트의 첫 번째 항목(학생 본인 정보)만 반환
        return data[0]