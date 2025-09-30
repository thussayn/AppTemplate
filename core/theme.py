import streamlit as st
from .i18n import LANGS

THEMES = {
    "ocean": {
        "--brand": "#2563eb",
        "--bg": "#0b1220",
        "--panel": "#111827",
        "--text": "#e5e7eb",
        "--muted": "#9ca3af",
        "--accent": "#06b6d4",
    },
    "light": {
        "--brand": "#2563eb",
        "--bg": "#ffffff",
        "--panel": "#f5f7fb",
        "--text": "#111827",
        "--muted": "#6b7280",
        "--accent": "#22c55e",
    },
    "solar": {
        "--brand": "#b58900",
        "--bg": "#fdf6e3",
        "--panel": "#f5efe0",
        "--text": "#073642",
        "--muted": "#586e75",
        "--accent": "#268bd2",
    },
    "midnight": {
        "--brand": "#8b5cf6",
        "--bg": "#0f172a",
        "--panel": "#111827",
        "--text": "#e5e7eb",
        "--muted": "#9ca3af",
        "--accent": "#f59e0b",
    },
}

BASE_CSS = """<style>
:root { --radius: 14px; --pad: 1rem; }
body, .main, [data-testid="stAppViewContainer"] { background: var(--bg) !important; color: var(--text) !important; }
section[data-testid="stSidebar"] > div { background: var(--panel) !important; color: var(--text) !important; }
.block-container { padding-top: 2rem; }
.stMarkdown, .stAlert, .stDataFrame { border-radius: var(--radius); }
a { color: var(--accent) !important; }
.html-rtl { direction: rtl; text-align: right; }
.html-ltr { direction: ltr; text-align: left; }
button[kind="primary"] { background: var(--brand) !important; border-radius: var(--radius); }
</style>"""

def _dir_class(lang: str) -> str:
    return "html-rtl" if LANGS.get(lang, {}).get("dir") == "rtl" else "html-ltr"

def apply_theme(theme_key: str, lang: str):
    theme = THEMES.get(theme_key, THEMES["light"]).copy()
    vars_css = ":root{" + ";".join([f"{k}:{v}" for k, v in theme.items()]) + "}"
    st.markdown(f"<style>{vars_css}</style>", unsafe_allow_html=True)
    st.markdown(BASE_CSS, unsafe_allow_html=True)
    st.markdown(
        f"<script>document.documentElement.classList.remove('html-rtl','html-ltr');document.documentElement.classList.add('{_dir_class(lang)}');</script>",
        unsafe_allow_html=True,
    )
