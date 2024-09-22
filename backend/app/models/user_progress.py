from app import db
from datetime import datetime

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    material_id = db.Column(db.Integer, db.ForeignKey('learning_material.id'), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, index=True)  # 'not_started', 'in_progress', 'completed'
    progress_percentage = db.Column(db.Float, default=0.0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('progress', lazy=True))
    learning_material = db.relationship('LearningMaterial', backref=db.backref('user_progress', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'material_id': self.material_id,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'last_accessed': self.last_accessed.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }