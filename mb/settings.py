from django.core.exceptions import ImproperlyConfigured

"""
Django settings for mb project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Check the mode in which this django should be run.
DJ_MODE_ALL_LOCAL = 0  # simple testing with sqlite and local files
DJ_MODE_GOOGLE_APPLICATION_ENGINE = 1 # production on gae
DJ_MODE_DJ_LOCAL_STATIC_DB_GOOGLE = 2 # run local with some google api

if os.getenv('GAE_INSTANCE'):
    RUNNING_MODE = DJ_MODE_GOOGLE_APPLICATION_ENGINE
else:
    dj_mode = os.getenv('DJANGO_MODE')
    if dj_mode == 'local+googledb':
        RUNNING_MODE = DJ_MODE_DJ_LOCAL_STATIC_DB_GOOGLE
    elif dj_mode == 'local':
        RUNNING_MODE = DJ_MODE_ALL_LOCAL
    else:
        raise ImproperlyConfigured("Can't figure out a mode to run.")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deploymen/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '**************************************************'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if RUNNING_MODE == DJ_MODE_GOOGLE_APPLICATION_ENGINE:
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
    'address.apps.AddressConfig',
    'agenda.apps.AgendaConfig',
    'client.apps.ClientConfig',
    'orders.apps.OrdersConfig',
    'ingredients.apps.IngredientsConfig',
    'food.apps.FoodConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # added for translations
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'orders.middleware.CartMiddleware',
]

ROOT_URLCONF = 'mb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mb.context_processors.side_wide_vars',
            ],
        },
    },
]

WSGI_APPLICATION = 'mb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
if RUNNING_MODE == DJ_MODE_ALL_LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
elif RUNNING_MODE in (DJ_MODE_DJ_LOCAL_STATIC_DB_GOOGLE,
                      DJ_MODE_GOOGLE_APPLICATION_ENGINE):
    DATABASES = {
        'default': {
            # If you are using Cloud SQL for MySQL rather than PostgreSQL, set
            # 'ENGINE': 'django.db.backends.mysql' instead of the following.
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mb_db',
            'USER': 'madam_site',
            'PASSWORD': 'test',
        }
    }

# In the flexible environment, you connect to CloudSQL using a unix socket.
# Locally, you can use the CloudSQL proxy to proxy a localhost connection
# to the instance
# mag normaal weg DATABASES['default']['HOST'] = '/cloudsql/madam-bocal-dev:europe-west1:madame-bocal'
if RUNNING_MODE == DJ_MODE_GOOGLE_APPLICATION_ENGINE:
    DATABASES['default']['HOST'] = '/cloudsql/madam-bocal-dev:europe-west1:madame-bocal'
elif RUNNING_MODE == DJ_MODE_DJ_LOCAL_STATIC_DB_GOOGLE:
    DATABASES['default']['HOST'] = '127.0.0.1'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'nl-BE'
#LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'static', '')
STATIC_ROOT = '/tmp/madam_bocal/static/'
if RUNNING_MODE == DJ_MODE_ALL_LOCAL:
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'site-wide-static')
    ]
    MEDIA_ROOT = '/var/www/mabo/media/'
    MEDIA_URL = '/var/www/mabo/media/'
elif RUNNING_MODE in (DJ_MODE_DJ_LOCAL_STATIC_DB_GOOGLE,
                      DJ_MODE_GOOGLE_APPLICATION_ENGINE):

# Using the google cloud storage for serving static content and media
# files
# To acces the GCS data I can use the urls.
# To use the GCS to store media uploaded by clients you have to pip
# install some packages and define some settings.
# The packages are google-cloud (the google cloud python package) and
# django-storages which gives you the gcloud storage backend.

# setting to use the gcloud storage by default
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# define your bucket name
    GS_BUCKET_NAME = 'madam-bocal-dev'

# Adding a path a static folder in the base directory
    # STATICFILES_DIRS = [
    #     os.path.join(BASE_DIR, 'site-wide-static')
    # ]


    STATIC_URL = 'https://storage.googleapis.com/madam-bocal-dev/static/'

    MEDIA_ROOT = '/var/www/mabo/media/'
    MEDIA_URL = 'https://storage.googleapis.com/madam-bocal-dev/media/'
               # change this for production side to a real url e.g.
#MEDIA_URL = 'www.madamebocal.be/'

########### my adding

# change standard redirect from log-in page
# https://docs.djangoproject.com/en/1.10/topics/auth/default/
LOGIN_REDIRECT_URL = '/'

# setup smtp mail
# https://docs.djangoproject.com/en/1.10/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.fusemail.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = '*******************'
EMAIL_HOST_PASSWORD = '****************'
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'info@roce.be'

MENU_NAME = 'top'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': ' %(name)s:%(levelname)s -> %(message)s'
        },
        'timed': {
            'format': '%(asctime)s: %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/dj_debug.log',
        },
        'client_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/tmp/client.log',
            'formatter': 'timed',
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['file'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
        'client': {
            'handlers': ['client_info', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
