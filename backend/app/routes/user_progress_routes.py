from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user_progress import UserProgress
from app.models.learning_material import LearningMaterial
from app.schemas import UserProgressSchema
from sqlalchemy import func

user_progress_schema = UserProgressSchema()

class UserProgressResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        progress = UserProgress.query.filter_by(user_id=user_id).all()
        return [p.to_dict() for p in progress], 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        errors = user_progress_schema.validate(data)
        if errors:
            return {'message': 'Validation error', 'errors': errors}, 400
        
        progress = UserProgress(
            user_id=user_id,
            material_id=data['material_id'],
            status=data['status'],
            progress_percentage=data['progress_percentage']
        )
        db.session.add(progress)
        db.session.commit()
        return progress.to_dict(), 201

class UserProgressAnalyticsResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        total_materials = LearningMaterial.query.count()
        completed_materials = UserProgress.query.filter_by(user_id=user_id, status='completed').count()
        in_progress_materials = UserProgress.query.filter_by(user_id=user_id, status='in_progress').count()
        
        avg_progress = db.session.query(func.avg(UserProgress.progress_percentage)).filter_by(user_id=user_id).scalar() or 0
        
        return {
            'total_materials': total_materials,
            'completed_materials': completed_materials,
            'in_progress_materials': in_progress_materials,
            'completion_rate': (completed_materials / total_materials) * 100 if total_materials > 0 else 0,
            'average_progress': avg_progress
        }, 200