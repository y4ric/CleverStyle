from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Style(Base):
    __tablename__ = 'style'

    style_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String , nullable=False)

    description: Mapped[str] = mapped_column(String , nullable=False)

    url_picture: Mapped[str] = mapped_column(String, nullable=False)

