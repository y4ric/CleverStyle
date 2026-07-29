from pydantic import BaseModel, ConfigDict, Field

class ClothesCreate(BaseModel):
    name: str = Field(default=None, min_length=1, max_length=200)
    category : str = Field(default=None, min_length=1, max_length=200)
    style : str = Field(default=None, min_length=1, max_length=200)
    color : str = Field(default=None, min_length=1, max_length=200)
    url_picture: str = Field(default=None, min_length=1, max_length=1000)


class ClothesResponse(BaseModel):
    clothes_id: int
    name: str
    category: str
    style: str
    color: str
    url_picture: str | None = None

    class Config:
        from_attributes = True