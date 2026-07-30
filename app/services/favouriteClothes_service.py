from sqlalchemy.orm import Session
from app.models.favouritesClothes import FavouritesClothes
from app.models.clothes import Clothes


class FavouritesClothesService:

    def __init__(self, db: Session):
        self.db = db

    # 1. МЕТОД ДОБАВЛЕНИЯ (Уже написан)
    def add_favourite(self, schema, user_id: int):
        favourite_record = FavouritesClothes(
            clothes_id=schema.clothes_id,
            user_id=user_id
        )
        self.db.add(favourite_record)
        self.db.commit()

        cloth = self.db.query(Clothes).filter(Clothes.clothes_id == schema.clothes_id).first()
        if cloth:
            cloth.favorites_count += 1
            self.db.commit()

        return {"status": "success", "message": "Одежда успешно добавлена в избранное"}

    # 2. МЕТОД ПОЛУЧЕНИЯ (Которого сейчас не хватает в коде!)
    def get_favourites(self, user_id: int):
        # Делаем JOIN таблиц одежды и избранного по полю clothes_id
        records = (
            self.db.query(Clothes)
            .join(FavouritesClothes, Clothes.clothes_id == FavouritesClothes.clothes_id)
            .filter(FavouritesClothes.user_id == user_id)
            .all()
        )
        return records

    # 3. МЕТОД УДАЛЕНИЯ (Для полной логики)
    def remove_favourite(self, clothes_id: int, user_id: int):
        record = self.db.query(FavouritesClothes).filter(
            FavouritesClothes.clothes_id == clothes_id,
            FavouritesClothes.user_id == user_id
        ).first()

        if record:
            self.db.delete(record)
            self.db.commit()

            cloth = self.db.query(Clothes).filter(Clothes.clothes_id == clothes_id).first()
            if cloth and cloth.favorites_count > 0:
                cloth.favorites_count -= 1
                self.db.commit()

            return {"status": "success", "message": "Успешно удалено из избранного"}

        return {"status": "error", "message": "Запись не найдена"}
