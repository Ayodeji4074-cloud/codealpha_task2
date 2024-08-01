import os
#python path of our database to help locate db during initialization and migration
basedir = os.path.abspath(os.path.dirname(__file__))
# app configurations
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '8738f0d1ae2326ea776afb788444db241684a5a8e98c58acf9ff551dd49aedbf'
    SECRET_KEY='220fb3bffffe107c384c33fd1bb6eed4'
    
# test configurations
class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '8738f0d1ae2326ea776afb788444db241684a5a8e98c58acf9ff551dd49aedbf'
    SECRET_KEY='220fb3bffffe107c384c33fd1bb6eed4'