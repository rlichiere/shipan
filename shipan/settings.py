"""
Django settings for shipan project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4wurshcnjlg)sw#5+e)bi5j1z)lx26ae^m^6z1k(4@wuj8o)8v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
   'django.contrib.admin',
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.messages',
   'django.contrib.staticfiles',
   'people.apps.PeopleConfig',
   'backoffice.apps.BackofficeConfig',
   'frontoffice.apps.FrontofficeConfig',
   'docutils',
   'rest_framework',
   'widget_tweaks',
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

ROOT_URLCONF = 'shipan.urls'

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

WSGI_APPLICATION = 'shipan.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
   'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
}


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

AUTHENTICATION_BACKENDS = (
   'people.auth_backends.CustomUserModelBackend',
)

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
STATIC_ROOT = '%s/static/' % BASE_DIR
# STATICFILES_DIRS = [
#    'static'
# ]


CUSTOM_USER_MODEL = 'people.Client'


# Login Redirect
LOGIN_URL = 'fo-home'
LOGIN_REDIRECT_URL = 'fo-home'


def skip_static_requests(record):
   if len(record.args) > 0:
      if (record.args[0].find('GET /static/') >= 0) or (record.args[0].find('GET /favicon.ico ') >= 0):
         return False
   return True

# Logging Settings
LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'filters': {
      'skip_static_requests': {
         '()': 'django.utils.log.CallbackFilter',
         'callback': skip_static_requests
      }
   },
   'formatters': {
      'custom': {
         'format': '%(levelname)s %(message)s'
      },
      'colored': {
         '()': 'colorlog.ColoredFormatter',
         'format': "%(log_color)s%(levelname)-8s%(reset)s %(cyan)s%(name)-10s%(reset)s %(message_log_color)s%(message)s",
         'secondary_log_colors': {
		      'message': {
			      'ERROR':    'white,bg_red',
			      'CRITICAL': 'white,bg_red'
		      },
            'levelname': {
               'ERROR':    'white,bg_red',
               'CRITICAL': 'white,bg_red'
            }
         }
      },
      'colored_sql': {
         '()': 'colorlog.ColoredFormatter',
         'format': "%(log_color)s%(levelname)-8s%(reset)s %(cyan)s%(duration)-10s%(reset)s %(message_log_color)s%(sql)s",
         'secondary_log_colors': {
		      'message': {
			      'ERROR':    'white,bg_red',
			      'CRITICAL': 'white,bg_red'
		      },
            'levelname': {
               'ERROR':    'white,bg_red',
               'CRITICAL': 'white,bg_red'
            }
         }
      }
   },
   'handlers': {
      'console': {
         'level': 'DEBUG',
         'class': 'logging.StreamHandler',
         'formatter': 'colored',
         'filters': ['skip_static_requests'],
      },
      'console_sql': {
         'level': 'DEBUG',
         'class': 'logging.StreamHandler',
         'formatter': 'colored_sql',
      },
   },
   'loggers': {
      # 'django': {
      #    'handlers': ['console'],
      #    'level': 'ERROR',
      #    'propagate': True,
      # },

      # 'django.db.backends': {
      #    'handlers': ['console_sql'],
      #    'level': 'DEBUG',
      #    'propagate': False,
      # },
      'django.server': {
         'handlers': ['console'],
         'level': 'DEBUG',
         'propagate': False,
      },
      'shipan': {
         'handlers': ['console'],
         'level': os.environ.get('LOG_LEVEL', 'INFO'),
      },
   },
}

DJANGO_COLORS='light'
