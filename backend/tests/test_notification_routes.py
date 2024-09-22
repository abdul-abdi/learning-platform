import json
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.models.notification import Notification

def test_get_notifications(client, init_database):
    user = User.query.filter_by(username='testuser1').first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}

    # Create test notifications
    notification1 = Notification(user_id=user.id, message='Test notification 1', type='info')
    notification2 = Notification(user_id=user.id, message='Test notification 2', type='alert')
    init_database.session.add_all([notification1, notification2])
    init_database.session.commit()

    response = client.get('/api/notifications', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['message'] == 'Test notification 2'  # Assuming ordered by created_at desc
    assert data[1]['message'] == 'Test notification 1'

def test_mark_notification_as_read(client, init_database):
    user = User.query.filter_by(username='testuser1').first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}

    # Create a test notification
    notification = Notification(user_id=user.id, message='Test notification', type='info')
    init_database.session.add(notification)
    init_database.session.commit()

    response = client.put(f'/api/notifications/{notification.id}', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Notification marked as read'

    # Verify the notification is marked as read
    updated_notification = Notification.query.get(notification.id)
    assert updated_notification.read == True

def test_create_notification(client, init_database):
    user = User.query.filter_by(username='testuser1').first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.post('/api/notifications', json={
        'message': 'New notification',
        'type': 'info'
    }, headers=headers)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'New notification'
    assert data['type'] == 'info'