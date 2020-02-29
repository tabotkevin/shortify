import os

SECRET_KEY = 'top-secret!'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
REDIS_URL = os.environ.get('REDIS_URL')
