class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://clowncore:clowncoreM&a@clowncore.c144myww860a.ap-south-1.rds.amazonaws.com:5432/postgres'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'your_production_database_uri'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
