from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.learning_material import LearningMaterial
from app.services.analytics_service import AnalyticsService
from app import db, cache

learning_material_bp = Blueprint('learning_material', __name__)

@learning_material_bp.route('/learning-materials', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_learning_materials():
    materials = LearningMaterial.query.all()
    return jsonify([material.to_dict() for material in materials]), 200

@learning_material_bp.route('/learning-materials/<int:id>', methods=['GET'])
@jwt_required()
def get_learning_material(id):
    material = LearningMaterial.query.get_or_404(id)
    user_id = get_jwt_identity()
    AnalyticsService.track_material_view(user_id, id)
    return jsonify(material.to_dict()), 200

@learning_material_bp.route('/learning-materials', methods=['POST'])
@jwt_required()
def create_learning_material():
    data = request.get_json()
    new_material = LearningMaterial(title=data['title'], content=data['content'])
    db.session.add(new_material)
    db.session.commit()
    cache.delete('view//learning-materials')  # Invalidate cache
    return jsonify(new_material.to_dict()), 201