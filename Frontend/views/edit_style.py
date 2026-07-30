import requests
import streamlit as st

# 1. Импортируем правильные функции для работы со стилями
from api.client import get_error_message, update_style
from auth.state import require_admin


# Быстрая функция-заглушка для получения стиля по ID, если её нет в клиенте
def get_style_by_id(style_id: int) -> requests.Response:
    return requests.get(f"http://127.0.0{style_id}")


require_admin()
st.header("Редактирование направления стиля")

# Получаем ID стиля, который админ нажал редактировать
style_id = st.session_state.get("edit_style_id")  # Заменили edit_car_id на edit_style_id

if style_id is None:
    st.info("Сначала выберите стиль для редактирования.")
    st.stop()

try:
    item_response = get_style_by_id(style_id)
except requests.RequestException:
    st.error("Не удалось получить данные стиля с backend.")
    st.stop()

if not item_response.ok:
    st.error(get_error_message(item_response))
    st.stop()

item = item_response.json()
st.toast('Данные стиля успешно загружены!', icon='🎉')

# Форма редактирования строго под поля твоей модели Style
with st.form(f"edit_style_form_{style_id}"):
    # Делаем выпадающий список со значением по умолчанию, которое уже есть в базе
    available_styles = ["Casual", "Old Money", "Streetwear", "Business Casual"]
    default_index = available_styles.index(item["name"]) if item["name"] in available_styles else 0

    name = st.selectbox(
        "Название направления стиля",
        options=available_styles,
        index=default_index
    )

    url_picture = st.text_input(
        "Ссылка на обложку стиля (URL)",
        value=item.get("url_picture") or "",
    )

    description = st.text_area(
        "Философия и описание стиля",
        value=item.get("description", ""),
    )

    submitted = st.form_submit_button("Сохранить изменения")

if submitted:
    if not url_picture.strip():
        st.error("Добавьте ссылку на изображение-обложку.")
        st.stop()
    if not description.strip():
        st.error("Заполните описание стиля.")
        st.stop()

    # Формируем payload под структуру бэкенда таблицы Style
    payload = {
        "name": name,
        "description": description.strip(),
        "url_picture": url_picture.strip(),
    }

    try:
        response = update_style(style_id, payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.ok:
        st.success("Изменения успешно сохранены!")
        st.session_state["selected_style_id"] = style_id
        st.switch_page("views/style_details.py")  # Перекидываем обратно на страницу деталей стиля
    else:
        st.error(get_error_message(response))
