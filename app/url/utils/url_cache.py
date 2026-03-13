import json
from app.database.redis import get_redis
from app.url.entities.url_entity import UrlEntity

CACHE_PREFIX = "url:redirect:"


def get_cached_url(short_code: str) -> UrlEntity | None:
    redis = get_redis()

    data = redis.get(CACHE_PREFIX + short_code)

    if not data:
        return None

    obj = json.loads(data)

    return UrlEntity(**obj)


def cache_url(url: UrlEntity) -> None:
    redis = get_redis()

    redis.set(
        CACHE_PREFIX + url.short_code,
        json.dumps({
            "short_code": url.short_code,
            "original_url": url.original_url,
            "created_at": url.created_at.isoformat()
        }),
        ex=3600
    )