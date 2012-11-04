# Django settings for wh3 project.
import dj_database_url
import django.template

import os.path
PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.normpath(__file__)), '..')) # wh3/..
def proj_rel(path):
    return os.path.realpath(os.path.join(PROJECT_ROOT, path)) # PROJECT_ROOT/path

AUTH_USER_MODEL = 'auth.User'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///sqlite3.db')
    #'default': {
        #'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': '',                      # Or path to database file if using sqlite3.
        #'USER': '',                      # Not used with sqlite3.
        #'PASSWORD': '',                  # Not used with sqlite3.
        #'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        #'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    #}
}

TIME_ZONE = 'America/Los_Angeles'

LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False # not needed
USE_L10N = True
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

STATIC_ROOT = proj_rel('static/')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    proj_rel('assets'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'fflu@&amp;_-6ag=5j$c3!vq2#8&amp;8kz5j1wzq*814x0^a-40x1#z9u'

TEMPLATE_DIRS = (
    proj_rel('templates/'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'wh3.urls'
WSGI_APPLICATION = 'wh3.wsgi.application'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'auth', 'blog','contact',
)

# allow {% unl 'something' %} inside of templates
django.template.add_to_builtins('django.templatetags.future')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
