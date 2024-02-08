from fastapi import APIRouter, Depends
from redis import Redis
from sqlalchemy.orm import Session

from app.config.base import PREVIEW_LINK
from app.config.cache import create_redis as redis
from app.config.database import get_db
from app.schemas.preview import MenuPreview
from app.services.api.preview import PreviewService

main_router = APIRouter()


@main_router.get(
    PREVIEW_LINK,
    response_model=list[MenuPreview],
    tags=['Preview'],
    summary='Get all menus, with all submenus and all dishes'
)
def get_menus_preview(
    db: Session = Depends(get_db),
    cache: Redis = Depends(redis)
):
    result = PreviewService(db, cache).get_all()
    return result
