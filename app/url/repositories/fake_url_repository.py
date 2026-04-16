from app.url.repositories.interfaces.ulr_repository_interface import UrlRepositoryInterface
from app.url.entities.url_entity import UrlEntity
from typing import List, TypedDict

class UrlStats(TypedDict):
    short_code: str
    clicks: int


class FakeUlrRepository(UrlRepositoryInterface):
    
    def __init__(self):
        self.urls: List[UrlEntity] = []
        self.url_clicks: List[UrlStats] = []
        
    def save(self, url) -> None:
        return self.urls.append(url)
    
    def find_by_code(self, short_code) -> UrlEntity | None:
        return next((x for x in self.urls if x.short_code == short_code), None)
    
    def increment_click(self, short_code) -> None:
        stat = next((x for x in self.url_clicks if x.short_code == short_code), None)

        if not stat:
            self.url_clicks.append({
                "short_code": short_code,
                "clicks": 1
            })
            return

        stat["clicks"] += 1