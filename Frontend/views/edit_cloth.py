import requests
import streamlit as st

# 1. Импортируем функцию обновления и вывода ошибок одежды
from api.client import get_error_message, update_cloth, get_cloth_by_id
from auth.state import require_admin

require_admin()
st.header("Редактирование вещи")

# Получаем ID одежды, которую админ выбрал для редактирования
clothes_id = st.session_state.get("edit_clothes_id")

if clothes_id is None:
    st.info("Сначала выберите вещь для редактирования.")
    st.stop()

try:
    item_response = get_cloth_by_id(clothes_id)
except requests.RequestException:
    st.error("Не удалось получить данные одежды с backend.")
    st.stop()

if not item_response.ok:
    st.error(get_error_message(item_response))
    st.stop()

item = item_response.json()
st.toast('Данные одежды успешно загружены!', icon='🎉')

# Форма редактирования строго под структуру твоей модели Clothes
with st.form(f"edit_cloth_form_{clothes_id}"):
    name = st.text_input("Название вещи", value=item["name"])

    # Списки доступных категорий и стилей
    categories = ["Верх", "Низ", "Обувь", "Верхняя одежда", "Аксессуары"]
    styles = ["Casual", "Old Money", "Streetwear", "Business Casual"]

    # Находим текущие индексы, чтобы выставить старые значения по умолчанию
    default_cat_idx = categories.index(item["category"]) if item["category"] in categories else 0
    default_style_idx = styles.index(item["style"]) if item["style"] in styles else 0

    category = st.selectbox("Категория", options=categories, index=default_cat_idx)
    style = st.selectbox("Стиль одежды", options=styles, index=default_style_idx)

    color = st.text_input("Цвет вещи", value=item.get("color", ""))
    url_picture = st.text_input("Ссылка на изображение (URL)", value=item.get("url_picture") or "")

    submitted = st.form_submit_button("Сохранить изменения")

if submitted:
    if not name.strip():
        st.error("Укажите название.")
        st.stop()
    if not color.strip():
        st.error("Укажите цвет вещи.")
        st.stop()
    if not url_picture.strip():
        st.error("Добавьте ссылку на изображение.")
        st.stop()

    # Формируем payload под структуру бэкенда таблицы Clothes
    payload = {
        "name": name.strip(),
        "category": category,
        "style": style,
        "color": color.strip(),
        "url_picture": url_picture.strip()
    }

    try:
        response = update_cloth(clothes_id, payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.ok:
        st.success("Изменения успешно сохранены!")
        st.session_state["selected_clothes_id"] = clothes_id
        st.switch_page("views/catalog.py")  # Перекидываем обратно в общий каталог одежды
    else:
        st.error(get_error_message(response))
