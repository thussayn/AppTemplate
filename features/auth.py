# features/auth.py
import streamlit as st
from core.i18n import get_text
from users.auth_service import login

def render(cookies=None):
    st.title(get_text("login"))
    
    with st.form("login_form"):
        username = st.text_input(get_text("username"))
        password = st.text_input(get_text("password"), type="password")
        remember = st.checkbox(get_text("remember_me"))
        submit = st.form_submit_button(get_text("login_button"))
    
    if submit:
        success, message_key = login(username, password, remember, cookies=cookies)
        if success:
            st.success(get_text("logged_in_success"))
            st.rerun()
        else:
            st.error(get_text(message_key))

def render_register_user():
    st.title(get_text("create_new_user"))
    username = st.text_input(get_text("username"))
    password = st.text_input(get_text("password"), type="password")
    role_options = ["Admin", "Editor", "Viewer"]
    role = st.selectbox(get_text("role"), options=role_options)
    
    if st.button(get_text("create_user_button")):
        from users.auth_service import create_user
        success, message_key = create_user(username, password, role)
        if success:
            st.success(get_text("user_created_success"))
        else:
            st.error(get_text(message_key))

def render_logout():
    from users.auth_service import logout
    logout()
    st.success(get_text("logged_out_success"))
    st.rerun()