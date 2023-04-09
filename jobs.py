import pendulum
from app import app
from db import db, JobRun, JobStatus
from hue import light_the_beam, reset_beam
from nba import fetch_kings_game, game_winner
from scheduler import scheduler


# add better logging
def check_for_winner():
    print("LIGHT THE BEAM")

    todays_date = pendulum.now("US/Pacific").format("YYYY-MM-DD")
    response = fetch_kings_game(todays_date)
    if response["status"] == "success":
        job_status = JobStatus.success

        winner = game_winner(response["game"])
        if winner and winner == "Kings":
            light_the_beam()
        else:
            reset_beam()

        
    else:
        job_status = JobStatus.error
        reset_beam()

    # save new job run to DB
    with app.app_context():
        run = JobRun(
            name="check_for_winner",
            status=job_status
        )
        db.session.add(run)
        db.session.commit()


# add better logging
def check_for_daily_kings_game():
    print("CHECKING FOR DAILY GAME")

    todays_date = pendulum.now("US/Pacific").format("YYYY-MM-DD")
    response = fetch_kings_game(todays_date)
    if response["status"] == "success":
        job_status = JobStatus.success

        # start/stop polling interval job
        if response["game"]:
            scheduler.add_job(
                id="check_for_winner",
                func=check_for_winner,
                trigger="interval",
                seconds=10,
                misfire_grace_time=900,
            )
        else:
            scheduler.delete_job(id="check_for_winner")
            reset_beam()
    else:
        job_status = JobStatus.error
        
    
    # save new job run to DB
    with app.app_context():
        run = JobRun(
            name="check_for_daily_kings_game",
            status=job_status
        )
        db.session.add(run)
        db.session.commit()
