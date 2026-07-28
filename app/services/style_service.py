from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.style import Style
from app.repositories.style_repository import StyleRepository
from app.schemas.style import StyleCreate


class StyleService:
    def __init__(self, db: Session):
        self.repository = StyleRepository(db)

    def create_style(self, schema: StyleCreate) -> Style:
        new_style = Style(
            name = schema.name,
            description = schema.description,
            url_picture = schema.url_picture,
        )
        return self.repository.create(new_style)

    def get_styles(self) -> list[Style]:
        return self.repository.get_all()

    def get_style(self, style_id: int) -> Style:
        style = self.repository.get_by_id(style_id)

        if style is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Style not found",
            )


        # Делаем коммит. Если в твоем сервисе сессия называется self.db:
        self.repository.db.commit()
        return style

    def update_style(self, style_id: int, schema):
        style = self.repository.get_by_id(style_id)
        if not style:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Стиль не найдена")

        # Обновляем поля модели новыми значениями из схемы фронтенда
        style.name = schema.name
        style.description = schema.description
        style.url_picture = schema.url_picture

        # Сохраняем изменения в базу данных
        self.repository.db.commit()
        return {"status": "success", "message": "Данные стиля успешно обновлены"}


