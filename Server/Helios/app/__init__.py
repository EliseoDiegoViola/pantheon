from flask import Flask
from configs import config

app = Flask(__name__)
app.config.from_object('configs.config.DevelopmentConfig')


from app import routes
