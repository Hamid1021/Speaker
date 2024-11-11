"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h-2z_0qp9p-e0aq#$uy7t1s_+*^c%$1%qjivui4$t#zx$#(^cb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

if DEBUG:
    ALLOWED_HOSTS = ["*"]
    
    # Database
    # https://docs.djangoproject.com/en/5.1/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    STATIC_ROOT = BASE_DIR / 'static/'
    MEDIA_ROOT = BASE_DIR / 'media/'
else:
    ALLOWED_HOSTS = [
        '91.207.205.38', 'https://server.ir', 'http://server.ir', 'server.ir',
        'https://www.server.ir', 'http://www.server.ir', 'www.server.ir',
    ]
    # Database
    # https://docs.djangoproject.com/en/5.0/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': "",
            'USER': "",
            'PASSWORD': "",
            'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
            'PORT': '3306',
            'OPTIONS': {
                'sql_mode': 'STRICT_ALL_TABLES',
                'charset': 'utf8mb4'
            },
        }
    }
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': '',
    #         'USER': '',
    #         'PASSWORD': '',
    #         'HOST': '127.0.0.1',
    #         'PORT': '5432',
    #     }
    # }
    STATIC_ROOT = "/home/cp39649/public_html/static"
    MEDIA_ROOT = "/home/cp39649/public_html/media"


# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True

AUTH_USER_MODEL = "account.USER"

X_FRAME_OPTIONS = 'ALLOW-FROM 127.0.0.1'

CKEDITOR_FORCE_JPEG_COMPRESSION = True
CKEDITOR_IMAGE_QUALITY = 50
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_IMAGE_BACKEND = 'ckeditor_uploader.backends.PillowBackend'
CKEDITOR_FILENAME_GENERATOR = 'utils.get_filename'
CKEDITOR_UPLOAD_PATH = "upload/"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

CKEDITOR_CONFIGS = {
    'page_editor': {
        'toolbar': 'full',
    },
    'default': {
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': [
                'Source', 'Undo', 'Redo', 'Bold', 'Italic', 'Underline',
                'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat',
                'TextColor', 'BGColor',
                'Maximize',  # 'Preview',
            ]},
            {'name': 'paragraph',
             'items': [  # 'NumberedList', 'BulletedList',
                 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-',
                 '-', 'Outdent', 'Indent', '-', 'Blockquote', '-',
                 'BidiLtr', 'BidiRtl', ]
             },
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert', 'items': [
                'Image', 'Html5video', 'HorizontalRule', 'SpecialChar', 'PageBreak',
                'Styles', 'Format', 'Font', 'FontSize',
            ]},
            # '/',  # put this to force next toolbar on new line
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
            'html5video',
        ]),
        "removePlugins": "tableselection,tabletools,liststyle,contextmenu ",
    }
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Extension
    'django_render_partial',
    'ckeditor',
    'ckeditor_uploader',
    "extensions",
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'widget_tweaks',
    
    # Added Application
    "account.apps.AccountConfig",
    "application.apps.ApplicationConfig",
    'map_xml.apps.MapXmlConfig',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates/', os.path.join(BASE_DIR, "templates/")],
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
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / 'assets',
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_EMAIL = 'myemain@myemain.ir',
# EMAIL_HOST = 'mail.myemain.ir'
# EMAIL_USE_TLS = False
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'myemain'
# EMAIL_HOST_PASSWORD = ''