import requests
import streamlit as st
# Импортируем нашу готовую карточку шмотки
from components.item_card import render_cloth_card

def get_look_clothes(look_id: int):
    # Этот эндпоинт FastAPI должен возвращать список объектов Clothes, входящих в образ
    return requests.get(f"http://127.0.0{look_id}/clothes")

look_id = st.session_state.get("selected_look_id")
look_name = st.session_state.get("selected_look_name", "Образ")

if not look_id:
    st.warning("Образ не выбран. Вернитесь назад.")
    if st.button("⬅️ К образам"):
        st.switch_page("views/style_details.py")
    st.stop()

# Кнопка шага назад
if st.button("⬅️ Назад к списку образов"):
    st.switch_page("views/style_details.py")

st.title(f"🛍️ Капсула: {look_name}")
st.write("Эти вещи идеально сочетаются между собой. Ты можешь добавить любую из них в избранное:")
st.markdown("---")

try:
    response = get_look_clothes(look_id)
except requests.RequestException:
    st.error("Бэкенд недоступен.")
    st.stop()

if response.ok:
    clothes_in_look = response.json()
    if not clothes_in_look:
        st.info("В этот образ пока не добавлено ни одной вещи.")
    else:
        # Выводим одежду в красивую сетку!
        cols = st.columns(3)
        for idx, cloth in enumerate(clothes_in_look):
            with cols[idx % 3]:
                # Вызываем нашу полноценную карточку! В ней уже есть лайки и логика избранного
                render_cloth_card(cloth, key_prefix=f"look_inside_{idx}")
else:
    st.error("Не удалось получить состав лука с бэкенда.")
