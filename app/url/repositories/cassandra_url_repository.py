from app.database.cassandra import get_session
from app.url.repositories.interfaces.ulr_repository_interface import UrlRepositoryInterface
from app.url.entities.url_entity import UrlEntity

class CassandraUlrRepository(UrlRepositoryInterface):
    
    def __init__(self):
        self.session = get_session()
        
    def save(self, url: UrlEntity) -> UrlEntity:
        query = """
        INSERT INTO url_shortener.urls (short_code, original_url, created_at)
        VALUES (%s, %s, %s)
        """
        
        self.session.execute(
            query,
            (
                url.short_code,
                url.original_url,
                url.created_at
            )
        )
    
    def find_by_code(self, short_code: str) -> UrlEntity | None:
        
        query = """
        SELECT short_code, original_url, created_at
        FROM url_shortener.urls
        WHERE short_code = %s
        """
        
        result = self.session.execute(query, (short_code,))
        row = result.one()
        
        if not row:
            return None
        
        return UrlEntity(
            short_code=row.short_code,
            original_url=row.original_url,
            created_at=row.created_at
        )
    
    def increment_click(self, short_code) -> None:
        query = """
        UPDATE url_shortener.url_clicks
        SET clicks = clicks + 1
        WHERE short_code = %s
        """

        self.session.execute(query, (short_code,))