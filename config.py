import os

# DB url
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")

# HUE Config
HUE_BRIDGE_IP = os.getenv("HUE_BRIDGE_IP")
HUE_BRIDGE_USERNAME = os.getenv("HUE_BRIDGE_IP")

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
