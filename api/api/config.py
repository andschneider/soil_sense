from os import getenv


class Config:
    SECRET_KEY = getenv("SECRET_KEY", "hard to guess string")
    JWT_SECRET_KEY = getenv("SECRET_KEY", "super secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_DEV_URL")


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_TEST_URL")


class ProductionConfig(Config):
    """Production configuration"""

    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
