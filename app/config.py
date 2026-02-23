import os

class Config:
    # base configuration class
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    
class DevelopmentConfig(Config):
    # development configuration class
    SQLALCHEMY_DATABASE_URI = 'sqlite:///school_library.db'
    DEBUG = True
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')


class ProductionConfig(Config):
    # production configuration class
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    


config ={
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    "default": DevelopmentConfig
}