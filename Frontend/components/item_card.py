import requests
import streamlit as st

# Импортируем наши новые функции для одежды и стилей из api.client
from api.client import (
    get_error_message,
    add_favourite_cloth,
    remove_favourite_cloth,
    add_favourite_style,
    remove_favourite_style,
    delete_cloth,  # для админ-действий с одеждой
)
from auth.state import is_admin, is_authenticated


# ==========================================
#   ЛОГИКА КНОПОК ИЗБРАННОГО
# ==========================================

def render_favorite_cloth_button(item: dict, key_prefix: str) -> None:
    """Кнопка избранного для одежды"""
    if not is_authenticated():
        st.caption("Войдите, чтобы добавить запись в избранное.")
        return

    clothes_id = item["clothes_id"]
    # Если префикс "favorite" или у вещи в базе уже есть лайк — считаем её избранной!
    is_favorite = item.get("is_favorite", False) or key_prefix.startswith("favorite") or item.get("favorites_count",
                                                                                                  0) > 0

    button_text = "Убрать из избранного" if is_favorite else "В избранное"

    if st.button(button_text, key=f"{key_prefix}_fav_cloth_{clothes_id}"):
        try:
            if is_favorite:
                response = remove_favourite_cloth(clothes_id)
            else:
                response = add_favourite_cloth(clothes_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            if button_text == "В избранное":
                st.balloons()
                import time
                time.sleep(1.5)
            st.rerun()
        else:
            st.error(get_error_message(response))


def render_favorite_style_button(item: dict, key_prefix: str) -> None:
    """Кнопка избранного для стилей"""
    if not is_authenticated():
        st.caption("Войдите, чтобы добавить запись в избранное.")
        return

    style_id = item["style_id"]
    is_favorite = item.get("is_favorite", False) or key_prefix == "favorite"
    button_text = "Убрать из избранного" if is_favorite else "В избранное"

    if st.button(button_text, key=f"{key_prefix}_fav_style_{style_id}"):
        try:
            if is_favorite:
                response = remove_favourite_style(style_id)
            else:
                response = add_favourite_style(style_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            if button_text == "В избранное":
                st.balloons()
                import time
                time.sleep(1.5)
            st.rerun()
        else:
            st.error(get_error_message(response))


# ==========================================
#   ЛОГИКА ДЕЙСТВИЙ АДМИНИСТРАТОРА
# ==========================================

def render_admin_cloth_actions(clothes_id: int, key_prefix: str) -> None:
    """Действия админа над одеждой"""
    if not is_admin():
        return

    edit_column, delete_column = st.columns(2)

    if edit_column.button("Редактировать", key=f"{key_prefix}_edit_cloth_{clothes_id}"):
        st.session_state["edit_clothes_id"] = clothes_id
        st.switch_page("views/edit_cloth.py")

    if delete_column.button("Удалить", key=f"{key_prefix}_del_cloth_{clothes_id}", type="primary"):
        try:
            response = delete_cloth(clothes_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            st.success("Одежда удалена.")
            st.switch_page("views/catalog.py")
        else:
            st.error(get_error_message(response))


# ==========================================
#   ФИНАЛЬНЫЕ КАРТОЧКИ ДЛЯ ОТРИСОВКИ В VIEWS
# ==========================================

def render_cloth_card(item: dict, key_prefix: str = "cloth_card") -> None:
    """Отрисовка карточки одежды"""
    clothes_id = item["clothes_id"]

    with st.container(border=True):
        if item.get("url_picture"):
            try:
                st.image(item["url_picture"], use_container_width=True)
            except Exception:
                st.warning("Не удалось загрузить изображение (некорректная ссылка)")
        else:
            st.info("Изображение не добавлено")

        # Счётчики просмотров и лайков для одежды
        views = item.get("views_count", 0)
        favs = item.get("favorites_count", 0)

        st.markdown(
            f"""
            <div style="display: flex; gap: 15px; margin-top: 5px; margin-bottom: 5px; font-size: 0.9rem; opacity: 0.8;">
                <span>👁️ {views} просмотров</span>
                <span>❤️ {favs} в избранном</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Название вещи и её категория / цвет
        st.markdown(
            f"<div style='height: 60px; overflow: hidden;'><h3 style='margin:0; padding:0; font-size:1.2rem; font-weight:600;'>{item['name']}</h3></div>",
            unsafe_allow_html=True
        )

        # Вывод тегов Категории и Цвета одежды
        st.caption(f"Категория: {item.get('category', '—')} | Цвет: {item.get('color', '—')}")

        # Описание вещи
        desc_text = item.get("description", "") or "Описание отсутствует."
        st.markdown(
            f"<div style='height: 75px; overflow: hidden; font-size:0.95rem; color:#31333F; line-height:1.4;'>{desc_text}</div>",
            unsafe_allow_html=True
        )

        # Кнопка избранного для одежды
        render_favorite_cloth_button(item, key_prefix=key_prefix)

        if st.button("Подробнее", key=f"cloth_details_btn_{clothes_id}"):
            st.session_state["selected_clothes_id"] = clothes_id
            st.switch_page("views/cloth_details.py")

        # Админ-кнопки для одежды
        render_admin_cloth_actions(clothes_id, key_prefix=key_prefix)


def render_style_card(item: dict, key_prefix: str = "style_card") -> None:
    """Отрисовка карточки направления стиля"""
    style_id = item["style_id"]

    with st.container(border=True):
        if item.get("url_picture"):  # Проверь, как называется поле обложки у стиля (url_picture или url_cover)
            try:
                st.image(item["url_picture"], use_container_width=True)
            except Exception:
                st.warning("Не удалось загрузить изображение обложки")
        else:
            st.info("Обложка стиля не добавлена")

        # Счетчик лайков стиля
        favs = item.get("favorites_count", 0)
        st.markdown(
            f"""
            <div style="display: flex; gap: 15px; margin-top: 5px; margin-bottom: 5px; font-size: 0.9rem; opacity: 0.8;">
                <span>❤️ {favs} подписчиков на стиль</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Название стиля
        st.markdown(
            f"<div style='height: 40px; overflow: hidden;'><h3 style='margin:0; padding:0; font-size:1.3rem; font-weight:600; color:#1E3A8A;'>{item['name']}</h3></div>",
            unsafe_allow_html=True
        )

        # Философия / описание стиля
        desc_text = item.get("description", "") or "Описание стиля отсутствует."
        st.markdown(
            f"<div style='height: 65px; overflow: hidden; font-size:0.95rem; color:#31333F; line-height:1.4;'>{desc_text}</div>",
            unsafe_allow_html=True
        )

        # 1. ВЫЗЫВАЕМ КНОПКУ ИЗБРАННОГО ДЛЯ СТИЛЯ (Теперь она появится на экране!)
        render_favorite_style_button(item, key_prefix=key_prefix)

        # 2. Кнопка открытия образов стиля
        if st.button("🗺️ Открыть образы стиля", key=f"style_details_btn_{style_id}", use_container_width=True):
            st.session_state["selected_style_id"] = style_id
            st.session_state["selected_style_name"] = item["name"]
            st.switch_page("views/style_details.py")
