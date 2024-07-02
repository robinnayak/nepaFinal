
from pathlib import Path
import dj_database_url
from decouple import config
from datetime import timedelta
import os
import firebase_admin
from firebase_admin import credentials,storage
from google.oauth2 import service_account

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w%%5(=(^inejev)qg59(0!n=59001dw2f_h*+$cq2c!m)y3w(b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')
CSRF_TRUSTED_ORIGINS = ['https://nepafinal.vercel.app/']

#firebase configuration
# firebase_credentials = {
#     "type": "service_account",
#     "project_id": "nepamove-5c2f4",
#     "private_key_id": "42147bb0b72a9a3e2bc418321a1181035e242acb",
#     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2wWAISZYqupRB\nYokyAaIWmp5nleRfnnGNgRJY22iCEJsg3TmlyXYAZVdr9GeATdW3AUMtFD79jPPO\ngL51NcMp6EswGfIg530xG3OiZvr//d8UGUrbAVkVpVeNNEmOKrZiiVOTG7y8dXDI\nswXhiQfSPMnDp6g2A5hjUpJW+GEcpCwBccc5p2z2WnoRxMAbBRR1FNnPkMCrmjCS\nkFkGw/EuQoF24hIhtLOkvG8aV1KkqZ03bdt0pzCeKFQt0OytBiA2j6Lx2c4ea3CI\nvZmv1g76RRnKFBoX4fkdjaukheVh/JA+5MX9cWhfSH4CSIysFF/HB/yBphEWXlCQ\n6eiu4VtlAgMBAAECggEABZ4tWo128HqENi8jDCBHhq305dBFkR7owX9qb5E6Rc1G\n4RxYoLajSi3TVL4FmuJJo7+F/IVdZ/C344aXoQWPEBaHWsPH0Q65c+Bl9JcTBJPq\nq85/O5Si09FQvxMQmi5iWH/jy5p6ecloA/Nk4ElhesTKZ8y0+6J7dVb2qQ/BKt7G\nFDfga2Oq7EdUdH/NHu/VtCRqrNTbb/K0zAHKm8sFr9AaysfkUzB6Lq91Xcv3TA7a\nw+5YHbVdrZlbtW2x90QphZFVdFmnRG2dClwf1vufT4qJjwus+NA0aGI2rc6ZBJX4\n38tPBuRiSIala5BNY+c6yvpcgVTbJsOO7VleAZZTHQKBgQD1vnkwV1Ac4L8vWGaO\nb11HBzCOWrsvgi9Z5SzqWrZIMYT/zTngLbBZ5KhNy+XCoQHWT1QfC1EptLIJ0J+M\nYznnWzCMjqaC+YRhsNsJBWh7mRd//YHvIkBqBKF2nbrwYtX6Ol+IHnR+fXVlTuZk\nmJieVtKe3VcB92bc2RSmZl3uVwKBgQC+Ye54OdT/oQYRB4+l5hbIReZGXgvK9CFf\nUQif2d8quUQTU99bRE0QozpfT4uGM4RYopP5Pz0/5UobP04R3TX5Jthp0ALtdL6d\nZX+6bvnGhKaPnC1sL+jRiELCyS2p5iTmqXztsDLSIYwyaz3YWaZ3Exh8ABXdr/E2\nwrLNdW32owKBgQDCUCtpkxDQ1NG38TGe3OYn3MKDPbEXftxMO8/JO5M5AJcG4dMq\ntVXlrs16Pojd3gwi1rVQmtVBohTJeAJAstE9ZDi+W6nElOIdkQeRWYpleQdA+EZ+\nvVmrux+lOFFx9OT3qKKTcmlw/2kNg1bgIl1DjqmaXrCG6IaYiLowXW9WnwKBgA0F\n3+0jb5mI50RU8xOTGK3ccjMQDdh1OK8veNqOacCfabO0wguZMXhY4g5Q/6dPcNcr\nT9n15HexdI9Glk2Mhzui15ztWLXrjXpwzfrvynA09LvQIB9Na6yhmIeAgXokvxN0\nNpJ/wgozt0ZfpZxeDZAJo1wgGV7PwT1QtjBtvvbnAoGAT4aOliDF9WLYy0x/bj/9\n8d94CF6OQeTC6POY/1d2aWYJ8Dq9KvWxVFhGf7/U3DcCwB+/KGS1j/bJvGcHhJvC\nPD0F35629Xf8wcra1RoljcTIP+N80o9WQB8Mm1gzYuauUqpwKb6xVRoeNc2unrn/\nw9EKLzkTEX2gCXkqkHzbBt8=\n-----END PRIVATE KEY-----\n",
#     "client_email": "firebase-adminsdk-fgyy0@nepamove-5c2f4.iam.gserviceaccount.com",
#     "client_id": "114539793901721396567",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fgyy0%40nepamove-5c2f4.iam.gserviceaccount.com",
#     "universe_domain": "googleapis.com"
# }

# cred = credentials.Certificate(firebase_credentials)

# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'nepamove-5c2f4.appspot.com'
# })

# gcs_credentials = service_account.Credentials.from_service_account_info(firebase_credentials)
# DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
# GS_CREDENTIALS = gcs_credentials
# GS_BUCKET_NAME = 'nepamove-5c2f4.appspot.com'
# GS_DEFAULT_ACL = 'publicRead'

# firebase = pyrebase.initialize_app(firebase_credentials)
# storage = firebase.storage()

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'api',
    'authentication',
    'passenger',
    'driver',
    'organization',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES' : ('rest_framework.renderers.JSONRenderer',)
}

ROOT_URLCONF = 'nepaFinal.urls'

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

WSGI_APPLICATION = 'nepaFinal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles_build" / "static"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'authentication.CustomUser'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
}