# core/layout.py
import streamlit as st

def app_header(title: str, lang: str = "en"):
    direction = "rtl" if lang == "ar" else "ltr"
    text_align = "right" if lang == "ar" else "left"
    
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:.75rem;background:var(--panel);padding:1rem;border-radius:var(--radius);direction:{direction};text-align:{text_align};">
            <div style="width:12px;height:12px;background:var(--brand);border-radius:50%"></div>
            <h2 style="margin:0;">{title}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

def app_footer(lang: str = "en"):
    direction = "rtl" if lang == "ar" else "ltr"
    text_align = "right" if lang == "ar" else "left"
    
    st.markdown(
        f"""
        <hr/>
        <div style="opacity:.7;font-size:.9rem;direction:{direction};text-align:{text_align};">
            Built with Streamlit • Secure Modular Starter
        </div>
        """,
        unsafe_allow_html=True,
    )