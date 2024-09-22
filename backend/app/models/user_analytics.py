from app import db
from datetime import datetime

class UserAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('learning_material.id'), nullable=False)
    time_spent = db.Column(db.Integer, default=0)  # Time spent in seconds
    interactions = db.Column(db.Integer, default=0)  # Number of interactions with the material
    last_interaction = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('analytics', lazy=True))
    learning_material = db.relationship('LearningMaterial', backref=db.backref('user_analytics', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'material_id': self.material_id,
            'time_spent': self.time_spent,
            'interactions': self.interactions,
            'last_interaction': self.last_interaction.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }