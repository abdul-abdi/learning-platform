from flask import request, jsonify, url_for
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db, jwt, mail
from app.models.user import User
from datetime import timedelta
from app.schemas import LoginSchema, RegistrationSchema, PasswordResetRequestSchema, PasswordResetSchema
from app import limiter
from flask_mail import Message
import secrets

class UserRegistration(Resource):
    @limiter.limit("5 per minute")
    def post(self):
        schema = RegistrationSchema()
        errors = schema.validate(request.json)
        if errors:
            return {'message': 'Validation error', 'errors': errors}, 400
        
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'User already exists'}, 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            role='student'
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        return {'message': 'User created successfully'}, 201

class UserLogin(Resource):
    @limiter.limit("5 per minute")
    def post(self):
        schema = LoginSchema()
        errors = schema.validate(request.json)
        if errors:
            return {'message': 'Validation error', 'errors': errors}, 400
        
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user_id': user.id
            }, 200
        return {'message': 'Invalid credentials'}, 401

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        # For simplicity, we're not blacklisting tokens here.
        # In a production environment, you should implement token blacklisting.
        return {'message': 'Successfully logged out'}, 200

class PasswordResetRequest(Resource):
    @limiter.limit("3 per hour")
    def post(self):
        schema = PasswordResetRequestSchema()
        errors = schema.validate(request.json)
        if errors:
            return {'message': 'Validation error', 'errors': errors}, 400
        
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user:
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            
            reset_url = url_for('password_reset', token=token, _external=True)
            msg = Message('Password Reset Request',
                          sender='noreply@yourdomain.com',
                          recipients=[user.email])
            msg.body = f'To reset your password, visit the following link: {reset_url}'
            mail.send(msg)
        
        return {'message': 'If an account with that email exists, a password reset link has been sent.'}, 200

class PasswordReset(Resource):
    def post(self, token):
        schema = PasswordResetSchema()
        errors = schema.validate(request.json)
        if errors:
            return {'message': 'Validation error', 'errors': errors}, 400
        
        user = User.query.filter_by(reset_token=token).first()
        if user and user.reset_token_expiration > datetime.utcnow():
            data = request.get_json()
            user.set_password(data['password'])
            user.reset_token = None
            user.reset_token_expiration = None
            db.session.commit()
            return {'message': 'Password has been reset successfully'}, 200
        return {'message': 'Invalid or expired token'}, 400

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    # Here you would check if the token is in your blocklist
    # For simplicity, we're always returning False
    return False