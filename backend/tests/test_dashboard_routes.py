import json
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.models.learning_material import LearningMaterial
from app.models.user_progress import UserProgress

def test_get_user_dashboard(client, init_database):
    user = User.query.filter_by(username='testuser1').first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Create test learning materials and progress
    material1 = LearningMaterial(title='Test Material 1', description='Description 1', content='Content 1')
    material2 = LearningMaterial(title='Test Material 2', description='Description 2', content='Content 2')
    init_database.session.add_all([material1, material2])
    init_database.session.commit()
    
    progress1 = UserProgress(user_id=user.id, material_id=material1.id, status='completed', progress_percentage=100)
    progress2 = UserProgress(user_id=user.id, material_id=material2.id, status='in_progress', progress_percentage=50)
    init_database.session.add_all([progress1, progress2])
    init_database.session.commit()
    
    response = client.get('/api/dashboard', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['total_materials'] == 2
    assert data['completed_materials'] == 1
    assert data['in_progress_materials'] == 1
    assert data['completion_rate'] == 50.0
    assert len(data['recent_progress']) == 2
    assert len(data['recommendations']) > 0