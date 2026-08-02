import requests
import streamlit as st
from api.client import get_error_message, get_styles

# 1. ОБЯЗАТЕЛЬНО ИМПОРТИРУЕМ НАШУ ГОТОВУЮ КАРТОЧКУ СТИЛЯ С ИЗБРАННЫМ
from components.item_card import render_style_card

st.title("✨ Умный стилист CleverStyle")
st.write("Выберите направление стиля, чтобы посмотреть готовые капсулы и образы.")
st.markdown("---")

try:
    styles_response = get_styles()
except requests.RequestException:
    st.error("Бэкенд недоступен. Проверьте запуск FastAPI.")
    st.stop()

if styles_response.ok:
    styles = styles_response.json()
    if not styles:
        st.info("Стили еще не добавлены в базу.")
    else:
        # Рисуем красивую сетку из 3 колонок для направлений стилей
        style_cols = st.columns(3)
        for idx, style_item in enumerate(styles):
            with style_cols[idx % 3]:
                # 2. ЗАМЕНИЛИ ВЕСЬ РУЧНОЙ КОД НА ОДНУ СИСТЕМНУЮ ФУНКЦИЮ!
                # Она сама выведет картинку, описание, кнопку Избранного и кнопку перехода
                render_style_card(style_item, key_prefix=f"catalog_style_{idx}")
