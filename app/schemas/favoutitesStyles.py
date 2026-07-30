from pydantic import BaseModel, ConfigDict, Field

class AddFavouriteStyles(BaseModel):
    style_id: int = Field()
    user_id: int = Field()


class FavouriteStylesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    style_id: int
    user_id: int