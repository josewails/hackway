import dj_database_url
from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')

DATABASES = {}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

HACKERRANK_API_KEY = os.environ['HACKERRANK_API_KEY']

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['BUCKET_NAME']

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
AWS_S3_HOST = 's3.us-east-1.amazonaws.com'

AWS_QUERYSTRING_AUTH = False
