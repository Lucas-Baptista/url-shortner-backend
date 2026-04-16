from fastapi import APIRouter, Depends

from app.url.dtos.url_dto import CreateUrlRequestDTO, CreateUrlResponseDTO
from app.url.services.url_service import UrlService
from app.url.dependencies import get_url_service

from fastapi.responses import RedirectResponse
from fastapi import HTTPException


router = APIRouter(
    tags=["URL"]
)


@router.post("/shorten", response_model=CreateUrlResponseDTO, status_code=201)
def create_short_url(
    data: CreateUrlRequestDTO,
    service: UrlService = Depends(get_url_service)
):
    url = service.create_short_url(data.original_url)

    return CreateUrlResponseDTO(
        short_code=url.short_code,
        original_url=url.original_url,
        created_at=url.created_at
    )
    
@router.get("/{short_code}")
def redirect(
    short_code: str,
    service: UrlService = Depends(get_url_service)
):
    url = service.get_original_url(short_code)

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url.original_url, status_code=307)