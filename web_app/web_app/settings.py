"""
Django settings for web_app project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

DJANGO_PROJECT_NAME = os.getenv('DJANGO_PROJECT_NAME', default='web_app'),
DJANGO_SETTINGS_MODULE = os.getenv('DJANGO_SETTINGS_MODULE', default='web_app.settings')

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-82$df-20jmx$79#d8-4gu3itq+2^16qd+%e25$#+uy%@__7+k)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "management",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_api_key',

    # AllAuth
    'allauth',
    'allauth.account',
    # # Optional -- requires install using `django-allauth[socialaccount]`.
    # 'allauth.socialaccount',
    # # ... include the providers you want to enable:
    # 'allauth.socialaccount.providers.auth0',
    # 'allauth.socialaccount.providers.odnoklassniki',
    # 'allauth.socialaccount.providers.openid',
    # 'allauth.socialaccount.providers.openid_connect',
    # 'allauth.socialaccount.providers.vk',
    # 'allauth.socialaccount.providers.yandex',

    "api",
    "input_queue",
    "organizations",
    "users",
    "user_auth",

    "web_start",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Add the account middleware for AllAuth:
    "allauth.account.middleware.AccountMiddleware",

]

ROOT_URLCONF = 'web_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Already defined Django-related contexts here
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'web_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', default='db'),
        'USER': os.getenv('DB_USER', default='dbuser'),
        'PASSWORD': os.getenv('DB_PASS', default='ZusmanAC60'),
        'HOST': os.getenv('DB_HOST', default='localhost'),
        'PORT': os.getenv('DB_PORT', default='5432')
    }
}


AUTH_USER_MODEL = 'users.User'

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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_FORMS = {
    'signup': 'user_auth.forms.CustomSignupForm',
}

ACCOUNT_ADAPTER = "user_auth.adapter.AccountAdapter"
# ACCOUNT_EMAIL_VERIFICATION = None
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"

# # AllAuth.  Provider specific settings
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # (``socialaccount`` app) containing the required client
#         # credentials, or list them here:
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     }
# }

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.AllowAny',

        # Установка глобальных разрешениний rest_framework_api_key
        # 'rest_framework_api_key.permissions.HasAPIKey',
    ]
}


API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"


DJANGO_COLORS = "light;error=yellow/blue,blink;notice=magenta"

LOG_COLOR = {
    'asctime': '{thin_light_white}[{asctime}]{reset}',
    'levelname': '{log_color}[{levelname}]{reset}',
    'module': '{thin_light_white}[{module}>{filename}>{funcName}()>{lineno}]{reset}',
    'message': '{bold}{message}{reset}',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'colored_asctime': '{thin_light_white}[{asctime}]{reset}',

    'formatters': {
        'main_format': {
            'format': '[{asctime}]-[{levelname}]-[{filename} > {module} > {funcName}() > {lineno}] - {message}', # [%(filename)s > %(funcName)s() > %(lineno)s]
            'style': '{',
        },
        'verbose': {
            '()': 'colorlog.ColoredFormatter',  # colored output
            'format': f'{LOG_COLOR["asctime"]}-{LOG_COLOR["levelname"]}-{LOG_COLOR["module"]}-{LOG_COLOR["message"]}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            # 'stream': sys.stdout,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'main': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': True,
    },
}

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {
            'db': '1',
        }
    }
}
