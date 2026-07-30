from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.favoutitesStyles import  AddFavouriteStyles
from app.services.favouritesStyles_service import FavouritesStylesService


router = APIRouter(
    prefix="/favouritesStyles",
    tags=["favouritesStyles"],
)

def favourite_service(
    db: Session = Depends(get_db),
) -> FavouritesStylesService:
    return FavouritesStylesService(db)
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def add_favourite(
    schema: AddFavouriteStyles,
    service: FavouritesStylesService = Depends(favourite_service),
):
    return service.add_favourite(schema, user_id=schema.user_id)

@router.get("/")
def get_favorites(
    user_id: int,
    service: FavouritesStylesService = Depends(favourite_service),
):
    return service.get_favourites(user_id=user_id)

@router.delete("/")
def remove_favourite(
    style_id: int,
    user_id: int,
    service: FavouritesStylesService = Depends(favourite_service),
):
    return service.remove_favourite(style_id=style_id, user_id=user_id)

