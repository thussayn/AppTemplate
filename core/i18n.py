# core/i18n.py
import json
import os
import logging
import streamlit as st

# إعداد التسجيل (logging) لعرض التحذيرات في حالة وجود مشاكل في ملفات الترجمة
logger = logging.getLogger(__name__)

LANGS = {
    "en": {"label": "English", "dir": "ltr"},
    "ar": {"label": "العربية", "dir": "rtl"},
}

# ✅ قائمة موحدة وخالية من التكرار
_DEF_TEXTS = {
    # === App Structure ===
    "app_title": {"en": "Secure Modular Starter", "ar": "قالب ستريمليت آمن ومنظّم"},
    "language": {"en": "Language", "ar": "اللغة"},
    "theme": {"en": "Theme", "ar": "الثيم"},
    "logout": {"en": "Log out", "ar": "تسجيل الخروج"},
    "home_title": {"en": "Home", "ar": "الصفحة الرئيسية"},
    "about_title": {"en": "About", "ar": "حول"},
    "about_content": {
        "en": "This is the About page of the Secure Modular Starter application.",
        "ar": "هذه هي صفحة حول تطبيق Secure Modular Starter."
    },
    "dashboard": {"en": "Dashboard", "ar": "لوحة التحكم"},
    "settings": {"en": "Settings", "ar": "الإعدادات"},
    "welcome_msg": {"en": "Welcome to your secure starter!", "ar": "مرحبًا بك في القالب الآمن!"},
    "app_title_label": {"en": "App Title", "ar": "عنوان التطبيق"},

    # === Authentication ===
    "login": {"en": "Login", "ar": "تسجيل الدخول"},
    "username": {"en": "Username", "ar": "اسم المستخدم"},
    "password": {"en": "Password", "ar": "كلمة المرور"},
    "remember_me": {"en": "Remember me", "ar": "تذكرني"},
    "login_button": {"en": "Login", "ar": "تسجيل الدخول"},
    "logged_in_success": {"en": "Logged in successfully!", "ar": "تم تسجيل الدخول بنجاح!"},
    "logged_out_success": {"en": "You have been logged out successfully.", "ar": "تم تسجيل الخروج بنجاح."},

    # === User Management ===
    "create_new_user": {"en": "Create New User", "ar": "إنشاء مستخدم جديد"},
    "create_user_button": {"en": "Create User", "ar": "إنشاء مستخدم"},
    "user_created_success": {"en": "User created successfully!", "ar": "تم إنشاء المستخدم بنجاح!"},
    "role": {"en": "Role", "ar": "الدور"},
    "admin": {"en": "Admin", "ar": "مسؤول"},
    "editor": {"en": "Editor", "ar": "محرر"},
    "viewer": {"en": "Viewer", "ar": "مشاهد"},

    # === Settings Form ===
    "save": {"en": "Save", "ar": "حفظ"},
    "cancel": {"en": "Cancel", "ar": "إلغاء"},
    "settings_saved": {"en": "Settings saved successfully!", "ar": "تم حفظ الإعدادات بنجاح!"},

    # === Language & Theme Options ===
    "language_selector_label": {"en": "Language", "ar": "اللغة"},
    "theme_selector_label": {"en": "Theme", "ar": "الثيم"},
    "english": {"en": "English", "ar": "الإنجليزية"},
    "arabic": {"en": "Arabic", "ar": "العربية"},
    "light": {"en": "Light", "ar": "فاتح"},
    "dark": {"en": "Dark", "ar": "داكن"},

    # === Dashboard Titles ===
    "home_page_title": {"en": "Home Page", "ar": "الصفحة الرئيسية"},
    "home_page_welcome": {"en": "Welcome to the Home page!", "ar": "مرحبًا بك في الصفحة الرئيسية!"},
    "admin_dashboard_title": {"en": "Admin Dashboard", "ar": "لوحة تحكم المسؤول"},
    "admin_dashboard_welcome": {"en": "Welcome, Admin!", "ar": "مرحبًا، أيها المسؤول!"},
    "editor_dashboard_title": {"en": "Editor Dashboard", "ar": "لوحة تحكم المحرر"},
    "editor_dashboard_welcome": {"en": "Welcome, Editor!", "ar": "مرحبًا، أيها المحرر!"},
    "viewer_dashboard_title": {"en": "Viewer Dashboard", "ar": "لوحة تحكم المشاهد"},
    "viewer_dashboard_welcome": {"en": "Welcome, Viewer!", "ar": "مرحبًا، أيها المشاهد!"},

    # === Auth Error Messages ===
    "missing_credentials": {"en": "Missing credentials", "ar": "بيانات الاعتماد مفقودة"},
    "user_not_found": {"en": "User not found", "ar": "المستخدم غير موجود"},
    "invalid_password": {"en": "Invalid password", "ar": "كلمة المرور غير صحيحة"},
    "username_password_required": {"en": "Username and password are required", "ar": "اسم المستخدم وكلمة المرور مطلوبان"},
    "username_exists": {"en": "Username already exists", "ar": "اسم المستخدم موجود مسبقًا"},
    "unknown_error": {"en": "An unknown error occurred", "ar": "حدث خطأ غير معروف"},
    "ok": {"en": "OK", "ar": "تم"},

    # === Generic ===
    "yes": {"en": "Yes", "ar": "نعم"},
    "no": {"en": "No", "ar": "لا"},
    "error": {"en": "Error", "ar": "خطأ"},
    "success": {"en": "Success", "ar": "نجاح"},
    "are_you_sure": {"en": "Are you sure?", "ar": "هل أنت متأكد؟"},
}

_TRANSLATIONS = {}

def _load_json(path: str):
    """تحميل ملف ترجمة JSON مع معالجة الأخطاء."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Translation file not found: {path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {path}: {e}")
        return {}

def load_translations():
    """تحميل الترجمات من مجلد locales."""
    global _TRANSLATIONS
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "locales")
    _TRANSLATIONS = {
        "en": _load_json(os.path.join(base_dir, "en.json")),
        "ar": _load_json(os.path.join(base_dir, "ar.json")),
    }

def get_text(key: str) -> str:
    """استرجاع النص المترجم حسب اللغة الحالية."""
    if not _TRANSLATIONS:
        load_translations()
    
    lang = st.session_state.get("lang", "en")
    if lang not in LANGS:
        lang = "en"  # fallback إلى الإنجليزية إذا كانت اللغة غير مدعومة

    # أولًا: جرّب من ملفات locales (إذا وُجدت)
    value = _TRANSLATIONS.get(lang, {}).get(key)
    if value is not None:
        return value

    # ثانيًا: جرّب من _DEF_TEXTS المضمنة
    if key in _DEF_TEXTS:
        return _DEF_TEXTS[key].get(lang, _DEF_TEXTS[key].get("en", key))

    # ثالثًا: fallback
    return f"??{key}??"

def init_language(default: str = "en"):
    """تهيئة اللغة الافتراضية في حالة عدم وجودها في الجلسة."""
    if "lang" not in st.session_state:
        st.session_state.lang = default