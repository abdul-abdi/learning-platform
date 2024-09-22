from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.recommendation_service import RecommendationService

class RecommendationResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        recommendations = RecommendationService.get_recommendations(user_id)
        return recommendations, 200