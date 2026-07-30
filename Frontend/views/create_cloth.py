import requests
import streamlit as st

# Импортируем новую функцию создания одежды из api.client
from api.client import create_cloth, get_error_message
from auth.state import require_admin

require_admin()
st.header("Добавление новой одежды")

# Создаем форму для ввода данных (убрали описание)
with st.form("create_cloth_form"):
    name = st.text_input("Название вещи (например: Белая базовая футболка)")

    # Удобные выпадающие списки для категорий и стилей
    category = st.selectbox(
        "Категория",
        ["Верх", "Низ", "Обувь", "Верхняя одежда", "Аксессуары"]
    )

    style = st.selectbox(
        "Стиль одежды",
        ["Casual", "Old Money", "Streetwear", "Business Casual"]
    )

    color = st.text_input("Цвет вещи (например: Белый)")
    url_picture = st.text_input("Ссылка на изображение (URL)")

    submitted = st.form_submit_button("Добавить в базу")

if submitted:
    # Валидация обязательных полей
    if not name.strip():
        st.error("Укажите название.")
        st.stop()
    if not color.strip():
        st.error("Укажите цвет вещи.")
        st.stop()
    if not url_picture.strip():
        st.error("Добавьте ссылку на изображение.")
        st.stop()

    # Формируем payload СТРОГО под твою модель Clothes
    payload = {
        "name": name.strip(),
        "category": category,
        "style": style,
        "color": color.strip(),
        "url_picture": url_picture.strip()
    }

    try:
        response = create_cloth(payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.status_code in (200, 201):
        created_cloth = response.json()
        st.success("Вещь успешно добавлена в базу данных SQLite!")

        # Сохраняем ID созданной вещи и перенаправляем на страницу подробностей
        st.session_state["selected_clothes_id"] = created_cloth["clothes_id"]
        st.switch_page("views/cloth_details.py")
    else:
        st.error(get_error_message(response))
