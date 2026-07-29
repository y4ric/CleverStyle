from sqlalchemy.orm import Session
from app.models.clothes import Clothes


class ClothesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Clothes]:
        return self.db.query(Clothes).all()

    def get_by_id(
        self,
        clothes_id: int,
    ) -> Clothes | None:

        return (
            self.db.query(Clothes).filter(Clothes.clothes_id == clothes_id).first()
        )

    def create(self, clothes) -> Clothes:
        new_clothes = Clothes(
            name=clothes.name,
            category=clothes.category,
            style=clothes.style,
            color=clothes.color,
            url_picture=clothes.url_picture
        )

        self.db.add(new_clothes)
        self.db.commit()
        self.db.refresh(new_clothes)
        return new_clothes



