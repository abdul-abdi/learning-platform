from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, metrics
from app.models.learning_material import LearningMaterial
from app.schemas import LearningMaterialSchema
from app.decorators import role_required
from loguru import logger
from flask_caching import Cache

cache = Cache()

learning_material_schema = LearningMaterialSchema()

learning_material_views = metrics.counter(
    'learning_material_views_total', 'Number of views for learning materials'
)

class LearningMaterialResource(Resource):
    @jwt_required()
    @learning_material_views.count_exceptions()
    def get(self, material_id):
        material = LearningMaterial.query.get_or_404(material_id)
        learning_material_views.inc()
        return material.to_dict(), 200

class LearningMaterialListResource(Resource):
    @jwt_required()
    @cache.cached(timeout=300)  # Cache for 5 minutes
    def get(self):
        materials = LearningMaterial.query.all()
        return [material.to_dict() for material in materials], 200

    @jwt_required()
    @role_required(['admin', 'teacher'])
    def post(self):
        data = request.get_json()
        errors = learning_material_schema.validate(data)
        if errors:
            return {'message': 'Validation error', 'errors': errors}, 400
        
        material = LearningMaterial(
            title=data['title'],
            description=data['description'],
            content=data['content'],
            difficulty_level=data['difficulty_level']
        )
        db.session.add(material)
        db.session.commit()
        return material.to_dict(), 201

class LearningMaterialUpdateResource(Resource):
    @jwt_required()
    @role_required(['admin', 'teacher'])
    def put(self, material_id):
        material = LearningMaterial.query.get_or_404(material_id)
        data = request.get_json()
        errors = learning_material_schema.validate(data)
        if errors:
            return {'message': 'Validation error', 'errors': errors}, 400
        
        material.title = data.get('title', material.title)
        material.description = data.get('description', material.description)
        material.content = data.get('content', material.content)
        material.difficulty_level = data.get('difficulty_level', material.difficulty_level)
        
        db.session.commit()
        return material.to_dict(), 200

    @jwt_required()
    @role_required(['admin'])
    def delete(self, material_id):
        material = LearningMaterial.query.get_or_404(material_id)
        db.session.delete(material)
        db.session.commit()
        return '', 204