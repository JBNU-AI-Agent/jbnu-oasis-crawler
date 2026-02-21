from app.crawlers.base import BaseCrawler
from app.core.oasis_client import OasisClient
from app.core.constants import STD_INFO_URL
class StudentInfoCrawler(BaseCrawler):
    async def crawl(self, std_no: str, client: OasisClient):
        payload = client.build_payload(std_no, None)
        data = await client.fetch_xml(STD_INFO_URL, payload)
        
        # 리스트의 첫 번째 항목(학생 본인 정보)만 반환
        return data[0] if data else None