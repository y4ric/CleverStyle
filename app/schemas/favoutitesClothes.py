from pydantic import BaseModel, ConfigDict, Field

class AddFavouriteClothes(BaseModel):
    clothes_id: int = Field()
    user_id: int = Field()


class FavouriteClothResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    clothes_id: int
    user_id: int