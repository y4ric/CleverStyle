from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.style import  StyleCreate ,StyleResponse
from app.services.style_service import StyleService


router = APIRouter(
    prefix="/styles",
    tags=["styles"],
)

def get_style_service(
    db: Session = Depends(get_db),
) -> StyleService:
    return StyleService(db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_style(
    schema: StyleCreate,
    service: StyleService = Depends(get_style_service),
):
    return service.create_style(schema)

@router.get(
    "/{style_id}",
    response_model=StyleResponse,
)
def get_style(
    style_id: int,
    service: StyleService = Depends(get_style_service),
):
    return service.get_style(style_id)

@router.get(
    "/",
    response_model=list[StyleResponse],
)
def get_styles(
    service: StyleService = Depends(get_style_service),
):
    return service.get_styles()
@router.put("/{style_id}")
def update_style(
    style_id: int,
    schema: StyleCreate,  # или ваша специальная схема для обновления, например CarUpdate
    service: StyleService = Depends(get_style_service),
):
    return service.update_style(style_id, schema)
