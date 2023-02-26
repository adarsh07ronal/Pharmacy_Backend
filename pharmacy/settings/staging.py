from .base import *

DEBUG = True

# ALLOWED_HOSTS = ['https://dev-pharmacy.eoraa.com',"http://localhost:3000"]
ALLOWED_HOSTS = ['https://dev-pharmacy.eoraa.com',"http://localhost:3000","localhost","http://bs-local.com:3000/","bs-local.com"]
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE',
                                 'django.db.backends.postgresql'
                                 ),
        'NAME': os.environ.get('SQL_DATABASE', ''),
        'USER': os.environ.get('SQL_USER', ''),
        'PASSWORD': os.environ.get('SQL_PASSWORD', ''),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}
