import dj_database_url
from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')

DATABASES = {
    'default': {}
}

DEBUG = int(os.environ.get('DEBUG').strip())

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['BUCKET-NAME']

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATIC_URL = 'https://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
AWS_S3_HOST='s3.us-east-2.amazonaws.com'

