from abc import ABC, abstractmethod
from app.url.entities.url_entity import UrlEntity


class UrlRepositoryInterface(ABC):

    @abstractmethod
    def save(self, url: UrlEntity) -> None:
        pass

    @abstractmethod
    def find_by_code(self, short_code: str) -> UrlEntity | None:
        pass

    @abstractmethod
    def increment_click(self, short_code: str) -> None:
        pass