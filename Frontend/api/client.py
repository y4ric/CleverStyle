from streamlit import session_state
import requests

BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login/"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register/"
PROFILE_ENDPOINT = f"{BACKEND_URL}/users/me/"
STYLES_ENDPOINT = f"{BACKEND_URL}/styles/"
CLOTHES_ENDPOINT = f"{BACKEND_URL}/clothes/"
FAVOURITESSTYLES_ENDPOINT = f"{BACKEND_URL}/favouritesStyles/"
FAVOURITESCLOTHES_ENDPOINT = f"{BACKEND_URL}/favouritesClothes/"


# --- АВТОРИЗАЦИЯ И ПРОФИЛЬ ---

def register(email: str, password: str, full_name: str) -> requests.Response:
    data = {
        "email": email,
        "password": password,
        "full_name": full_name,
    }
    return requests.post(REGISTER_ENDPOINT, json=data)


def login(email: str, password: str) -> requests.Response:
    data = {
        "email": email,
        "password": password,
    }
    return requests.post(LOGIN_ENDPOINT, json=data)


def get_profile() -> requests.Response:
    return request_with_authorization_header("GET", PROFILE_ENDPOINT)


# --- ФУНКЦИИ ДЛЯ РАБОТЫ С ОДЕЖДОЙ (CLOTHES) ---

def get_clothes() -> requests.Response:
    """Получить весь список одежды"""
    if session_state.get("access_token"):
        return request_with_authorization_header("GET", CLOTHES_ENDPOINT)
    return requests.get(CLOTHES_ENDPOINT)


def get_cloth_by_id(clothes_id: int) -> requests.Response:
    """Получить конкретную вещь по ID"""
    endpoint = f"{CLOTHES_ENDPOINT}{clothes_id}"
    if session_state.get("access_token"):
        return request_with_authorization_header("GET", endpoint)
    return requests.get(endpoint)


def create_cloth(payload: dict) -> requests.Response:
    """Создать новую вещь (Админка)"""
    return request_with_authorization_header("POST", CLOTHES_ENDPOINT, payload=payload)


def delete_cloth(clothes_id: int) -> requests.Response:
    """Удалить вещь (Админка)"""
    endpoint = f"{CLOTHES_ENDPOINT}{clothes_id}/"
    return request_with_authorization_header("DELETE", endpoint)

def update_cloth(clothes_id: int, payload: dict) -> requests.Response:
    """Обновить данные одежды (Админка)"""
    endpoint = f"{CLOTHES_ENDPOINT}{clothes_id}/" # Путь PUT/PATCH запроса к FastAPI
    return request_with_authorization_header("PUT", endpoint, payload=payload)

# --- ФУНКЦИИ ДЛЯ ИЗБРАННОЙ ОДЕЖДЫ (FAVOURITES CLOTHES) ---

def get_favourites_clothes() -> requests.Response:
    """Получить избранную одежду пользователя"""
    user_id = session_state.get("user_id") or 1
    return request_with_authorization_header(
        "GET",
        FAVOURITESCLOTHES_ENDPOINT,
        params={"user_id": user_id}
    )


def add_favourite_cloth(clothes_id: int) -> requests.Response:
    """Добавить одежду в избранное"""
    user_id = session_state.get("user_id") or 1
    return request_with_authorization_header(
        "POST",
        FAVOURITESCLOTHES_ENDPOINT,
        payload={
            "clothes_id": clothes_id,
            "user_id": user_id
        }
    )


def remove_favourite_cloth(clothes_id: int) -> requests.Response:
    """Удалить одежду из избранного"""
    user_id = session_state.get("user_id") or 1
    endpoint = f"{FAVOURITESCLOTHES_ENDPOINT}?clothes_id={clothes_id}&user_id={user_id}"
    return request_with_authorization_header("DELETE", endpoint)


# --- ФУНКЦИИ ДЛЯ РАБОТЫ СО СТИЛЯМИ (STYLES) ---

def get_styles() -> requests.Response:
    """Получить список всех стилей"""
    if session_state.get("access_token"):
        return request_with_authorization_header("GET", STYLES_ENDPOINT)
    return requests.get(STYLES_ENDPOINT)


# --- ФУНКЦИИ ДЛЯ ИЗБРАННЫХ СТИЛЕЙ (FAVOURITES STYLES) ---

def get_favourites_styles() -> requests.Response:
    """Получить избранные стили пользователя"""
    user_id = session_state.get("user_id") or 1
    return request_with_authorization_header(
        "GET",
        FAVOURITESSTYLES_ENDPOINT,
        params={"user_id": user_id}
    )


def add_favourite_style(style_id: int) -> requests.Response:
    """Добавить стиль в избранное"""
    user_id = session_state.get("user_id") or 1
    return request_with_authorization_header(
        "POST",
        FAVOURITESSTYLES_ENDPOINT,
        payload={
            "style_id": style_id,
            "user_id": user_id
        }
    )


def remove_favourite_style(style_id: int) -> requests.Response:
    """Удалить стиль из избранного"""
    user_id = session_state.get("user_id") or 1
    endpoint = f"{FAVOURITESSTYLES_ENDPOINT}?style_id={style_id}&user_id={user_id}"
    return request_with_authorization_header("DELETE", endpoint)

def create_style(payload: dict) -> requests.Response:
    """Создать новый стиль (Админка)"""
    return request_with_authorization_header("POST", STYLES_ENDPOINT, payload=payload)
def update_style(style_id: int, payload: dict) -> requests.Response:
    """Обновить данные стиля (Админка)"""
    endpoint = f"{STYLES_ENDPOINT}{style_id}/" # Проверь, чтобы в роутере FastAPI был такой PUT/PATCH путь
    return request_with_authorization_header("PUT", endpoint, payload=payload)

# --- БАЗОВАЯ СИСТЕМНАЯ ФУНКЦИЯ ДЛЯ ЗАПРОСОВ (C ХЕДЕРАМИ АВТОРИЗАЦИИ) ---

def request_with_authorization_header(
    request_type: str,
    endpoint: str,
    params: dict | None = None,
    payload: dict | None = None,
) -> requests.Response:
    headers = {}
    if session_state.get("access_token"):
        headers["Authorization"] = f"Bearer {session_state['access_token']}"

    if request_type == "GET":
        response = requests.get(endpoint, headers=headers, params=params)
    elif request_type == "POST":
        response = requests.post(endpoint, headers=headers, params=params, json=payload)
    elif request_type == "PUT":
        response = requests.put(endpoint, headers=headers, params=params, json=payload)
    elif request_type == "PATCH":
        response = requests.patch(endpoint, headers=headers, params=params, json=payload)
    elif request_type == "DELETE":
        response = requests.delete(endpoint, headers=headers, params=params)
    else:
        raise ValueError("Неизвестный тип запроса")

    # Если JWT токен больше не действителен
    if response.status_code == 401:
        session_state.pop("access_token", None)
        session_state.pop("profile", None)

    return response


def get_error_message(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail")
        return str(detail or f"Ошибка backend: HTTP {response.status_code}")
    except ValueError:
        return f"Ошибка backend: HTTP {response.status_code}"
def create_look(payload: dict) -> requests.Response:
    """Создать новый готовый образ/лук (Админка)"""
    # Запрос улетит на эндпоинт, который мы настраивали в handlers/looks.py
    return request_with_authorization_header("POST", f"{BACKEND_URL}/looks/", payload=payload)
def link_clothes_to_look(look_id: int, clothes_id: int) -> requests.Response:
    """Привязать конкретную вещь к образу"""
    payload = {"look_id": look_id, "clothes_id": clothes_id}
    return request_with_authorization_header("POST", f"{BACKEND_URL}/looks/add-clothes/", payload=payload)
