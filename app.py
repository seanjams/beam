from flask import Flask
import logging

from config import Config
from db import db
from jobs import check_for_daily_kings_game
from routes import init_routes
from scheduler import scheduler, everyday_at_noon

# init logging
logging.basicConfig(filename="beam.log", level=logging.INFO)

# create app
app = Flask(__name__)
app.config.from_object(Config())

# init db
db.init_app(app)
with app.app_context():
    db.create_all()

# init scheduler
scheduler.init_app(app)
scheduler.add_job(
    id="check_for_daily_kings_game",
    func=check_for_daily_kings_game,
    **everyday_at_noon
)
scheduler.start()

# init routes
init_routes(app)

# run app
if __name__ == "__main__":
    app.run()
    # run job on startup
    # scheduler.run_job("check_for_daily_kings_game")
