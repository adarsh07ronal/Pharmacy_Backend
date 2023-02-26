from .base import *

DEBUG = True

#ALLOWED_HOSTS = ['dev-pharmacy.eoraa.com',"http://localhost:3000","localhost"]
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('SQL_ENGINE',
#                                  'django.db.backends.postgresql'
#                                  ),
#         'NAME': os.environ.get('SQL_DATABASE', ''),
#         'USER': os.environ.get('SQL_USER', ''),
#         'PASSWORD': os.environ.get('SQL_PASSWORD', ''),
#         'HOST': os.environ.get('SQL_HOST', 'localhost'),
#         'PORT': os.environ.get('SQL_PORT', '5432'),
#     }
# }

ELASTICSEARCH_DSL = {
    "default" : {"hosts":"esearch:9200"}
}
