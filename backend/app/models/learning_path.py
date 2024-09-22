from app import db
from datetime import datetime

class LearningPath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    materials = db.relationship('LearningPathMaterial', back_populates='learning_path', order_by='LearningPathMaterial.order')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'materials': [m.to_dict() for m in self.materials],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class LearningPathMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    learning_path_id = db.Column(db.Integer, db.ForeignKey('learning_path.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('learning_material.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)

    learning_path = db.relationship('LearningPath', back_populates='materials')
    learning_material = db.relationship('LearningMaterial')

    def to_dict(self):
        return {
            'id': self.id,
            'learning_path_id': self.learning_path_id,
            'material_id': self.material_id,
            'order': self.order,
            'material': self.learning_material.to_dict()
        }