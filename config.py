import os

os_env = os.environ

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os_env.get('PL_CRAWL_SECRET_KEY')

class DevConfig(Config):
    DEBUG = True
