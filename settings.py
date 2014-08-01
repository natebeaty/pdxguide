# Django settings for pdxguide project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEFAULT_CHARSET = 'utf-8'

ADMINS = (
    ('Nate Beaty', 'natebeaty@gmail.com'),
)

MANAGERS = (
    ('Nate Beaty', 'nate@clixel.com'),
    ('Shawn Granton', 'tfrindustries@gmail.com'),
)

DATABASE_ENGINE = 'mysql_old'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'pdxguide'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
TIME_ZONE = 'America/Portland'

# Language code for this installation. All choices can be found here:
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
SITE_URL = 'pdxguide.org'
SERVER_EMAIL = 'www@%s' % SITE_URL

# Absolute path to the directory that holds media.
MEDIA_ROOT = '/var/www/pdxguide.org/public_html/media/'

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'pdxguide.middleware.threadlocals.ThreadLocals', 
)

ROOT_URLCONF = 'pdxguide.urls'

TEMPLATE_DIRS = (
    '/home/natebeaty/django/django_projects/pdxguide/templates',

)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.flatpages',
    'django.contrib.markup',
	'pdxguide.guide',
	'pdxguide.tags',
)

CACHE_BACKEND = 'db://cache'
CACHE_MIDDLEWARE_SECONDS = 86400
CACHE_MIDDLEWARE_KEY_PREFIX = 'pdxguide'

# Custom global variables
YAHOO_ID = ''
GOOGLE_ID = ''
