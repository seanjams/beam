import logging
import sys

from config import app, RUN_SCHEDULER
from db import db
from jobs import check_for_daily_kings_game
from routes import init_routes
from scheduler import everyday_at_4am, scheduler

# init logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("beam.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# init db
db.init_app(app)
with app.app_context():
    db.create_all()

# init routes
init_routes(app)

# init scheduler (not called when running flask shell)
def schedule_jobs():
    scheduler.init_app(app)
    scheduler.start()
    if scheduler.get_job("check_for_daily_kings_game"):
        return
    # add job
    scheduler.add_job(
        id="check_for_daily_kings_game",
        func=check_for_daily_kings_game,
        **everyday_at_4am
    )
    # run once right away
    scheduler.run_job("check_for_daily_kings_game")

# run app with ./run.sh script
if RUN_SCHEDULER:
    schedule_jobs()

# run app in development
if __name__ == "__main__":
    schedule_jobs()
    app.run()
