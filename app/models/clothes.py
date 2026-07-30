from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base  # или твой путь к Base


class Clothes(Base):
    __tablename__ = 'clothes'

    # Убедись, что primary_key=True стоит ТОЛЬКО здесь!
    clothes_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    style: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=False)
    url_picture: Mapped[str] = mapped_column(String, nullable=False)

    # ВНИМАНИЕ: Здесь НЕ ДОЛЖНО быть primary_key=True! Только Integer и default=0
    favorites_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
