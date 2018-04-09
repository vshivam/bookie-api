# /instance/config.py


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = "BOOKIE-AMAZING-SECRET"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:super_amazing_password@localhost:5432/flask_api"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
