"""
Django settings for YandexHub project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ai(u4jwm*p$a7z7-6fbub100c1ul5sl3mew88!3-f#h4skbnph'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # DRF
    'rest_framework.authtoken',  # auth tokens
    'django_summernote',  # custom input
    'djoser', # tokens
    'channels', # channels
    "corsheaders", # cors headers
    
    'site_app',  # site app
    'api_app', # api app
    'socket_app', # socket socket app
]

# User model
AUTH_USER_MODEL = 'site_app.CustomUser'
AUTH_PROFILE_MODULE = 'site_app.CustomUser'
LOGIN_URL = 'signin'
LOGIN_REDIRECT_URL = '/home/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'YandexHub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'poll_extras': 'site_app.templatetags.poll_extras',
            }
        },
    },
]

WSGI_APPLICATION = 'YandexHub.wsgi.application'
ASGI_APPLICATION = 'YandexHub.routing.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '...', 
        'USER': 'postgres', 
        'PASSWORD': '...',
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'yandexhub_db', 
        'USER': 'postgres', 
        'PASSWORD': '12344321',
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    BASE_DIR / "static",
)

MEDIA_ROOT = BASE_DIR / "media"


# SMTP
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '...'
EMAIL_HOST_PASSWORD = '...'


# Summernote
X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_THEME = 'bs4'
SUMMERNOTE_CONFIG = {
    'iframe': True,
    'attachment_filesize_limit': 2560 * 2560,
    'summernote': {
        'airMode': False,
        'width': '100%',
        'height': '500',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen']],  # codeview, help
        ],
    },
}


# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}


# Celery settings
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60


# REDIS settings
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_ACCEPT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Cors settings (allowed urls)
CORS_ORIGIN_WHITELIST = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]


# site domain, used for telegram bot
DOMEN = 'http://127.0.0.1:8000/'


# Limitations
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.wmv', '.mov', '.3gp', '.flv', '.webm']
IMAGE_EXTENSIONS = ['.jpeg', '.jpg', '.gif', '.png', '.pict', '.ico', '.tiff', '.ai', '.webp', '.eps', '.cdr']
TRACK_EXTENSIONS = ['.wav', '.aif', '.mp3', '.mid']
MAX_IMAGE_SIZE = 7864320  # 7.5 MB
MAX_VIDEO_SIZE = 209715200  # 200 MB