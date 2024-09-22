from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user_analytics import UserAnalytics

class UserAnalyticsResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        material_id = data.get('material_id')
        time_spent = data.get('time_spent', 0)
        interactions = data.get('interactions', 0)

        if not material_id:
            return {'message': 'Missing required fields'}, 400

        analytics = UserAnalytics.query.filter_by(user_id=user_id, material_id=material_id).first()
        if analytics:
            analytics.time_spent += time_spent
            analytics.interactions += interactions
        else:
            analytics = UserAnalytics(user_id=user_id, material_id=material_id, time_spent=time_spent, interactions=interactions)
            db.session.add(analytics)

        db.session.commit()
        return analytics.to_dict(), 201

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        analytics = UserAnalytics.query.filter_by(user_id=user_id).all()
        return [a.to_dict() for a in analytics], 200