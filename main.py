from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from forms import LoginForm, RegisterForm, addJobForm, addDepartmentForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.__all_models import User, Jobs, Departament

from data.jobs_api import blueprint as blueprint_job
from data.user_api import blueprint as blueprint_user

import requests
from restful_api.users_resource import UsersResource, UsersListResource
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(UsersListResource, '/api/v2/users')
api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')


login_manager = LoginManager()
login_manager.init_app(app)

app.config["SECRET_KEY"] = "my_supers3cr3t"

@app.route("/")
def index():
    session = db_session.create_session()

    cur_jobs = session.query(Jobs).all()

    return render_template("jobs_table.html", jobs_list=cur_jobs)


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
        job = session.query(Jobs).filter(Jobs.id == job_id, (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()

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


@app.route('/departments')
def show_departments():
    session = db_session.create_session()
    departments = session.query(Departament).all()

    return render_template("department_table.html", department_list=departments)


@app.route("/new_department", methods=["GET", "POST"])
@login_required
def add_department():
    form = addDepartmentForm()

    if form.validate_on_submit():
        session = db_session.create_session()

        chief_id = form.chief.data
        user = session.query(User).filter(User.id == chief_id).first()
        if not user:
            return render_template("add_department.html", form=form, message="Неправильный chief")
        
        members_data= form.members.data
        for member_id in members_data.split(','):
            user = session.query(User).filter(User.id == member_id).first()
            if not user:
                return render_template("add_department.html", form=form, message="Неправильный members")
        
        department = session.query(Departament).filter(Departament.email == form.email.data).first()
        if department:
            return render_template("add_department.html", form=form, message="Департамент с таким email уже есть")
        
        department = Departament(
            title=form.title.data,
            email=form.email.data,
            chief=chief_id,
            members=members_data
            )
        
        session.add(department)
        session.commit()

        return redirect('/departments')

    return render_template("add_department.html", form=form)


@app.route("/new_department/<int:dep_id>", methods=["GET", "POST"])
@login_required
def edit_department(dep_id):
    form = addDepartmentForm()

    if request.method == "GET":
        session = db_session.create_session()
        department = session.query(Departament).filter(Departament.id == dep_id, Departament.chief == current_user.id).first()

        if department:
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    
    if form.validate_on_submit():
        session = db_session.create_session()
        department = session.query(Departament).filter(Departament.id == dep_id, Departament.chief == current_user.id).first()

        if department:
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data

            session.commit()
            return redirect("/departments")
        else:
            abort(404)
    
    return render_template("add_department.html", form=form)
    

@app.route("/department_del/<int:dep_id>")
@login_required
def remove_department(dep_id):
    session = db_session.create_session()
    department = session.query(Departament).filter(Departament.id == dep_id, Departament.chief == current_user.id).first()

    if department:
        session.delete(department)
        session.commit()

        return redirect('/departments')
    else:
        abort(404)


@app.route('/users_show/<int:user_id>')
def show_user_town_image(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        abort(404)
    
    geocode = user.from_city
    if not geocode:
        abort(400)

    geocode_url = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    
    geocoder_request = f'{geocode_url}apikey={api_key}&geocode={geocode}&format=json'

    response = requests.get(geocoder_request)
    if not response:
        abort(400)

    json_response = response.json()
    results = json_response["response"]["GeoObjectCollection"]["featureMember"]
    if len(results) <= 0:
        abort(400)
    
    toponym = results[0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"].split()
    
    static_url = 'https://static-maps.yandex.ru/v1?'
    static_apikey = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
    params = {
        'apikey': static_apikey,
        'll': ','.join(toponym_coodrinates),
        'spn': '0.02,0.02'
    }

    response = requests.get(static_url, params=params)
    if not response:
        abort(400)

    with open(f'zip_project/static/img/map_{user_id}.png', "wb") as file:
        file.write(response.content)
    
    return render_template('user_town_image.html', user=user)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/auth_user.db")
    app.register_blueprint(blueprint_job)
    app.register_blueprint(blueprint_user)
    app.run(host="127.0.0.1", port="8080")


main()