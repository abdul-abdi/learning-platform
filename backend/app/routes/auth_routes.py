from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db, limiter

class Login(Resource):
    @limiter.limit("5 per minute")
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

class Register(Resource):
    @limiter.limit("3 per hour")
    def post(self):
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already registered'}, 400
        new_user = User(email=data['email'], username=data['username'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

# Update API routes
api.add_resource(Login, '/auth/login')
api.add_resource(Register, '/auth/register')