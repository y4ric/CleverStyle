from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class FavouritesClothes(Base):
    __tablename__ = "favouritesClothes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    clothes_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)