# app.py
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# Set page config early
st.set_page_config(page_title="Secure Modular Starter", layout="wide")

# Initialize Encrypted Cookie Manager
cookies = EncryptedCookieManager(
    prefix="secure_modular_starter/",
    password="your-very-strong-secret-key-change-in-prod-2025!"  # ⚠️ Change in production
)

if not cookies.ready():
    st.stop()

# --- Early imports for auth and session management ---
from users.auth_service import (
    ensure_db_ready,
    restore_session_from_cookie,
    is_authenticated,
    get_current_user,
    logout
)

# Helper to update user preferences from sidebar
def update_user_language_and_theme(lang: str, theme: str):
    from users.auth_service import update_user_prefs
    user = get_current_user()
    if user:
        update_user_prefs(user["username"], preferred_lang=lang, preferred_theme=theme)

# Ensure DB is ready
ensure_db_ready()

# Restore session from cookie — unless we just logged out
if st.session_state.get("post_logout"):
    st.session_state.pop("post_logout", None)
else:
    restore_session_from_cookie(cookies)

# Initialize language and theme if not set
if "lang" not in st.session_state:
    st.session_state.lang = cookies.get("lang", "en")
if "theme" not in st.session_state:
    st.session_state.theme = cookies.get("theme", "light")

# Import other modules
from core.i18n import get_text
from features import auth as auth_feature
from core.layout import app_header, app_footer
from features import dashboard_admin, dashboard_editor, dashboard_viewer, home, about

# Sidebar
with st.sidebar:
    st.markdown("### 🌐 " + get_text("language"))
    lang_keys = ["en", "ar"]
    idx = lang_keys.index(st.session_state.lang) if st.session_state.lang in lang_keys else 0
    lang = st.selectbox(
        get_text("language_selector_label"),
        options=lang_keys,
        format_func=lambda x: {"en": get_text("english"), "ar": get_text("arabic")}[x],
        index=idx,
        key="lang_selector"
    )
    if lang != st.session_state.lang:
        st.session_state.lang = lang
        cookies["lang"] = lang
        if is_authenticated():
            update_user_language_and_theme(lang, st.session_state.get("theme", "light"))
        cookies.save()
        st.rerun()

    st.markdown("---")
    st.markdown("### 🎨 " + get_text("theme"))
    theme_keys = ["light", "dark"]
    current_theme = st.session_state.get("theme", "light")
    theme = st.radio(
        get_text("theme_selector_label"),
        options=theme_keys,
        index=theme_keys.index(current_theme) if current_theme in theme_keys else 0,
        format_func=lambda x: get_text(x),
        key="theme_selector"
    )
    if theme != st.session_state.get("theme", "light"):
        st.session_state.theme = theme
        cookies["theme"] = theme
        if is_authenticated():
            update_user_language_and_theme(st.session_state.lang, theme)
        cookies.save()
        st.rerun()

    # Logout button
    if is_authenticated():
        st.markdown("---")
        if st.button(get_text("logout")):
            logout(cookies=cookies)
            st.session_state.post_logout = True
            st.rerun()

# Apply RTL/LTR based on language — compatible with all Streamlit versions
def apply_direction_css(lang: str):
    # إنشاء ختم فريد لضمان تحديث CSS في كل مرة
    import time
    unique_stamp = str(int(time.time() * 1000000))  # microsecond timestamp
    
    if lang == "ar":
        css = f"""
        /* RTL CSS - {unique_stamp} */
        html, body, [data-testid="stAppViewContainer"],
        [data-testid="stHeader"], [data-testid="stSidebarContent"] {{
            direction: rtl !important;
            text-align: right !important;
        }}
        [data-testid="stSidebar"] {{
            left: auto !important;
            right: 0 !important;
        }}
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stRadio > div,
        .stMarkdown,
        .stText {{
            text-align: right !important;
        }}
        """
    else:
        css = f"""
        /* LTR CSS - {unique_stamp} */
        html, body, [data-testid="stAppViewContainer"],
        [data-testid="stHeader"], [data-testid="stSidebarContent"] {{
            direction: ltr !important;
            text-align: left !important;
        }}
        [data-testid="stSidebar"] {{
            left: 0 !important;
            right: auto !important;
        }}
        """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

apply_direction_css(st.session_state.lang)

# Header
app_header(get_text("app_title"), lang=st.session_state.lang)

# Routing
if not is_authenticated():
    auth_feature.render(cookies=cookies)
else:
    user = get_current_user()
    role = user.get("role", "Viewer")

    home_label = get_text("home_title")
    about_label = get_text("about_title")
    dashboard_label = get_text("dashboard")
    settings_label = get_text("settings")

    tab = st.tabs([home_label, about_label, dashboard_label, settings_label])

    with tab[0]:
        home.render()
    with tab[1]:
        about.render()
    with tab[2]:
        if role == "Admin":
            dashboard_admin.render()
        elif role == "Editor":
            dashboard_editor.render()
        else:
            dashboard_viewer.render()
    with tab[3]:
        from ui.forms import settings_form
        settings_form(cookies=cookies)

app_footer(lang=st.session_state.lang)