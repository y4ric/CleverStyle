import requests
import streamlit as st

# 1. Импортируем раздельные функции получения избранного и новые карточки
from api.client import get_error_message, get_favourites_clothes, get_favourites_styles
from auth.state import require_login
from components.item_card import render_cloth_card, render_style_card

require_login()
st.header("❤️ Моё избранное")

# 2. Создаем две красивые вкладки сверху страницы
tab_clothes, tab_styles = st.tabs(["👚 Любимая одежда", "✨ Сохраненные стили"])

# ==========================================
#   ВКЛАДКА 1: ИЗБРАННАЯ ОДЕЖДА
# ==========================================
with tab_clothes:
    try:
        response_clothes = get_favourites_clothes()
    except requests.RequestException:
        st.error("Не удалось загрузить избранную одежду.")
        response_clothes = None

    if response_clothes:
        if not response_clothes.ok:
            st.error(get_error_message(response_clothes))
        else:
            clothes_items = response_clothes.json()

            if not clothes_items:
                st.info("Вы пока не добавили ни одной вещи в избранное.")
            else:
                # Отрисовываем сетку из 3 колонок для вещей
                cols = st.columns(3)
                for index, item in enumerate(clothes_items):
                    with cols[index % 3]:
                        # Вызываем карточку одежды с префиксом "favorite"
                        render_cloth_card(item, key_prefix=f"favorite_cloth_{index}")

# ==========================================
#   ВКЛАДКА 2: ИЗБРАННЫЕ СТИЛИ
# ==========================================
with tab_styles:
    try:
        response_styles = get_favourites_styles()
    except requests.RequestException:
        st.error("Не удалось загрузить сохраненные стили.")
        response_styles = None

    if response_styles:
        if not response_styles.ok:
            st.error(get_error_message(response_styles))
        else:
            styles_items = response_styles.json()

            if not styles_items:
                st.info("Вы пока не сохранили ни одного направления стиля.")
            else:
                # Отрисовываем сетку из 3 колонок для стилей
                cols = st.columns(3)
                for index, item in enumerate(styles_items):
                    with cols[index % 3]:
                        # Вызываем карточку стиля с префиксом "favorite"
                        render_style_card(item, key_prefix=f"favorite_style_{index}")
