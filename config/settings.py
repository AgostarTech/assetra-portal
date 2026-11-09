import os
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    host.strip()
    for host in config(
        "ALLOWED_HOSTS",
        default="127.0.0.1,localhost,.onrender.com,assetra.africa,www.assetra.africa",
    ).split(",")
    if host.strip()
]

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # Project applications
    "accounts",
    "assets",
    "portfolios",
    "documents",
    "dashboards",
    "support",
    "audit.apps.AuditConfig",
]

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise for production static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --------------------------------------------------
# DATABASE - SUPABASE POSTGRESQL (CLOUD)
# --------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# --------------------------------------------------
# CUSTOM USER MODEL & BACKENDS
# --------------------------------------------------
AUTH_USER_MODEL = "accounts.CustomUser"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# --------------------------------------------------
# AUTHENTICATION AND REDIRECTS
# --------------------------------------------------
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "dashboards:role_router"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# --------------------------------------------------
# TIMEZONE AND DATETIME HANDLING
# --------------------------------------------------
USE_TZ = True
TIME_ZONE = "Africa/Dar_es_Salaam"

# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Robust WhiteNoise storage for production
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# --------------------------------------------------
# MEDIA FILES
# --------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------
# DEFAULT PRIMARY KEY
# --------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------
# JAZZMIN ADMIN THEME
# --------------------------------------------------
JAZZMIN_SETTINGS = {
    "site_title": "Asset Portal Admin",
    "site_header": "Asset Portal",
    "site_brand": "Enterprise Portfolio",
    "welcome_sign": "Welcome to the Secure Admin Hub",
    "copyright": "Asset Portal Enterprise",
    "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-warning",
    "accent": "accent-warning",
}

# Email Configuration (SMTP Real Delivery)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aroycetom@gmail.com'
EMAIL_HOST_PASSWORD = 'budxqijmyzqaziaq'
DEFAULT_FROM_EMAIL = 'Assetra Africa <aroycetom@gmail.com>'

# Africa's Talking SMS Configuration
AT_USERNAME = os.environ.get('AT_USERNAME', 'sandbox')
AT_API_KEY = os.environ.get('AT_API_KEY', 'atsk_2d7c42af1c97dab732786631f714aa99a64e4961983cade49a510c61403165b19705448d')