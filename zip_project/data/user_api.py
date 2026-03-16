from flask import Blueprint, jsonify, make_response, request

from . import db_session
from .__all_models import User

blueprint = Blueprint(
    "user_api", __name__,
    template_folder="templates"
)

@blueprint.route("/api/user")
def get_all_user():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'user': [
                item.to_dict(only=('id', 'name', 'email', 'from_city')) for item in users
            ]
        }
    )


@blueprint.route("/api/user/<int:user_id>")
def get_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return jsonify(
            {
                'user': user.to_dict(only=('id', 'name', 'email', 'from_city'))
            }
        )


@blueprint.route("/api/user", methods=["POST"])
def create_new_user():
    print(request.json)
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    
    user_data = ['name', 'email', 'password', 'from_city']
    if not all(key in request.json for key in user_data):
        return make_response(jsonify({'error': 'Bad request'}, 400))
    
    user = User(
        name=request.json['name'],
        email=request.json['email'],
        from_city=request.json['from_city']
    )
    user.set_password(request.json['password'])

    session = db_session.create_session()
    session.add(user)
    session.commit()

    return jsonify({'id': user.id})


@blueprint.route("/api/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    session.delete(user)
    session.commit()

    return jsonify({'success': 'OK'})


@blueprint.route("/api/user/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    
    user_data = ['name', 'email', 'password', 'from_city']
    if not all(key in request.json for key in user_data):
        return make_response(jsonify({'error': 'Bad request'}, 400))
    
    json_data = request.json
    user.name = json_data['team_leader']
    user.email = json_data['user']
    user.from_city = json_data['from_city']
    user.set_password(json_data['password'])

    session.commit()
    return jsonify({'success': 'OK', 'id': user.id})
