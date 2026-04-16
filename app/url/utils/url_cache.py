import json
import os
import random
from app.database.redis import get_redis
from app.url.entities.url_entity import UrlEntity

cache_prefix = os.getenv("CACHE_PREFIX", "url:redirect:")
cache_replicas = int(os.getenv("CACHE_REPLICAS", 5))
cache_hot_key_threshold = int(os.getenv("HOT_KEY_THRESHOLD", 100))
cache_url_access_count = os.getenv("CACHE_URL_ACCESS_COUNT")

def _build_key(short_code: str, replica: int | None = None) -> str:
    if replica:
        return f"{cache_prefix}{short_code}:{replica}"
    return f"{cache_prefix}{short_code}"


def _is_hot_key(short_code: str) -> bool:
    redis = get_redis()

    key = f"{cache_url_access_count}{short_code}"

    count = redis.incr(key)
    redis.expire(key, 60) 

    return count > cache_hot_key_threshold


def get_cached_url(short_code: str) -> UrlEntity | None:
    redis = get_redis()

    # tenta chave simples primeiro
    data = redis.get(_build_key(short_code))

    if data:
        obj = json.loads(data)
        return UrlEntity(**obj)

    replica = random.randint(1, cache_replicas)
    key = _build_key(short_code, replica)

    data = redis.get(key)

    if not data:
        return None

    obj = json.loads(data)

    return UrlEntity(**obj)


def cache_url(url: UrlEntity, short_code: str) -> None:
    redis = get_redis()

    is_hot = _is_hot_key(short_code)

    payload = json.dumps({
        "short_code": url.short_code,
        "original_url": url.original_url,
        "created_at": url.created_at.isoformat()
    })

    if is_hot:
        # sharding (hot key)
        for replica in range(1, cache_replicas + 1):
            redis.set(
                _build_key(short_code, replica),
                payload,
                ex=3600
            )
    else:
        # chave simples
        redis.set(
            _build_key(short_code),
            payload,
            ex=3600
        )