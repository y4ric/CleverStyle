import requests
import streamlit as st
from api.client import get_error_message

# Используем одну общую переменную адреса, чтобы не ошибаться в точках
BASE_URL = "http://127.0.0.1:8000"

def get_style_by_id(sid: int):
    return requests.get(f"{BASE_URL}/styles/{sid}/")

def get_looks_by_style(sid: int):
    return requests.get(f"{BASE_URL}/styles/{sid}/looks/")



style_id = st.session_state.get("selected_style_id")
style_name = st.session_state.get("selected_style_name", "Стиль")

if not style_id:
    st.warning("Стиль не выбран. Вернитесь в каталог.")
    if st.button("⬅️ В каталог"):
        st.switch_page("views/catalog.py")
    st.stop()

# Кнопка возврата на главную
if st.button("⬅️ Назад в каталог стилей"):
    st.switch_page("views/catalog.py")

st.title(f"👑 Готовые образы: {style_name}")
st.write("Выберите готовый лук, чтобы посмотреть, из каких вещей он состоит.")
st.markdown("---")

# ВРЕМЕННО УБИРАЕМ TRY-EXCEPT ДЛЯ ТЕСТА:
looks_resp = get_looks_by_style(style_id)

if not looks_resp.ok:
    st.error(f"Код ошибки FastAPI: {looks_resp.status_code}")
    st.text(looks_resp.text)
    st.stop()

if not looks_resp.ok:
    st.error(f"Код ошибки FastAPI: {looks_resp.status_code}")
    try:
        st.json(looks_resp.json())
    except Exception:
        st.text(looks_resp.text)
    st.stop()

# Если бэкенд ответил успешно (200 OK)
looks = looks_resp.json()

if not looks:
    st.info(f"В стиле {style_name} пока нет созданных луков.")
else:
    # Выводим сетку готовых образов
    look_cols = st.columns(3)
    for idx, look in enumerate(looks):
        with look_cols[idx % 3]:
            with st.container(border=True):
                if look.get("url_picture"):
                    try:
                        st.image(look["url_picture"], use_container_width=True)
                    except Exception:
                        st.warning("Не удалось загрузить фото лука")

                st.markdown(f"#### {look['name']}")
                st.write("")

                # Кнопка перехода к составу одежды этого образа
                if st.button("🛍️ Посмотреть состав одежды", key=f"look_btn_{look['look_id']}",
                             use_container_width=True):
                    st.session_state["selected_look_id"] = look["look_id"]
                    st.session_state["selected_look_name"] = look["name"]
                    st.switch_page("views/look_details.py")
