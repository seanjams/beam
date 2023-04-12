import logging
import sys

from app import app
from db import db
from jobs import check_for_daily_kings_game
from routes import init_routes
from scheduler import scheduler, everyday_at_noon

# init logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("beam.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
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

    # kick off initial job
    scheduler.run_job("check_for_daily_kings_game")
    return app

# run app
if __name__ == "__main__":
    # run job on startup
    main()
    app.run()
