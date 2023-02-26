from pickle import TRUE
from .base import *

DEBUG = True

#ALLOWED_HOSTS = ['dev-pharmacy.eoraa.com',"localhost","http://localhost:3000"]
#ALLOWED_HOSTS = ['https://dev-pharmacy.eoraa.com',"http://localhost:3000","localhost"]
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('SQL_ENGINE',
#                                  'django.db.backends.postgresql'
#                                  ),
#         'NAME': os.environ.get('SQL_DATABASE', 'postgres'),
#         'USER': os.environ.get('SQL_USER', 'postgres'),
#         # 'PASSWORD': os.environ.get('SQL_PASSWORD', ''),
#         'HOST': os.environ.get('SQL_HOST', 'pharmacy.ckovfasq13ub.us-east-2.rds.amazonaws.com'),
#         'PORT': os.environ.get('SQL_PORT', '5432'),
#     }
# }