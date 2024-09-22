from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.learning_path import LearningPath, LearningPathMaterial
from app.models.user_progress import UserProgress

class LearningPathResource(Resource):
    @jwt_required()
    def get(self, path_id):
        learning_path = LearningPath.query.get_or_404(path_id)
        return learning_path.to_dict(), 200

class LearningPathListResource(Resource):
    @jwt_required()
    def get(self):
        learning_paths = LearningPath.query.all()
        return [path.to_dict() for path in learning_paths], 200

class UserLearningPathProgressResource(Resource):
    @jwt_required()
    def get(self, path_id):
        user_id = get_jwt_identity()
        learning_path = LearningPath.query.get_or_404(path_id)
        
        progress = []
        total_materials = len(learning_path.materials)
        completed_materials = 0

        for path_material in learning_path.materials:
            user_progress = UserProgress.query.filter_by(
                user_id=user_id, 
                material_id=path_material.material_id
            ).first()

            if user_progress and user_progress.status == 'completed':
                completed_materials += 1

            progress.append({
                'material_id': path_material.material_id,
                'status': user_progress.status if user_progress else 'not_started',
                'progress_percentage': user_progress.progress_percentage if user_progress else 0
            })

        overall_progress = (completed_materials / total_materials) * 100 if total_materials > 0 else 0

        return {
            'path_id': path_id,
            'overall_progress': overall_progress,
            'materials_progress': progress
        }, 200