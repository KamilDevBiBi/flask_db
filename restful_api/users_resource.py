from flask_restful import Resource, abort

from flask import jsonify

from data import db_session
from data.__all_models import User

from .reqparser import parser

def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)

    if not user:
        abort(404, message=f"User {user_id} not found")

class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)

        session = db_session.create_session()
        user = session.query(User).get(user_id)

        return jsonify({'user': user.to_dict(only=('id', 'name', 'email', 'from_city'))})
    
    def delete(self, user_id):
        abort_if_user_not_found(user_id)

        session = db_session.create_session()
        user = session.query(User).get(user_id)

        session.delete(user)
        session.commit()

        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            'user': [ item.to_dict(only=('id', 'name', 'email', 'from_city')) for item in users]
        })
    
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        user = User(
            name=args['name'],
            email=args['email'],
            from_city=args['from_city']
        )
        user.set_password(args['password'])

        session.add(user)
        session.commit()

        return jsonify({'id': user.id})
