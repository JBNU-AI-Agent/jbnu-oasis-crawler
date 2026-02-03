from abc import ABC, abstractmethod
from app.core.oasis_client import OasisClient
from typing import List, Dict, Optional

class BaseCrawler(ABC):
    @abstractmethod
    async def crawl(self, std_no: str, client: OasisClient) -> Optional[List[Dict[str, str]]]:
        pass