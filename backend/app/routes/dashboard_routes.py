from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user_progress import UserProgress
from app.models.learning_material import LearningMaterial
from app.services.recommendation_service import RecommendationService

class UserDashboardResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        # Get user progress
        progress = UserProgress.query.filter_by(user_id=user_id).all()
        total_materials = LearningMaterial.query.count()
        completed_materials = sum(1 for p in progress if p.status == 'completed')
        in_progress_materials = sum(1 for p in progress if p.status == 'in_progress')
        
        # Get recommendations
        recommendations = RecommendationService.get_recommendations(user_id, num_recommendations=3)
        
        return {
            'total_materials': total_materials,
            'completed_materials': completed_materials,
            'in_progress_materials': in_progress_materials,
            'completion_rate': (completed_materials / total_materials) * 100 if total_materials > 0 else 0,
            'recent_progress': [p.to_dict() for p in progress[-5:]],
            'recommendations': recommendations
        }, 200