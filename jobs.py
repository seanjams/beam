import logging
import pendulum

from db import JobRun, JobStatus
from hue import light_the_beam, reset_beam, save_current_light_status
from nba import fetch_kings_game, game_winner
from scheduler import every_ten_minutes, scheduler
from utils import convert_to_pacific_tz, todays_date

log = logging.getLogger(__name__)

def check_for_winner():
    log.info("Checking for winner...")

    todays_date = pendulum.now("US/Pacific").format("YYYY-MM-DD")
    response = fetch_kings_game(todays_date)
    if response["status"] == "success":
        job_status = JobStatus.success
        winner = game_winner(response["game"])
        if winner and winner == "Kings":
            # stop polling for winner, save current light configuration,
            # and light them beam!!
            msg = "KINGS WIN!! LIGHT THE BEAM!!!"
            save_current_light_status()
            light_the_beam()
            scheduler.delete_job(id="check_for_winner")
        elif winner:
            # stop polling for winner, and be sad
            msg = "Kings Lose :("
            scheduler.delete_job(id="check_for_winner")
        else:
            msg = "No winner yet..."
    else:
        msg = f"Error, fetch_kings_game returned {response['status_code']}"
        job_status = JobStatus.error

    # save new job run to DB
    run = JobRun(
        name="check_for_winner",
        status=job_status,
        data={
            "game_winner_response": response,
            "message": msg
        }
    )
    run.save()

    # log output
    log.info(msg)

def check_for_daily_kings_game():
    # check for LightStatus instance from yesterday, and reset beam if found
    reset_beam()

    log.info("Checking for daily game...")
    response = fetch_kings_game(todays_date())
    if response["status"] == "success":
        job_status = JobStatus.success

        if response["game"]:
            # start polling for winner
            msg = "Found Kings game. Adding job check_for_winner."
            start_date = convert_to_pacific_tz(response["game"]["gameTimeUTC"])
            end_date = start_date.end_of("day")
            scheduler.add_job(
                id="check_for_winner",
                func=check_for_winner,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                **every_ten_minutes
            )
        else:
            # do nothing if no game today
            msg = "No Kings game found."
    else:
        msg = f"Error, fetch_kings_game returned {response['status_code']}"
        job_status = JobStatus.error
    
    # save new job run to DB
    run = JobRun(
        name="check_for_daily_kings_game",
        status=job_status,
        data={
            "game_winner_response": response,
            "message": msg
        }
    )
    run.save()

    # log output
    log.info(msg)
