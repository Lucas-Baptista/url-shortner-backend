from datetime import datetime

from app.url.repositories.interfaces.ulr_repository_interface import UrlRepositoryInterface
from app.url.entities.url_entity import UrlEntity
from app.url.utils.id_generator import get_next_id
from app.url.utils.short_code import encode_id

class UrlService:

    def __init__(self, repository: UrlRepositoryInterface):
        self.repository = repository
        
    def create_short_url(self, original_url: str) -> UrlEntity:
        id = get_next_id()
        
        print(id)
        
        short_code = encode_id(id)
        
        print("short_code:", short_code)
        
        url = UrlEntity(
            short_code=short_code,
            original_url=str(original_url),
            created_at=datetime.now()
        )
        
        print("url: ", url)

        self.repository.save(url)

        return url
    