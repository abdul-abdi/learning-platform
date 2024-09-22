from app.models.user import User
from app.models.learning_material import LearningMaterial
from app.models.user_progress import UserProgress
from app.models.user_analytics import UserAnalytics
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app import redis_client
import json

class RecommendationService:
    @staticmethod
    def get_recommendations(user_id, num_recommendations=5):
        cache_key = f'user:{user_id}:recommendations'
        cached_recommendations = redis_client.get(cache_key)

        if cached_recommendations:
            return json.loads(cached_recommendations)

        user = User.query.get(user_id)
        if not user:
            return []

        # Get user's completed materials
        completed_materials = UserProgress.query.filter_by(user_id=user_id, status='completed').all()
        completed_material_ids = [progress.material_id for progress in completed_materials]

        # Get user's analytics
        user_analytics = UserAnalytics.query.filter_by(user_id=user_id).all()
        
        # Create a user-item matrix based on time spent and interactions
        all_materials = LearningMaterial.query.all()
        user_item_matrix = np.zeros((1, len(all_materials)))
        
        for i, material in enumerate(all_materials):
            analytics = next((a for a in user_analytics if a.material_id == material.id), None)
            if analytics:
                user_item_matrix[0, i] = analytics.time_spent * analytics.interactions

        # Apply user preferences
        for i, material in enumerate(all_materials):
            if material.learning_style == user.settings.learning_style:
                user_item_matrix[0, i] *= 1.2  # Boost materials matching user's learning style
            
            if material.difficulty == user.settings.difficulty_preference:
                user_item_matrix[0, i] *= 1.1  # Boost materials matching user's difficulty preference

        # Find similar materials
        material_similarities = cosine_similarity(user_item_matrix, user_item_matrix)
        
        # Get top similar materials that the user hasn't completed yet
        similar_material_indices = material_similarities[0].argsort()[::-1]
        recommendations = []
        
        for index in similar_material_indices:
            material = all_materials[index]
            if material.id not in completed_material_ids and len(recommendations) < num_recommendations:
                recommendations.append(material.to_dict())

        redis_client.setex(cache_key, 3600, json.dumps(recommendations))  # Cache for 1 hour
        return recommendations
