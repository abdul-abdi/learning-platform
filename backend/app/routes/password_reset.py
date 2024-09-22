from flask import request, url_for
from flask_restful import Resource
from app import db
from app.models.user import User
from app.utils.email import send_password_reset_email
import secrets

class RequestPasswordReset(Resource):
    def post(self):
        email = request.json.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            db.session.commit()
            reset_url = url_for('reset_password', token=token, _external=True)
            send_password_reset_email(user.email, reset_url)
        return {'message': 'If an account with that email exists, a password reset link has been sent.'}, 200

class ResetPassword(Resource):
    def post(self, token):
        user = User.query.filter_by(reset_token=token).first()
        if not user:
            return {'message': 'Invalid or expired token'}, 400
        
        new_password = request.json.get('new_password')
        user.set_password(new_password)
        user.reset_token = None
        db.session.commit()
        return {'message': 'Password has been reset successfully'}, 200