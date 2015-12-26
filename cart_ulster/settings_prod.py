"""
Django settings for cart project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.core.exceptions import ImproperlyConfigured
import os
import json
import re
try:
    from . import VERSION as SITE_VERSION # used in templates to display site version
    SITE_VERSION = SITE_VERSION[0]
except ImportError:
    SITE_VERSION = ''
try:
    from ims import VERSION as IMS_VERSION # used in templates to display ims version
    IMS_VERSION=IMS_VERSION[0]
except ImportError:
    IMS_VERSION=''
from getpass import getuser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_NAME = BASE_DIR.rsplit(os.sep,1)[-1]
# JSON secrets module
with open(os.path.join(BASE_DIR, '.cart_ulster_secret.json')) as f:
    secrets=json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """
    get the secret setting or return explicit exception
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable in the secret file".format(setting)
        raise ImproperlyConfigured(error_msg)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

PICTURE_SIZE = 600
THUMBNAIL_SIZE = 90
PAGE_SIZE = 20
PRODUCT_INFORMATION_FORM_ADDED_FIELDS = ['warehouseLocation',
                'canExpire', 'expirationDate', 'expirationNotes', 'costPerItem',
                'picture']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('CART_ULSTER_SECRET')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

#ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['.cart.ulstercorps.org',]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ims',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# add request so we can access request url in 404 handler page
TEMPLATE_CONTEXT_PROCESSORS = (
"django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"django.core.context_processors.request"
)

ROOT_URLCONF = 'cart_ulster.urls'

WSGI_APPLICATION = 'cart_ulster.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret('CART_ULSTER_DB'),
        'USER': get_secret('CART_ULSTER_DB_USER'),
        'PASSWORD': get_secret('CART_ULSTER_DB_PASS'),
        'HOST': 'localhost',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL='/accounts/login'
#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_secret('CART_ULSTER_EMAIL_HOST')
EMAIL_PORT = 465
EMAIL_HOST_USER = get_secret('CART_ULSTER_EMAIL_HOST_USER')
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = get_secret('CART_ULSTER_EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = '/home3/ulsterc3/public_html/subdomains/cart/ulster/static'
MEDIA_ROOT = '/home3/ulsterc3/public_html/subdomains/cart/ulster/uploads'
MEDIA_URL = '/uploads/'
STATIC_URL = '/static/'

TEMP_DIR = '/tmp'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/home3/ulsterc3/Rob/python27/lib/python2.7/site-packages/ims/static',
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates'),
                '/home3/ulsterc3/Rob/python27/lib/python2.7/site-packages/ims/templates',]
# SITE_ADMIN will display as contact person on each page
SITE_ADMIN = ('Rob Groves','robert.groves@redcross.org')
# add other admins if you like to be contacted in case of errors
ADMINS = (SITE_ADMIN,)

SITE_MANAGER = ('Rob Groves','robert.groves@redcross.org')
# managers get notified of 404 errors and possibly other minor iussues
MANAGERS = (SITE_MANAGER,)
EMAIL_SUBJECT_PREFIX = '[CART-ULSTER]'

DJANGO_LOG_FILE=os.path.join(BASE_DIR, 'log/' + getuser()+ '_django.log')
IMS_LOG_FILE=os.path.join(BASE_DIR, 'log/' + getuser()+ '_ims.log')
LOG_FILES= (
            DJANGO_LOG_FILE,
            IMS_LOG_FILE,
            )


IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)
# Logging setup
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
                   'verbose': {
                               'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                               'datefmt' : "%d/%b/%Y %H:%M:%S"
                               },
                   'simple': {
                              'format': '%(levelname)s %(message)s'
                              },
                   },
    'handlers': {
                 'django_file': {
                          'level': 'INFO',
                          'class': 'logging.handlers.RotatingFileHandler',
                          'filename': DJANGO_LOG_FILE,
                          'formatter': 'verbose',
                          'maxBytes':1048576,
                          'backupCount':10,
                          },
                 'ims_file': {
                                  'level': 'DEBUG',
                                  'class': 'logging.handlers.RotatingFileHandler',
                                  'filename': IMS_LOG_FILE,
                                  'formatter': 'verbose',
                                  'maxBytes':1048576,
                                  'backupCount':10,
                                  },
                 'mail_admins': {
                                 'level': 'ERROR',
                                 'class': 'django.utils.log.AdminEmailHandler',
                                 'include_html': True,
                                 }
                 
                 },
    'loggers': {
                'django': {
                           'handlers':['django_file','mail_admins',],
                           'propagate': True,
                           'level':'DEBUG',
                           },
                'ims': {
                           'handlers':['ims_file','mail_admins',],
                           'propagate': False,
                           'level':'DEBUG',
                           },
                }
}
