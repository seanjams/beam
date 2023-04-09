from app import app
from db import db, JobRun
from jobs import check_for_daily_kings_game
from scheduler import scheduler

# init db
db.init_app(app)
with app.app_context():
    db.create_all()

# init scheduler
scheduler.init_app(app)
scheduler.add_job(
    id="check_for_daily_kings_game",
    func=check_for_daily_kings_game,
    trigger="interval",
    hours=24,
    misfire_grace_time=900,
)
scheduler.start()

# init routes
@app.route('/job_runs')
def list_job_runs():
    with app.app_context():
        return [run.json() for run in JobRun.query.all()]

@app.route('/job_runs/<int:run_id>')
def retrieve_job_run(run_id):
    with app.app_context():
        if run := JobRun.query.get(run_id):
            return run.json()
        return {}

# run app
if __name__ == "__main__":
    app.run()
