from app.services.recommendation_service import RecommendationService
from app.models.user import User
from app.models.learning_material import LearningMaterial
from app.models.user_progress import UserProgress

def test_get_recommendations(init_database):
    user = User.query.filter_by(username='testuser1').first()
    material = LearningMaterial.query.first()
    
    # Create some user progress
    progress = UserProgress(user_id=user.id, material_id=material.id, status='completed', progress_percentage=100)
    init_database.session.add(progress)
    init_database.session.commit()
    
    recommendations = RecommendationService.get_recommendations(user.id)
    
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    for recommendation in recommendations:
        assert 'id' in recommendation
        assert 'title' in recommendation
        assert 'description' in recommendation

def test_get_recommendations_collaborative_filtering(init_database):
    # Create test users and materials
    user1 = User(username='user1', email='user1@example.com')
    user2 = User(username='user2', email='user2@example.com')
    user3 = User(username='user3', email='user3@example.com')
    
    material1 = LearningMaterial(title='Material 1', description='Description 1', content='Content 1')
    material2 = LearningMaterial(title='Material 2', description='Description 2', content='Content 2')
    material3 = LearningMaterial(title='Material 3', description='Description 3', content='Content 3')
    
    init_database.session.add_all([user1, user2, user3, material1, material2, material3])
    init_database.session.commit()
    
    # Create user progress
    progress1 = UserProgress(user_id=user1.id, material_id=material1.id, status='completed', progress_percentage=100)
    progress2 = UserProgress(user_id=user1.id, material_id=material2.id, status='in_progress', progress_percentage=50)
    progress3 = UserProgress(user_id=user2.id, material_id=material1.id, status='completed', progress_percentage=100)
    progress4 = UserProgress(user_id=user2.id, material_id=material3.id, status='completed', progress_percentage=100)
    
    init_database.session.add_all([progress1, progress2, progress3, progress4])
    init_database.session.commit()
    
    # Get recommendations for user3
    recommendations = RecommendationService.get_recommendations(user3.id)
    
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    assert any(r['id'] == material1.id for r in recommendations)
    assert any(r['id'] == material3.id for r in recommendations)