from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.forum_post import ForumPost

class ForumPostResource(Resource):
    @jwt_required()
    def get(self, material_id):
        posts = ForumPost.query.filter_by(material_id=material_id).order_by(ForumPost.created_at.desc()).all()
        return [post.to_dict() for post in posts], 200

    @jwt_required()
    def post(self, material_id):
        user_id = get_jwt_identity()
        data = request.get_json()
        content = data.get('content')

        if not content:
            return {'message': 'Content is required'}, 400

        new_post = ForumPost(user_id=user_id, material_id=material_id, content=content)
        db.session.add(new_post)
        db.session.commit()

        return new_post.to_dict(), 201

class ForumPostListResource(Resource):
    @jwt_required()
    def get(self):
        posts = ForumPost.query.order_by(ForumPost.created_at.desc()).limit(20).all()
        return [post.to_dict() for post in posts], 200