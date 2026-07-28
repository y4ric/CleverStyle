from sqlalchemy.orm import Session
from app.models.style import Style


class StyleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Style]:
        return self.db.query(Style).all()

    def get_by_id(
        self,
        style_id: int,
    ) -> Style | None:

        return (
            self.db.query(Style).filter(Style.style_id == style_id).first()
        )

    def create(self, style) -> Style:
        new_style = Style(
            name=style.name,
            description=style.description,
            url_picture=style.url_picture
        )

        self.db.add(new_style)
        self.db.commit()
        self.db.refresh(new_style)
        return new_style



