from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Clothes(Base):
    __tablename__ = 'clothes'

    clothes_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String , nullable=False)

    category: Mapped[str] = mapped_column(String , nullable=False)

    style: Mapped[str] = mapped_column(String , nullable=False)

    color: Mapped[str] = mapped_column(String, nullable=False)

    url_picture: Mapped[str] = mapped_column(String, nullable=False)
