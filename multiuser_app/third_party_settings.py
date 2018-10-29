
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