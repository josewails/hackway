import dj_database_url
from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')

DATABASES = {
    'default': {}
}

DEBUG = int(os.environ.get('DEBUG').strip())

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = 'defoot'

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
AWS_S3_HOST='s3.us-east-2.amazonaws.com'

AWS_QUERYSTRING_AUTH=True

CORS_ORIGIN_WHITELIST = (
    'google.com',
    'https://defoot.herokuapp.com'
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
