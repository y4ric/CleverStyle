from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db  # Проверь путь к твоей функции get_db

# Импортируем модели SQLAlchemy
from app.models.style import Style
from app.models.look import Look , LookClothes
from app.models.clothes import Clothes

router = APIRouter(tags=["Looks & Capsules"])


# 1. ЭНДПОИНТ: Получить все ОБРАЗЫ для конкретного СТИЛЯ
# Именно его вызывает фронтенд на странице views/style_details.py
@router.get("/styles/{style_id}/looks/")
def get_looks_by_style(style_id: int, db: Session = Depends(get_db)):
    # Проверяем, существует ли вообще такой стиль в базе
    style_exists = db.query(Style).filter(Style.style_id == style_id).first()
    if not style_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный стиль не найден"
        )

    # Ищем все луки, у которых style_id совпадает с запрошенным
    looks = db.query(Look).filter(Look.style_id == style_id).all()
    return looks


# 2. ЭНДПОИНТ: Получить всю ОДЕЖДУ, которая входит в конкретный ОБРАЗ
# Именно его вызывает фронтенд на странице views/look_details.py
@router.get("/looks/{look_id}/clothes/")
def get_clothes_for_look(look_id: int, db: Session = Depends(get_db)):
    # Проверяем, существует ли такой образ
    look_exists = db.query(Look).filter(Look.look_id == look_id).first()
    if not look_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный образ не найден"
        )

    # Делаем мощный JOIN: берем Одежду, соединяем её с таблицей связей look_clothes
    # по полю clothes_id и фильтруем по нужному нам look_id
    clothes_in_look = (
        db.query(Clothes)
        .join(LookClothes, Clothes.clothes_id == LookClothes.clothes_id)
        .filter(LookClothes.look_id == look_id)
        .all()
    )
    return clothes_in_look
# Не забудь импортировать Pydantic-схему для создания, если используешь валидацию,
# либо временно прими данные как dict/BaseModel. Вот простой вариант:
from pydantic import BaseModel

class LookCreateSchema(BaseModel):
    name: str
    style_id: int
    url_picture: str

@router.post("/looks/")
def create_new_look(schema: LookCreateSchema, db: Session = Depends(get_db)):
    new_look = Look(
        name=schema.name,
        style_id=schema.style_id,
        url_picture=schema.url_picture
    )
    db.add(new_look)
    db.commit()
    db.refresh(new_look)
    return new_look


from pydantic import BaseModel


# Схема для получения данных с фронтенда
class LinkClothesSchema(BaseModel):
    look_id: int
    clothes_id: int


@router.post("/looks/add-clothes/")
def add_clothes_to_look(schema: LinkClothesSchema, db: Session = Depends(get_db)):
    # Проверяем, нет ли уже такой шмотки в этом образе, чтобы не дублировать
    exists = db.query(LookClothes).filter(
        LookClothes.look_id == schema.look_id,
        LookClothes.clothes_id == schema.clothes_id
    ).first()

    if exists:
        return {"status": "info", "message": "Эта вещь уже есть в образе"}

    # Создаем новую запись в таблице связей
    new_link = LookClothes(
        look_id=schema.look_id,
        clothes_id=schema.clothes_id
    )
    db.add(new_link)
    db.commit()
    return {"status": "success", "message": "Вещь успешно добавлена в образ"}
