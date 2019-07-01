"""
Django settings for DmSuMarket project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os,sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = '/home/python/Desktop/DmSuMarket/dmsuMarket/dmsuMarket'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# add prefix apps to system path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zk^%pd#des6sr0f8ynli_2b853edm(mjjc-0%g6fs1aku_qxag'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users.apps.UsersConfig'
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

ROOT_URLCONF = 'dmsuMarket.urls'

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
        },
    },
]

WSGI_APPLICATION = 'dmsuMarket.wsgi.application'


# Database
# mysql: meiduo:meiduo@127.0.0.1:3306/meiduo_mail

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'meiduo',
        'PASSWORD': 'meiduo',
        'NAME': 'meiduo_mail'
    }
}

# redis: default@127.0.0.1:6379/0   session@127.0.0.1:6379/1

_REDIS_LOCATION = 'redis://127.0.0.1:6379/'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': _REDIS_LOCATION + '0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': _REDIS_LOCATION + '1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.cache.RedisCache',
        }
    }
}
SEESION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# Logging

_LOG_LEVEL = 'DEBUG'

LOGGING = {
    # todo: version
    'version': 1,
    # whether existing loggers are forbidden
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "%(levelname)s: *%(asctime)s* %(name)s@%(filename)s=%(funcName)s=:%(lineno)d=%(message)s"
        },
        'brief': {
            'format': "%(levelname)s:%(module)s@%(lineno)s:%(message)s"
        },
    },
    'filters': {
        'require_debug_true':{
            # only on debug model django will print log on console
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'handlers': {
        'console': {
            'level': _LOG_LEVEL,
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'brief'
        },
        'file': {
            'level': _LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/runlog.log'),
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'djlogger': {
            'handlers': ['console', 'file'],
            # whether logger continue pass information
            'propagate': True,
            'level': _LOG_LEVEL
        },
    },
}


# DRF CONFIG

REST_FRAMEWORK = {

    # Exception handlers
    'EXCEPTION_HANDLER': BASE_DIR + '.utils.exc_handlers.g_exc_handler',
}