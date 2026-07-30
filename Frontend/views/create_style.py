import requests
import streamlit as st

# Импортируем функцию создания стиля и проверки ошибок
from api.client import create_style, get_error_message
from auth.state import require_admin

require_admin()
st.header("Добавление нового стиля")

# Создаем форму для ввода данных стиля
with st.form("create_style_form"):
    name = st.selectbox(
        "Название направления стиля",
        ["Casual", "Old Money", "Streetwear", "Business Casual"]
    )

    url_picture = st.text_input("Ссылка на обложку стиля (URL-картинки)")
    description = st.text_area("Философия и описание стиля (правила сочетания, особенности)")

    submitted = st.form_submit_button("Создать стиль")

if submitted:
    # Валидация обязательных полей
    if not url_picture.strip():
        st.error("Добавьте ссылку на изображение-обложку.")
        st.stop()
    if not description.strip():
        st.error("Заполните описание стиля.")
        st.stop()

    # Формируем payload СТРОГО под твою модель Style
    payload = {
        "name": name,
        "description": description.strip(),
        "url_picture": url_picture.strip()
    }

    try:
        response = create_style(payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.status_code in (200, 201):
        created_style = response.json()
        st.success("Направление стиля успешно добавлено в базу данных SQLite!")

        # Сохраняем ID созданного стиля и перенаправляем на страницу капсулы
        st.session_state["selected_style_id"] = created_style["style_id"]
        st.session_state["selected_style_name"] = created_style["name"]
        st.switch_page("views/style_details.py")
    else:
        st.error(get_error_message(response))
