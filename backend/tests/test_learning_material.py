import pytest
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.models.learning_material import LearningMaterial

def test_get_learning_materials(client, init_database):
    user = User.query.filter_by(username='testuser1').first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get('/api/learning-materials', headers=headers)
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['title'] == 'Test Material 1'
    assert response.json[1]['title'] == 'Test Material 2'

def test_get_single_learning_material(client, init_database):
    user = User.query.filter_by(username='testuser1').first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}

    material = LearningMaterial.query.first()
    response = client.get(f'/api/learning-materials/{material.id}', headers=headers)
    assert response.status_code == 200
    assert response.json['title'] == material.title
    assert response.json['description'] == material.description
    assert response.json['content'] == material.content

def test_update_user_progress(client, init_database):
    user = User.query.filter_by(username='testuser1').first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}

    material = LearningMaterial.query.first()
    response = client.post('/api/user-progress', json={
        'material_id': material.id,
        'progress': 50
    }, headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Progress updated successfully'

    # Verify the progress was actually updated
    response = client.get('/api/user-progress', headers=headers)
    assert response.status_code == 200
    assert any(progress['material_id'] == material.id and progress['progress'] == 50 for progress in response.json)