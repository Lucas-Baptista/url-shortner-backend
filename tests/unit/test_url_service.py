from dotenv import load_dotenv
load_dotenv()

import pytest
from datetime import datetime
from unittest.mock import patch

from app.url.services.url_service import UrlService
from app.url.entities.url_entity import UrlEntity
from app.url.repositories.fake_url_repository import FakeUlrRepository



@pytest.fixture
def fake_repository():
    return FakeUlrRepository()


@pytest.fixture
def service(fake_repository):
    return UrlService(fake_repository)


def test_create_short_url(service):

    result = service.create_short_url("https://google.com")

    assert result.short_code is not None
    assert result.original_url == "https://google.com"
    
    
from unittest.mock import patch


@patch("app.url.services.url_service.encode_id")
@patch("app.url.services.url_service.get_next_id")
def test_create_short_url_with_mocked_id(mock_get_next_id, mock_encode_id, service):
    mock_get_next_id.return_value = 123
    mock_encode_id.return_value = "abc123"

    result = service.create_short_url("https://google.com")

    assert result.short_code == "abc123"
    assert result.original_url == "https://google.com"
    
    
def test_create_short_url_saves_in_repository(service, fake_repository):
    service.create_short_url("https://google.com")

    assert len(fake_repository.urls) == 1
    assert fake_repository.urls[0].original_url == "https://google.com"
    
    
@patch("app.url.services.url_service.get_cached_url")
def test_get_original_url_from_cache(mock_cache, service):
    fake_url = UrlEntity(
        short_code="abc",
        original_url="https://google.com",
        created_at=datetime.now()
    )

    mock_cache.return_value = fake_url

    result = service.get_original_url("abc")

    assert result == fake_url
    
    
@patch("app.url.services.url_service.get_cached_url")
def test_get_original_url_increments_click_from_cache(mock_cache, service, fake_repository):
    fake_url = UrlEntity(
        short_code="abc",
        original_url="https://google.com",
        created_at=datetime.now()
    )

    mock_cache.return_value = fake_url

    service.get_original_url("abc")

    assert fake_repository.url_clicks[0]["clicks"] == 1
    
    
@patch("app.url.services.url_service.get_cached_url")
def test_get_original_url_from_repository(mock_cache, service, fake_repository):
    mock_cache.return_value = None

    url = UrlEntity(
        short_code="abc",
        original_url="https://google.com",
        created_at=datetime.now()
    )

    fake_repository.save(url)

    result = service.get_original_url("abc")

    assert result == url
    
    
@patch("app.url.services.url_service.cache_url")
@patch("app.url.services.url_service.get_cached_url")
def test_get_original_url_saves_in_cache(mock_get_cache, mock_cache_url, service, fake_repository):
    mock_get_cache.return_value = None

    url = UrlEntity(
        short_code="abc",
        original_url="https://google.com",
        created_at=datetime.now()
    )

    fake_repository.save(url)

    service.get_original_url("abc")

    mock_cache_url.assert_called_once()
    
    
@patch("app.url.services.url_service.get_cached_url")
def test_get_original_url_returns_none_when_not_found(mock_cache, service):
    mock_cache.return_value = None

    result = service.get_original_url("not-found")

    assert result is None