from app.models.user import User

def test_user_creation(init_database):
    user = User(username='newuser', email='newuser@example.com')
    user.set_password('newpassword')
    init_database.session.add(user)
    init_database.session.commit()
    
    assert user.id is not None
    assert user.username == 'newuser'
    assert user.email == 'newuser@example.com'
    assert user.check_password('newpassword')
    assert not user.check_password('wrongpassword')

def test_user_to_dict(init_database):
    user = User.query.filter_by(username='testuser1').first()
    user_dict = user.to_dict()
    
    assert 'id' in user_dict
    assert 'username' in user_dict
    assert 'email' in user_dict
    assert 'password_hash' not in user_dict