# ui/forms.py
import streamlit as st
from core.i18n import get_text
from users.auth_service import update_user_prefs, get_current_user

def settings_form(cookies=None):
    st.title(get_text("settings"))

    user = get_current_user()
    if not user:
        st.warning(get_text("must_be_logged_in"))
        return

    username = user["username"]
    current_lang = st.session_state.get("lang", "en")
    current_theme = st.session_state.get("theme", "light")

    # Language
    st.markdown("### " + get_text("language"))
    lang_labels = [get_text("english"), get_text("arabic")]
    label_to_lang = {get_text("english"): "en", get_text("arabic"): "ar"}
    current_label = get_text("arabic") if current_lang == "ar" else get_text("english")
    selected_label = st.selectbox(
        get_text("language"),
        options=lang_labels,
        index=lang_labels.index(current_label),
        key="settings_lang_select"
    )
    selected_lang = label_to_lang[selected_label]

    # Theme
    st.markdown("### " + get_text("theme"))
    theme_labels = [get_text("light"), get_text("dark")]
    theme_label_to_value = {get_text("light"): "light", get_text("dark"): "dark"}
    current_theme_label = get_text("dark") if current_theme == "dark" else get_text("light")
    selected_theme_label = st.selectbox(
        get_text("theme"),
        options=theme_labels,
        index=theme_labels.index(current_theme_label),
        key="settings_theme_select"
    )
    selected_theme = theme_label_to_value[selected_theme_label]

    if st.button(get_text("save")):
        update_user_prefs(username, preferred_lang=selected_lang, preferred_theme=selected_theme)
        st.session_state.lang = selected_lang
        st.session_state.theme = selected_theme
        if cookies is not None:
            cookies["lang"] = selected_lang
            cookies["theme"] = selected_theme
            cookies.save()
        st.success(get_text("settings_saved"))
        st.rerun()