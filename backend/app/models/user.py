from app import db, bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='student')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_token(self):
        return create_access_token(identity=self.id, expires_delta=timedelta(days=1))

    @staticmethod
    def verify_token(token):
        try:
            user_id = decode_token(token)['sub']
            return User.query.get(user_id)
        except:
            return None
