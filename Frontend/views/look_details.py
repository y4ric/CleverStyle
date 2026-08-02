import requests
import streamlit as st
from components.item_card import render_cloth_card

# Используем одну общую переменную адреса, чтобы не ошибаться
BASE_URL = "http://127.0.0.1:8000"

def get_look_clothes(look_id: int):
    # Теперь адрес точный, без опечаток и со слэшем на конце
    return requests.get(f"{BASE_URL}/looks/{look_id}/clothes/")

look_id = st.session_state.get("selected_look_id")
look_name = st.session_state.get("selected_look_name", "Образ")

if not look_id:
    st.warning("Образ не выбран. Вернитесь назад.")
    if st.button("⬅️ К образам"):
        st.switch_page("views/style_details.py")
    st.stop()

if st.button("⬅️ Назад к списку образов"):
    st.switch_page("views/style_details.py")

st.title(f"🛍️ Капсула: {look_name}")
st.write("Эти вещи идеально сочетаются между собой:")
st.markdown("---")

try:
    response = get_look_clothes(look_id)
except requests.RequestException:
    st.error("Бэкенд недоступен. Убедитесь, что сервер FastAPI запущен.")
    st.stop()

if response.ok:
    clothes_in_look = response.json()
    if not clothes_in_look:
        st.info("В этот образ пока не добавлено ни одной вещи.")
    else:
        cols = st.columns(3)
        for idx, cloth in enumerate(clothes_in_look):
            with cols[idx % 3]:
                render_cloth_card(cloth, key_prefix=f"look_inside_{idx}")
else:
    st.error(f"Не удалось получить состав лука с бэкенда. Код: {response.status_code}")
