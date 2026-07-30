import requests
import streamlit as st
from api.client import get_error_message, get_styles

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
                with st.container(border=True):
                    # Показываем обложку стиля
                    if style_item.get("url_picture"):
                        try:
                            st.image(style_item["url_picture"], use_container_width=True)
                        except Exception:
                            st.warning("Не удалось загрузить обложку")

                    st.markdown(f"### {style_item['name']}")
                    st.caption(style_item.get("description", "Описание отсутствует"))
                    st.write("")

                    # Кнопка перехода внутрь стиля к образам
                    if st.button("🗺️ Открыть образы стиля", key=f"open_style_btn_{style_item['style_id']}",
                                 use_container_width=True):
                        st.session_state["selected_style_id"] = style_item["style_id"]
                        st.session_state["selected_style_name"] = style_item["name"]
                        st.switch_page("views/style_details.py")
