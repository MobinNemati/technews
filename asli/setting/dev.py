from asli.settings import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y_!!7f1a_25f!vj+_nrwh^00si$1s@x$l$bgz0t25$k&m7b)z0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


#INSTALLED_APPS = []


# sites framework
SITE_ID = 3


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media/'


STATICFILES_DIRS = [
    BASE_DIR / 'statics',
]

# debug_toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

X_FRAME_OPTIONS = 'SAMEORIGIN'


#compressor settings
COMPRESS_ENABLED = True

