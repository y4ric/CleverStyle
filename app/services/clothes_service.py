from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from unicodedata import category

from app.models.clothes import Clothes
from app.repositories.clothes_repository import ClothesRepository
from app.schemas.clothes import ClothesCreate


class ClothesService:
    def __init__(self, db: Session):
        self.repository = ClothesRepository(db)

    def create_cloth(self, schema: ClothesCreate) -> Clothes:
        new_clothes = Clothes(
            name = schema.name,
            category = schema.category,
            style = schema.style,
            color = schema.color,
            url_picture = schema.url_picture,
        )
        return self.repository.create(new_clothes)

    def get_clothes(self) -> list[Clothes]:
        return self.repository.get_all()

    def get_cloth(self, clothes_id: int) -> Clothes:
        clothes = self.repository.get_by_id(clothes_id)

        if clothes is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clothes not found",
            )


        # Делаем коммит. Если в твоем сервисе сессия называется self.db:
        self.repository.db.commit()
        return clothes

    def update_clothes(self, clothes_id: int, schema):
        clothes = self.repository.get_by_id(clothes_id)
        if not clothes:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Одежда не найдена")

        # Обновляем поля модели новыми значениями из схемы фронтенда
        clothes.name = schema.name
        clothes.category = schema.category
        clothes.style = schema.style
        clothes.color = schema.color
        clothes.url_picture = schema.url_picture

        # Сохраняем изменения в базу данных
        self.repository.db.commit()
        return {"status": "success", "message": "Данные одежды успешно обновлены"}


