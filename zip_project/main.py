from flask import Flask, render_template, redirect, request, abort
from forms import LoginForm, RegisterForm, addJobForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.__all_models import User, Jobs

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config["SECRET_KEY"] = "my_supers3cr3t"

@app.route("/")
def index():
    session = db_session.create_session()

    cur_jobs = session.query(Jobs).all()

    jobs_leaders_names = list()
    for item in cur_jobs:
        user = session.query(User).filter(User.id == item.team_leader).first()
        jobs_leaders_names.append(f'{user.name}')

    return render_template("jobs_table.html", jobs_list=cur_jobs, leader_names=jobs_leaders_names)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')
    
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User,user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()

        user_email = form.email.data
        user = session.query(User).filter(User.email == user_email).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        
        return render_template("login_form.html", message="Неверный логин или пароль", form=form)

    return render_template("login_form.html", form=form)


@app.route("/logout")
@login_required
def logout_url():
    logout_user()
    return redirect("/")


@app.route("/addjob", methods=["GET", "POST"])
def add_job():
    form = addJobForm()

    if form.validate_on_submit():
        session = db_session.create_session()
        leader_user = session.query(User).filter(User.id == form.team_leader.data).first()
        if not leader_user:
            return render_template("add_job.html", form=form, message="team leader id is incorrect")
        
        collaborators = form.collaborators.data.split(',')
        for coll_id in collaborators:
            user = session.query(User).filter(User.id == coll_id).first()
            if not user:
                return render_template("add_job.html", form=form, message="collaborators list is incorrect")
        
        new_job = Jobs(
            team_leader=form.team_leader.data, 
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
            )
        
        session.add(new_job)
        session.commit()

        return redirect("/")
    return render_template("add_job.html", form=form)


@app.route("/addjob/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    form = addJobForm()

    if request.method == "GET":
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == job_id, (Jobs.team_leader ==current_user.id) | (current_user.id == 1)).first()

        if job:
            form.job.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
        else:
            abort(404)

    if form.validate_on_submit():
        session = db_session.create_session()

        leader_user = session.query(User).filter(User.id == form.team_leader.data).first()
        if not leader_user:
            return render_template("add_job.html", form=form, message="team leader id is incorrect")
        
        collaborators = form.collaborators.data.split(',')
        for coll_id in collaborators:
            user = session.query(User).filter(User.id == coll_id).first()
            if not user:
                return render_template("add_job.html", form=form, message="collaborators list is incorrect")
        
        editting_job = session.query(Jobs).filter(Jobs.id == job_id, (Jobs.team_leader ==current_user.id) | (current_user.id == 1)).first()
        if editting_job:
            editting_job.team_leader = form.team_leader.data
            editting_job.job = form.job.data
            editting_job.work_size = form.work_size.data
            editting_job.collaborators = form.collaborators.data

            session.commit()
            return redirect("/")
        else:
            abort(404)
            
    return render_template("add_job.html", form=form)

@app.route("/deljob/<int:job_id>")
@login_required
def remove_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id, (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()

    if job:
        session.delete(job)
        session.commit()
        return redirect("/")
    else:
        abort(404)


def main():
    db_session.global_init("zip_project/db/auth_user.db")
    app.run(host="127.0.0.1", port="8080")


main()