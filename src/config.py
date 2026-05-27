import os

class Config:
    """Base configuration settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')
    PORT = int(os.environ.get('PORT', 19191))
    HOST = os.environ.get('HOST', '0.0.0.0')
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')

class ProductionConfig(Config):
    """Production configuration settings."""
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration settings."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration settings."""
    TESTING = True
    DEBUG = True
