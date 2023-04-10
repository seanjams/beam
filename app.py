from flask import Flask

from config import Config

# create app
app = Flask(__name__)
app.config.from_object(Config())
