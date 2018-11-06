import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

installed_apps = [
    'debug_toolbar',
]


MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'confession',
        'USER': 'root',
        'PASSWORD': 'ashwani1',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

MY_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(base_dir, 'db.sqlite3'),
    }
}