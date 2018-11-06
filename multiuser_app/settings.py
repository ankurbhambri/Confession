"""
Django settings for multiuser_app project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import datetime

global FLAG
FLAG = True
try:
    from .third_party_settings import *
except Exception:
    FLAG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o&d_1p0-wd@*co2ccvjxqom-rzk0c%wy%ite0jd$2ayt(#&dg='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["ashwani64.pythonanywhere.com", "127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'crispy_forms',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',

    'blog',
    'notifications',
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


ROOT_URLCONF = 'multiuser_app.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'multiuser_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = MY_DATABASE


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {
                'name': 'document',
                'items': ['Save', 'Preview', 'Print', '-', 'Templates']
            },
            {
                'name': 'clipboard',
                'items': ['Cut', 'Copy', 'Paste', '-', 'Undo', 'Redo']
            },
            {
                'name': 'editing',
                'items': ['Find', 'Replace', '-', 'SelectAll']
            },
            {
                'name': 'forms',
                'items': ['Form', 'Checkbox', 'Radio', 'TextField',
                          'Textarea', 'Select', 'Button', 'ImageButton',
                          'HiddenField'
                          ]
            },
            '/',
            {
                'name': 'basicstyles',
                'items': ['Bold', 'Italic', 'Underline', 'Strike',
                          'Subscript', 'Superscript', '-', 'RemoveFormat'
                          ]
            },
            {
                'name': 'paragraph',
                'items': ['NumberedList', 'BulletedList', '-', 'Outdent',
                          'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                          'JustifyLeft', 'JustifyCenter', 'JustifyRight',
                          'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                          'Language'
                          ]
            },
            {
                'name': 'links',
                'items': ['Link', 'Unlink', 'Anchor']
            },
            {
                'name': 'insert',
                'items': ['Image', 'Flash', 'Table', 'HorizontalRule',
                          'Smiley', 'SpecialChar', 'PageBreak', 'Iframe'
                          ]
            },
            '/',
            {'name': 'codesnippet', 'items': ['CodeSnippet']},
            '/',
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            # 'div',
            # 'autolink',
            # 'autoembed',
            # 'embedsemantic',
            # 'autogrow',
            # 'devtools',
            'codesnippet',
            # 'widget',
            # 'lineutils',
            # 'clipboard',
            # 'dialog',
            # 'dialogui',
            # 'elementspath'
        ]),
    }
}
CKEDITOR_BROWSE_SHOW_DIRS = False

AUTH_USER_MODEL = 'blog.User'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'post_list'
LOGOUT_REDIRECT_URL = 'home'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}

JWT_AUTH = {
    "JWT_VERIFY": True,
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
    "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=7200)
}

try:
    if DEBUG and FLAG:
        INSTALLED_APPS += installed_apps
        MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

        DEBUG_TOOLBAR_PANELS = [
            'debug_toolbar.panels.versions.VersionsPanel',
            'debug_toolbar.panels.timer.TimerPanel',
            'debug_toolbar.panels.settings.SettingsPanel',
            'debug_toolbar.panels.headers.HeadersPanel',
            'debug_toolbar.panels.request.RequestPanel',
            'debug_toolbar.panels.sql.SQLPanel',
            'debug_toolbar.panels.staticfiles.StaticFilesPanel',
            'debug_toolbar.panels.templates.TemplatesPanel',
            'debug_toolbar.panels.cache.CachePanel',
            'debug_toolbar.panels.signals.SignalsPanel',
            'debug_toolbar.panels.logging.LoggingPanel',
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ]

        DEBUG_TOOLBAR_CONFIG = {
            'INTERCEPT_REDIRECTS': False,
        }

        def show_toolbar(request):
            return True  # Always show toolbar, for example purposes only.

        DEBUG_TOOLBAR_CONFIG = {
            'INTERCEPT_REDIRECTS': False,
            'SHOW_TOOLBAR_CALLBACK': show_toolbar,
            'HIDE_DJANGO_SQL': False,
        }

        SHOW_TOOLBAR_CALLBACK = True
except Exception:
    pass
