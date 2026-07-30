from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.favoutitesClothes import  AddFavouriteClothes
from app.services.favouriteClothes_service import FavouritesClothesService


router = APIRouter(
    prefix="/favouritesClothes",
    tags=["favouritesClothes"],
)

def favourite_service(
    db: Session = Depends(get_db),
) -> FavouritesClothesService:
    return FavouritesClothesService(db)
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def add_favourite(
    schema: AddFavouriteClothes,
    service: FavouritesClothesService = Depends(favourite_service),
):
    return service.add_favourite(schema, user_id=schema.user_id)

@router.get("/")
def get_favorites(
    user_id: int,
    service: FavouritesClothesService = Depends(favourite_service),
):
    return service.get_favourites(user_id=user_id)

@router.delete("/")
def remove_favourite(
    clothes_id: int,
    user_id: int,
    service: FavouritesClothesService = Depends(favourite_service),
):
    return service.remove_favourite(clothes_id=clothes_id, user_id=user_id)

