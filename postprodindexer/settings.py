"""
Django settings for postprodindexer project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Django security key
SECRET_KEY = config('SECRET_KEY', cast=str, default='03x7v)57f$4h6_ucubc@1p@^jh__u95-ahh=_**3_0zw!6lyd')
# should debug mode be turned on or off? default = False
DEBUG = config("DEBUG", cast=bool, default=False)
LOGGING_LEVEL = "DEBUG" if DEBUG else config("LOGGING_LEVEL", cast=str, default="WARNING")

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap5',
    'indexer',
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

ROOT_URLCONF = 'postprodindexer.urls'

cached_loaders = [("django.template.loaders.cached.Loader",
                   ["django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader"]
                   )]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ] if DEBUG else cached_loaders,
        },
    },
]

WSGI_APPLICATION = 'postprodindexer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
key_list = [
        'DB_HOST',
        'DB_PORT',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
    ]
db_connections = dict()
for key in key_list:
    casting = int if "port" in key.lower() else str
    default_value = 3306 if "port" in key.lower() else ""
    db_connections[key] = config(key, cast=casting, default=default_value)

USE_LOCAL_DB = config("USE_LOCAL_DB", cast=bool, default=False)
if USE_LOCAL_DB:
    print("using sqlite3")
    my_default_db = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
else:
    print("using mysql")
    my_default_db = {
        'ENGINE': 'django.db.backends.mysql',
        'TIME_ZONE': 'UTC',
        'HOST': db_connections["DB_HOST"],
        'PORT': db_connections["DB_PORT"],
        'NAME': db_connections["DB_NAME"],
        'USER': db_connections["DB_USER"],
        'PASSWORD': db_connections["DB_PASSWORD"],
        'INIT_COMMAND': 'SET default_storage_engine=INNODB',
    }

DATABASES = {
    'default': my_default_db,
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


ERROR_LOG = config("ERROR_LOG", cast=str, default="/var/log/apache2/error.log")
ACCESS_LOG = config("ACCESS_LOG", cast=str, default="/var/log/apache2/access.log")


SITE = "glf-proxy"