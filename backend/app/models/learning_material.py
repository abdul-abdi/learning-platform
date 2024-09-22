from app import db
from datetime import datetime

class LearningMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    learning_style = db.Column(db.String(20), default='visual')
    difficulty = db.Column(db.String(20), default='balanced')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'learning_style': self.learning_style,
            'difficulty': self.difficulty,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }