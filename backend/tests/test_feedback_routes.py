import json
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.models.learning_material import LearningMaterial

def test_create_feedback(client, init_database):
    user = User.query.filter_by(username='testuser1').first()
    material = LearningMaterial.query.first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = client.post('/api/feedback', json={
        'material_id': material.id,
        'rating': 5,
        'comment': 'Great material!'
    }, headers=headers)
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['rating'] == 5
    assert data['comment'] == 'Great material!'

def test_get_feedback(client, init_database):
    user = User.query.filter_by(username='testuser1').first()
    material = LearningMaterial.query.first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Create a feedback first
    client.post('/api/feedback', json={
        'material_id': material.id,
        'rating': 4,
        'comment': 'Good material'
    }, headers=headers)
    
    response = client.get(f'/api/feedback/{material.id}', headers=headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]['rating'] == 4
    assert data[0]['comment'] == 'Good material'