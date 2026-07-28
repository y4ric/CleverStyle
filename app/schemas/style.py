from pydantic import BaseModel, ConfigDict, Field

class StyleCreate(BaseModel):
    name: str = Field(default=None, min_length=1, max_length=200)
    description: str = Field(default=None, min_length=1, max_length=200)
    url_picture: str = Field(default=None, min_length=1, max_length=1000)


class StyleResponse(BaseModel):
    style_id: int
    name: str
    description: str | None = None
    url_picture: str | None = None

    class Config:
        from_attributes = True