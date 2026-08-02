import requests
import streamlit as st
from api.client import create_look, get_error_message, get_styles
from auth.state import require_admin

require_admin()
st.header("Добавление готового образа (Лука)")

# Запрашиваем из базы все существующие стили, чтобы админ мог привязать образ к ним
try:
    styles_response = get_styles()
except requests.RequestException:
    st.error("Бэкенд недоступен. Проверьте запуск FastAPI.")
    st.stop()

if not styles_response.ok:
    st.error("Не удалось загрузить стили для привязки.")
    st.stop()

styles_list = styles_response.json()

if not styles_list:
    st.warning("Сначала создайте хотя бы одно направление стиля в базе данных!")
    st.stop()

# Формируем удобный список стилей для выпадающего меню {"Название": style_id}
style_options = {style["name"]: style["style_id"] for style in styles_list}

with st.form("create_look_form"):
    name = st.text_input("Название образа (например: Летний вечер в Монако)")

    # Админ выбирает текстовое название стиля, а в базу улетит его числовой ID!
    selected_style_name = st.selectbox("К какому стилю относится образ?", options=list(style_options.keys()))

    url_picture = st.text_input("Ссылка на изображение всего образа целиком (URL)")

    submitted = st.form_submit_button("Создать образ")

if submitted:
    if not name.strip():
        st.error("Укажите название образа.")
        st.stop()
    if not url_picture.strip():
        st.error("Добавьте ссылку на картинку лука.")
        st.stop()

    # Собираем payload строго под твою SQLAlchemy-модель Look
    payload = {
        "name": name.strip(),
        "style_id": style_options[selected_style_name],  # Достаем ID выбранного стиля
        "url_picture": url_picture.strip()
    }

    try:
        response = create_look(payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.status_code in (200, 201):
        st.success(f"Образ '{name}' успешно добавлен в SQLite!")
        # После создания перекидываем админа обратно в каталог
        st.switch_page("views/catalog.py")
    else:
        st.error(get_error_message(response))
