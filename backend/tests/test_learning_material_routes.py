import json
from flask_jwt_extended import create_access_token

def test_get_learning_materials(client, init_database):
    user = init_database.session.query(User).filter_by(username='testuser1').first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = client.get('/api/learning-materials', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    for material in data:
        assert 'id' in material
        assert 'title' in material
        assert 'description' in material

def test_get_learning_material(client, init_database):
    user = init_database.session.query(User).filter_by(username='testuser1').first()
    material = init_database.session.query(LearningMaterial).first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = client.get(f'/api/learning-materials/{material.id}', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == material.id
    assert data['title'] == material.title
    assert data['description'] == material.description