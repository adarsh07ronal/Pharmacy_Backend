"""
Django settings for pharmacy project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os 
from django.utils.translation import gettext_lazy as _
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8_zvgg)h*)7ow1f#5(=x7_6=1uxf_vd17_6585$(a(jvul_-=b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.line',
    
    'rest_framework',
    'rest_auth',
    'rest_framework.authtoken',
    'drf_yasg',
    'django_filters',
    'rest_framework_swagger',
    'corsheaders',

    'patient',
    'drug',
    'article',
    'notice',
    'notification',
    'inquiry',
    # 'user_memo',
    # 'otc_app',
    'pharmacy_drug_information',
    'pharmacy_otc_information',
    'template',
    'drugstore',
    'reservation',
    'pharmaceutical_manufacturer',
    'message',
    'medicine_tips',
    'favorites',
    'django_crontab'
    ]

SITE_ID = 1


SOCIALACCOUNT_PROVIDERS = {
          'line': {
              'APP': {
                  'client_id': '1656814152',
                  'secret': '53728f3d7c87b67bc456bde1dd72a7fd'
              },
              "SCOPE": ['email', 'openid', 'profile']
          }
      }

LOGIN_REDIRECT_URL = '/'

# CELERY_RESULT_BACKEND = "django-db"
# CELERY_RESULT_BACKEND = 'django-cache'


INSTALLED_APPS += [
    'pharmacy_auth',

]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware'
    # 'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'pharmacy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'pharmacy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'postgres.ckovfasq13ub.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
        "PASSWORD": 'pharmacy123',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',

    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend','rest_framework.filters.SearchFilter'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_EMAIL_FROM = 'developers.geitpl@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'developers.geitpl@gmail.com'
EMAIL_HOST_PASSWORD = 'lghozbwbmkvtragz'

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = ["http://bs-local.com:3000","http://localhost:8000","http://localhost:3000","https://pharmacy-user.netlify.app","https://dev-pharma-cms.eoraa.com","https://pharma-company.netlify.app"]

CORS_ALLOW_METHODS = [
'DELETE',
'GET',
'OPTIONS',
'PATCH',
'POST',
'PUT',
]


CORS_ALLOW_HEADERS = [
'accept',
'accept-encoding',
'authorization',
'content-type',
'dnt',
'origin',
'user-agent',
'x-csrftoken',
'x-requested-with',
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE =  'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),

]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'pharmacy_auth.User'

AUTHENTICATION_BACKENDS = ['pharmacy_auth.backends.EmailBackend',
                            'django.contrib.auth.backends.ModelBackend',
                            'allauth.account.auth_backends.AuthenticationBackend',
    ]

LANGUAGES = [
    ('en', _('English')),
    ('ja', _('Japanese')),
]

USE_I18N = True
USE_L10N = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

#Celery

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_DEFAULT_QUEUE = 'pharmacy'
CELERY_TASK_DEFAULT_QUEUE = 'pharmacy'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'sms'

CELERY_TIMEZONE = 'Asia/Kolkata'

# ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD ="email"

# INTERNAL_IPS = [
#     "127.0.0.1",
# ]

# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": lambda request: True,
# }
CRONJOBS = [("30 13 * * *", "cron.reservationsat7am"),("30 13 * * *", "cron.reservationsat7"),("30 18 * * *", "cron.reservationsat12"),("0 8 * * *", "cron.testAPI")]