from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

# 1. Таблица самого ОБРАЗА (твоя модель)
class Look(Base):
    __tablename__ = 'looks'

    look_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    style_id: Mapped[int] = mapped_column(Integer, nullable=False)
    url_picture: Mapped[str] = mapped_column(String, nullable=False)


# 2. Таблица СВЯЗИ образа и одежды (добавили сюда, чтобы не создавать новый файл!)
class LookClothes(Base):
    __tablename__ = 'look_clothes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    look_id: Mapped[int] = mapped_column(Integer, nullable=False)
    clothes_id: Mapped[int] = mapped_column(Integer, nullable=False)
