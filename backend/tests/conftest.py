import pytest
from app import create_app, db
from app.models.user import User
from app.models.learning_material import LearningMaterial
from app.models.notification import Notification

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        
        # Create test users
        user1 = User(username='testuser1', email='test1@example.com')
        user1.set_password('password123')
        user2 = User(username='testuser2', email='test2@example.com')
        user2.set_password('password456')
        
        # Create test learning materials
        material1 = LearningMaterial(title='Test Material 1', description='Description 1', content='Content 1')
        material2 = LearningMaterial(title='Test Material 2', description='Description 2', content='Content 2')
        
        # Create test notifications
        notification1 = Notification(user_id=user1.id, message='Test notification 1', type='info')
        notification2 = Notification(user_id=user1.id, message='Test notification 2', type='alert')
        
        db.session.add_all([user1, user2, material1, material2, notification1, notification2])
        db.session.commit()
        
        yield db
        
        db.drop_all()