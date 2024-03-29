from flask import Flask
import os


class NoHueBridgeCredentials(Exception):
    pass

# DB url
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")

# Should run scheduler on startup
RUN_SCHEDULER = os.getenv("RUN_SCHEDULER")

# HUE Config
HUE_BRIDGE_IP = os.getenv("HUE_BRIDGE_IP")
HUE_BRIDGE_USERNAME = os.getenv("HUE_BRIDGE_USERNAME")
if not HUE_BRIDGE_IP or not HUE_BRIDGE_USERNAME:
    raise NoHueBridgeCredentials(
        "No HUE_BRIDGE_IP and HUE_BRIDGE_USERNAME variables found in environment. Aborting."
    )

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL

# create app
app = Flask(__name__)
app.config.from_object(Config())
