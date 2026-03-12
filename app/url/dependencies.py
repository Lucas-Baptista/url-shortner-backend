from fastapi import Depends

from app.url.repositories.interfaces.ulr_repository_interface import UrlRepositoryInterface
from app.url.repositories.cassandra_url_repository import CassandraUrlRepository
from app.url.services.url_service import UrlService


def get_url_repository() -> UrlRepositoryInterface:
    return CassandraUrlRepository()


def get_url_service(
    repository: UrlRepositoryInterface = Depends(get_url_repository)
) -> UrlService:
    return UrlService(repository)