"""
Django settings for printercloud project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%!jyfax1)ly1%jfr89-(_7h^ro4e4_52fm&mtlco4jy%#(@4x='

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
    'apps.main',
    'apps.login',
    'apps.dashboard',
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

ROOT_URLCONF = 'printercloud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = 'printercloud.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
UPLOAD_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'template_static/'),
)
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# For development, set this to False; in production, it should be True if using HTTPS
SESSION_COOKIE_SECURE = False

# Optionally, you can enable this to delete the session when the browser closes
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os

AUTH0_DOMAIN = 'dev-26yi4saqemb6bhiy.us.auth0.com'
AUTH0_CLIENT_ID = 'jEUYLMN0HSezPflCbthh43Prp9fy0xw6'
AUTH0_CLIENT_SECRET = 'f0o_fhnUZ-veh41A7ngqD5wDnDKuod0-Dus3KjoOf31WvBaB7TtnRjd40SDRiCZ1'
AUTH0_CALLBACK_URL = 'http://localhost:8000/callback'  # Use localhost URL for development

# Configure Django authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_auth0.auth0backend.Auth0Backend',  # Auth0 backend
]

# Django settings for login and logout redirects
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/"

# Auth0 configuration in settings
SOCIAL_AUTH_AUTH0_DOMAIN = AUTH0_DOMAIN
SOCIAL_AUTH_AUTH0_KEY = AUTH0_CLIENT_ID
SOCIAL_AUTH_AUTH0_SECRET = AUTH0_CLIENT_SECRET

MOCK_API = True

if MOCK_API:
    BASE_API_URL = "https://default-blackbird-aleksandrs-organization-c5c42-0.blackbird-relay.a8r.io/printercloud-api"
    EPSON_API_URL = "https://default-blackbird-aleksandrs-organization-c5c42-0.blackbird-relay.a8r.io/epson-connect-printing-api"
    AUTH_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

else:
    pass