from pydantic import BaseModel, HttpUrl
from datetime import datetime


class CreateUrlRequestDTO(BaseModel):
    original_url: HttpUrl


class CreateUrlResponseDTO(BaseModel):
    short_code: str
    original_url: HttpUrl
    created_at: datetime


class UrlRedirectResponseDTO(BaseModel):
    original_url: HttpUrl


class UrlStatsResponseDTO(BaseModel):
    short_code: str
    clicks: int