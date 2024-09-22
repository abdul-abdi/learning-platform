from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.badge import UserBadge

class UserBadgeResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user_badges = UserBadge.query.filter_by(user_id=user_id).all()
        return [user_badge.to_dict() for user_badge in user_badges], 200