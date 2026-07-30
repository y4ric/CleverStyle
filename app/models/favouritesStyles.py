from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class FavouritesStyles(Base):
    __tablename__ = "favouritesStyles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    style_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)