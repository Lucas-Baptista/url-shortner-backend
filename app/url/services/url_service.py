from datetime import datetime

from app.url.repositories.interfaces.ulr_repository_interface import UrlRepositoryInterface
from app.url.entities.url_entity import UrlEntity
from app.url.utils.id_generator import get_next_id
from app.url.utils.short_code import decode_code

class UrlService:

    def __init__(self, repository: UrlRepositoryInterface):
        self.repository = repository
        
    def create_short_url(self, original_url: str) -> UrlEntity:
        id = get_next_id()
        
        short_code = decode_code(id)
        
        url = UrlEntity(
            short_code=short_code,
            original_url=original_url,
            created_at=datetime.now()
        )

        self.repository.save(url)

        return url
    