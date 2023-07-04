from flask import Flask ,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from Models.users import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is None:
            users = User.query.all()
            response = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
            return response, 200
        else:
            user = User.query.get(user_id)
            if user:
                response = {'id': user.id, 'username': user.username, 'email': user.email}
                return response, 200
            else:
                return {'error': 'User not found'}, 404

    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        response = {'id': user.id, 'username': user.username, 'email': user.email}
        return response, 201

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)

        if user:
            user.username = data.get('username')
            user.email = data.get('email')
            user.password = data.get('password')

            db.session.commit()

            response = {'id': user.id, 'username': user.username, 'email': user.email}
            return response, 200
        else:
            return {'error': 'User not found'}, 404

    def patch(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)

        if user:
            if 'username' in data:
                user.username = data.get('username')
            if 'email' in data:
                user.email = data.get('email')
            if 'password' in data:
                user.password = data.get('password')

            db.session.commit()

            response = {'id': user.id, 'username': user.username, 'email': user.email}
            return response, 200
        else:
            return {'error': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)

        if user:
            db.session.delete(user)
            db.session.commit()
            return '', 204
        else:
            return {'error': 'User not found'}, 404


api.add_resource(UserResource, '/users', '/users/<int:user_id>')


if __name__ == '__main__':
    app.run()
