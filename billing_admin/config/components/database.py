import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME_ADMIN'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST_ADMIN', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT_ADMIN', '5432'),
        'OPTIONS': {
            'options': '-c search_path=public,billing'
        }
    }
}
