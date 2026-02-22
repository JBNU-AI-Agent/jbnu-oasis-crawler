from abc import ABC, abstractmethod
from app.core.oasis_client import OasisClient
from typing import TypeVar, Generic, List

T = TypeVar("T")


class BaseCrawler(ABC, Generic[T]):
    @abstractmethod
    async def crawl(self, std_no: str, client: OasisClient) -> T:
        pass