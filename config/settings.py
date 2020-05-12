import os
import environ
from decouple import Csv, config
import datetime
import logging
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Main project directory adesua/
ROOT_PATH = environ.Path(__file__) -2

# public directory adesua-api/api
PUBLIC_PATH = ROOT_PATH.path('api')

env = environ.Env()
env.read_env('.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# Application definition
THIRD_PARTY_APPS = [
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',
    'rest_framework',
    'rest_auth.registration',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_framework_jwt',
    'corsheaders',
    'django_extensions',
    'storages',
    'django_q',
    'djmoney',
    'phonenumber_field',
]

MY_APPS = [
    # general apps
    'api.users',
    'api.wallet',
    'api.tolls',
    'api.vehicles',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + MY_APPS

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(PUBLIC_PATH('templates'))],
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

WSGI_APPLICATION = 'config.wsgi.application'

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

AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]

DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///buildforsdgdb'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# redis caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

# for cors header
CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', [])

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LTIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 35
}

# JWT CUSTOM DEFAULTS
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=360),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=360),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

# Activating the Custom Serializers
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'api.users.custom_registration.CustomRegistrationSerializer',
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'api.users.serializers.UserDetailModelSerializer',
    'PASSWORD_RESET_SERIALIZER': 'api.users.password_serializer.PasswordResetSerializer'
}

# rest framework docs
# REST_FRAMEWORK_DOCS = {
#     'HIDE_DOCS': config('HIDE_DRFDOCS', False)
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    str(PUBLIC_PATH('static')),
]

STATIC_ROOT = str(ROOT_PATH('staticfiles'))

MEDIA_URL = '/media/'
MEDIA_ROOT = str(ROOT_PATH('media'))

# authentication defaults
# auth settings
ACCOUNT_ADAPTER = 'api.users.adapters.AccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 365
ACCOUNT_ALLOW_REGISTRATION = True
LOGOUT_ON_PASSWORD_CHANGE = False
LOGIN_URL = 'account_login'
AUTH_USER_MODEL = 'users.User'
REST_USE_JWT = True

# email configuration
DEFAULT_FROM_EMAIL = 'Revenue <noreply@revenue.com.gh>'
EMAIL_SUBJECT_PREFIX = 'Revenue'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = env('SENDGRID_API_KEY')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

if not DEBUG:
    # S3 Setup
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'api/static'),
    ]


FRONTEND_URL = env('FRONTEND_URL', default='http://localhost:8081')
ADMIN_URL = env('ADMIN_URL', default='http://localhost:8080')

ADMINS = [('WahabAwudu', 'wahabawudu2020@gmail.com'),]
# Logging ==========================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

# sentry for loggin in production
SENTRY_DSN = env('SENTRY_DSN')
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", default=logging.INFO)

ENVIRONMENT = env('ENVIRONMENT', default='local')

if not ENVIRONMENT == 'local':
    sentry_logging = LoggingIntegration(
        level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[sentry_logging, DjangoIntegration()],
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

# PAYSTACK API KEYS
PAYSTACK_SECRET = env.str('PAYSTACK_SECRET')
PAYSTACK_PUBLIC = env.str('PAYSTACK_PUBLIC')

# heroku specific
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
