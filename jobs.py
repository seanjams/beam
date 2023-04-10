import pendulum
import logging
from db import db, JobRun, JobStatus
from hue import light_the_beam, reset_beam
from nba import fetch_kings_game, game_winner
from scheduler import scheduler, every_ten_minutes

log = logging.getLogger(__name__)


# add better logging
def check_for_winner():
    log.info("Checking for winner...")

    todays_date = pendulum.now("US/Pacific").format("YYYY-MM-DD")
    response = fetch_kings_game(todays_date)
    if response["status"] == "success":
        job_status = JobStatus.success
        winner = game_winner(response["game"])
        if winner and winner == "Kings":
            log.info("KINGS WIN!! LIGHT THE BEAM!!!")
            light_the_beam()
        elif winner:
            log.info("Kings Lose :(")
            reset_beam()
        else:
            log.info("No winner yet...")
            reset_beam()
    else:
        # No action on light (for now)
        job_status = JobStatus.error

    # save new job run to DB
    run = JobRun(
        name="check_for_winner",
        status=job_status
    )
    run.save()


# add better logging
def check_for_daily_kings_game():
    log.info("Checking for daily game...")

    todays_date = pendulum.now("US/Pacific").format("YYYY-MM-DD")
    response = fetch_kings_game(todays_date)
    if response["status"] == "success":
        job_status = JobStatus.success

        # start/stop polling interval job
        if response["game"]:
            log.info("Found Kings game.")
            scheduler.add_job(
                id="check_for_winner",
                func=check_for_winner,
                **every_ten_minutes
            )
        else:
            log.info("No Kings game found.")
            if scheduler.get_job("check_for_winner"):
                scheduler.delete_job(id="check_for_winner")
            reset_beam()
    else:
        job_status = JobStatus.error
    
    # save new job run to DB
    run = JobRun(
        name="check_for_daily_kings_game",
        status=job_status
    )
    run.save()
