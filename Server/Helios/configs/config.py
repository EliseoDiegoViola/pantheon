class Config(object):
    DEBUG = False
    TESTING = False
    #FLASK_RUN_PORT = 13371
    MONGO_URI = "mongodb://svAdmin:Ozymandias22@localhost:27020/heliosBase?authSource=admin"

class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
    DEBUG = True




