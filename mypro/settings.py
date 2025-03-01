from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # ✅ ใช้ Path ไม่ซ้ำซ้อน

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-szfb45_hy(an)p9-i&*7dlwhx^s61#_c5ktlth&er_-)9lbiox'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mypro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "store/templates"],  # ✅ ตรวจสอบให้แน่ใจว่า path นี้มีอยู่
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'mypro.wsgi.application'
AUTH_USER_MODEL = "store.CustomUser"

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ds',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',  # ✅ รองรับภาษาไทยและ Emoji
        },
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static Files Configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "store/static",  # ✅ กำหนด static ไว้ที่ root folder
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # ✅ ใช้สำหรับ collectstatic ใน production

# ✅ Media Files Configuration
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/login/"
LOGIN_REDIRECT_URL = "/"  # ✅ หลังจากล็อกอินให้ redirect ไปหน้าแรก

