"""
Django settings for django_training project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import dotenv
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False), ENV_FILE=(str, None), ALLOWED_HOSTS=(list, ['']))

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$1ty%e=j&0fxr--&&=qxf_e(x6^c+vf^1jrr7a47+u1t7kyvf7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '*',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'allauth',
    'allauth.account',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework.authtoken',
    'student_manager.users',
    'student_manager.students',
    'student_manager.classrooms',
    'student_manager.subjects',
    'storages',
    'student_manager.uploader',
    'student_manager.ocr',
    'django_celery_beat',
    'django_celery_results',
    'student_manager.stores',
    'student_manager.vouchers',
    'student_manager.promos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'django_training.urls'

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

WSGI_APPLICATION = 'django_training.wsgi.application'

# Custom Response
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'commons.middlewares.renderers.JSONResponseRenderer',
    ],
    'EXCEPTION_HANDLER': 'commons.middlewares.exception_handler.exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'django_training/staticfiles/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Override model user
AUTH_USER_MODEL = 'users.User'

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django_training/debug.log',
        },
    },
    # 'loggers': {
    #     'django': {
    #         'handlers': ['file'],
    #         'level': 'DEBUG',
    #         'propagate': True,
    #     },
    # },
}

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'staticfiles')

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'student_manager.users.serializers.UserRegisterSerializer',
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DOMAIN_URL = 'localhost'

CSRF_COOKIE_SECURE = True

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'student_manager',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'postgres',
        'PORT': '5432'
    }
}

# DATABASES = {'default': {}}
# db_from_env = dj_database_url.config(
#     conn_max_age=600, 
#     default='postgres://qreiogwdduhteo:a8aa17f83e87119d84036612762e969d09f0631ef601301727f3a8b6784c1003@ec2-18-210-64-223.compute-1.amazonaws.com:5432/d9o48scpevsf7m'
# )
# DATABASES['default'].update(db_from_env)

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = '+sHGRaUzreWefudW4kKz'
AWS_STORAGE_BUCKET_NAME = ''
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'ap-southeast-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'student_manager.uploader.services.PublicS3MediaStorage'

M360_URL = env("M360_URL", default="https://api.m360.com.ph/v3/api/globelabs/mt/")
M360_PASSPHRASE=""
M360_SHORTCODE=""

# celery settings
CELERY_BROKER_URL = "redis://127.0.0.1:6379"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379"
# CELERY_BEAT_SCHEDULE = {
    # 'send_email_invoice': {
    #     'task': 'student_manager.messagebus.tasks.send_invoice',
    #     'schedule': 30.0,
    # },
#     'create_monthly_invoice': {
#         'task': 'tasks.create_invoice',
#         'schedule': crontab(0, 0, day_of_month='28'),
#     },
# }
USE_TZ=False