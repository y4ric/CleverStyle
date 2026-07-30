import uvicorn
from fastapi import FastAPI

from app.config.config import get_settings
from app.database import Base, engine
from app.handlers.auth import router as auth_router
from app.handlers.style import router as style_router
from app.handlers.users import router as users_router
from app.handlers.clothes import router as clothes_router
#from app.handlers.favourite import router as favourite_router
from app.handlers.favouritesStyles import router as favourites_styles_router
from app.handlers.favouritesClothes import router as favourites_clothes_router
# В блоке импортов вверху файла:
from app.handlers.looks import router as looks_router

# Ниже, где у тебя подключаются другие роутеры (app.include_router):


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(style_router)
app.include_router(clothes_router)
app.include_router(users_router)
app.include_router(favourites_styles_router)
app.include_router(favourites_clothes_router)
app.include_router(looks_router)

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
