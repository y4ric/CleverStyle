from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.clothes import  ClothesCreate ,ClothesResponse
from app.services.clothes_service import ClothesService


router = APIRouter(
    prefix="/clothes",
    tags=["clothes"],
)

def get_style_service(
    db: Session = Depends(get_db),
) -> ClothesService:
    return ClothesService(db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_clothes(
    schema: ClothesCreate,
    service: ClothesService = Depends(get_style_service),
):
    return service.create_cloth(schema)

@router.get(
    "/{clothes_id}",
    response_model=ClothesResponse,
)
def get_cloth(
    clothes_id: int,
    service: ClothesService = Depends(get_style_service),
):
    return service.get_cloth(clothes_id)

@router.get(
    "/",
    response_model=list[ClothesResponse],
)
def get_clothes(
    service: ClothesService = Depends(get_style_service),
):
    return service.get_clothes()
@router.put("/{clothes_id}")
def update_clothes(
    clothes_id: int,
    schema: ClothesCreate,  # или ваша специальная схема для обновления, например CarUpdate
    service: ClothesService = Depends(get_style_service),
):
    return service.update_clothes(clothes_id, schema)
