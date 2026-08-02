import requests
import streamlit as st
from api.client import get_clothes, get_error_message
from auth.state import require_admin


# Быстрая функция получения вообще всех луков из базы для выбора
def get_all_looks():
    return requests.get("http://127.0.0")  # Убедись, что на бэкенде есть GET /looks/ или /styles/../looks


require_admin()
st.header("🛠 Конструктор капсул: Добавление одежды в образ")

# 1. Загружаем все образы (луки), чтобы админ выбрал, какую капсулу собирать
# Для теста можно просто взять текущий look_id из сессии, если ты перешел со страницы образа!
current_look_id = st.session_state.get("selected_look_id")
current_look_name = st.session_state.get("selected_look_name", "Не выбран")

st.info(f"Вы собираете образ: **{current_look_name}** (ID: {current_look_id})")

if not current_look_id:
    st.warning("Сначала выберите образ в каталоге!")
    st.stop()

st.write("### Выберите вещи, которые входят в этот лук:")

# 2. Загружаем вообще всю одежду, которая есть в базе данных SQLite
try:
    clothes_resp = get_clothes()
except requests.RequestException:
    st.error("Бэкенд недоступен.")
    st.stop()

if not clothes_resp.ok:
    st.error(get_error_message(clothes_resp))
    st.stop()

all_clothes = clothes_resp.json()

if not all_clothes:
    st.warning("В базе данных еще нет одежды. Сначала добавьте вещи через меню 'Добавить одежду'!")
    st.stop()

# 3. Создаем форму со списком вещей и чекбоксами (галочками)
from api.client import link_clothes_to_look

with st.form("add_clothes_to_look_form"):
    # Словарь, где будем хранить галочки: {clothes_id: True/False}
    selected_items = {}

    for cloth in all_clothes:
        # Красиво выводим строчку одежды: Категория | Название | Цвет
        label = f"[{cloth['category']}] {cloth['name']} ({cloth['color']})"

        # Отрисовываем чекбокс для каждой шмотки
        selected_items[cloth["clothes_id"]] = st.checkbox(label, key=f"cloth_check_{cloth['clothes_id']}")

    submitted = st.form_submit_button("💼 Сохранить состав капсулы")

if submitted:
    # Ищем, какие вещи админ отметил галочками
    linked_count = 0
    for clothes_id, is_selected in selected_items.items():
        if is_selected:
            # Отправляем каждую отмеченную вещь на бэкенд в таблицу связей
            response = link_clothes_to_look(current_look_id, clothes_id)
            if response.ok:
                linked_count += 1

    if linked_count > 0:
        st.success(f"🎉 Успешно! В образ '{current_look_name}' добавлено вещей: {linked_count}")
        # Возвращаем админа обратно посмотреть на готовую капсулу одежды!
        st.switch_page("views/look_details.py")
    else:
        st.warning("Вы не выбрали ни одной вещи.")
