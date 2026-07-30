import requests
import streamlit as st

from api.client import get_error_message, register


st.header("Регистрация")

with st.form("registration_form"):
    full_name = st.text_input("ФИО", key="registration_full_name")
    email = st.text_input("Почта", key="registration_email")
    password = st.text_input(
        "Пароль",
        type="password",
        key="registration_password",
    )
    submitted = st.form_submit_button("Зарегистрироваться")

if submitted:
    if not full_name.strip() or not email.strip() or not password:
        st.error("Заполните все поля.")
        st.stop()

    try:
        response = register(
            email=email.strip(),
            password=password,
            full_name=full_name.strip(),
        )
    except requests.RequestException:
        st.error("Backend недоступен. Проверьте, запущен ли FastAPI.")
        st.stop()

    if response.status_code in (200, 201):
        st.success("Регистрация выполнена. Теперь войдите в аккаунт.")
        st.switch_page("views/login.py")
    else:
        st.error(get_error_message(response))

st.page_link("views/login.py", label="Уже есть аккаунт? Войти")