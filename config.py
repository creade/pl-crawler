import os

os_env = os.environ

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os_env.get('PL_CRAWL_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os_env.get('DATABASE_URL','postgresql://localhost/pl_crawl')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os_env.get('TEST_DATABASE_URL','postgresql://localhost/pl_crawl_test')
