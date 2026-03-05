from flask import Flask, render_template
from data import db_session
from data.__all_models import Jobs, User

app = Flask(__name__)

@app.route("/")
def index():
    session = db_session.create_session()
    
    cur_jobs = session.query(Jobs).all()

    jobs_leaders_names = list()
    for item in cur_jobs:
        user = session.query(User).filter(User.id == item.team_leader).first()
        jobs_leaders_names.append(f'{user.surname} {user.name}')

    return render_template("jobs_table.html", jobs_list=cur_jobs, leader_names=jobs_leaders_names)


def main():
    db_session.global_init("zip_project/db/task_users.db")
    app.run(host="127.0.0.1", port="8080")

main()
