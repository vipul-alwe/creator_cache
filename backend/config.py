import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoid overhead

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URI",
        "postgresql://clowncore:clowncoreM&a@clowncore.c144myww860a.ap-south-1.rds.amazonaws.com:5432/postgres",
    )

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI")

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
