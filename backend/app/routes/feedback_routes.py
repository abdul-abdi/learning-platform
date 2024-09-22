from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.feedback import Feedback
from app.schemas import FeedbackSchema

feedback_schema = FeedbackSchema()

class FeedbackResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = feedback_schema.load(request.json)
        
        feedback = Feedback(
            user_id=user_id,
            material_id=data['material_id'],
            rating=data['rating'],
            comment=data.get('comment')
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        return feedback.to_dict(), 201

    @jwt_required()
    def get(self, material_id):
        feedback = Feedback.query.filter_by(material_id=material_id).all()
        return [f.to_dict() for f in feedback], 200