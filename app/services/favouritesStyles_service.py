from app.models.favouritesStyles import FavouritesStyles
from sqlalchemy.orm import Session
from app.models.style import Style


class FavouritesStylesService:

    def __init__(self, db: Session):
        self.db = db

    # 1. МЕТОД ДОБАВЛЕНИЯ (Твой рабочий код)
    def add_favourite(self, schema, user_id):
        favourite_record = FavouritesStyles(
            style_id=schema.style_id,
            user_id=user_id
        )
        self.db.add(favourite_record)
        self.db.commit()

        style = self.db.query(Style).filter(Style.style_id == schema.style_id).first()
        if style:
            style.favorites_count += 1
            self.db.commit()

        return {"status": "success", "message": "Стиль успешно добавлен в избранное"}

    # 2. МЕТОД ПОЛУЧЕНИЯ (Исправит ошибку AttributeError)
    def get_favourites(self, user_id: int):
        # Делаем JOIN таблиц стилей и избранного, чтобы вытащить полную инфу о стилях
        records = (
            self.db.query(Style)
            .join(FavouritesStyles, Style.style_id == FavouritesStyles.style_id)
            .filter(FavouritesStyles.user_id == user_id)
            .all()
        )
        return records

    # 3. МЕТОД УДАЛЕНИЯ (С уменьшением счетчика лайков)
    def remove_favourite(self, style_id: int, user_id: int):
        # Ищем запись о лайке конкретного юзера на конкретный стиль
        record = self.db.query(FavouritesStyles).filter(
            FavouritesStyles.style_id == style_id,
            FavouritesStyles.user_id == user_id
        ).first()

        if record:
            self.db.delete(record)
            self.db.commit()

            # Уменьшаем счетчик favorites_count у самого стиля
            style = self.db.query(Style).filter(Style.style_id == style_id).first()
            if style and style.favorites_count > 0:
                style.favorites_count -= 1
                self.db.commit()

            return {"status": "success", "message": "Успешно удалено из избранного"}

        return {"status": "error", "message": "Запись не найдена"}
