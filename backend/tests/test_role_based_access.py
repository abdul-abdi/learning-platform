import json
from flask_jwt_extended import create_access_token

def test_admin_access(client, init_database):
    admin_user = User(username='admin', email='admin@example.com', role='admin')
    admin_user.set_password('adminpass')
    init_database.session.add(admin_user)
    init_database.session.commit()

    access_token = create_access_token(identity=admin_user.id)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get('/api/admin/dashboard', headers=headers)
    assert response.status_code == 200
    assert b'Admin dashboard data' in response.data

def test_student_access_denied(client, init_database):
    student_user = User(username='student', email='student@example.com', role='student')
    student_user.set_password('studentpass')
    init_database.session.add(student_user)
    init_database.session.commit()

    access_token = create_access_token(identity=student_user.id)
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get('/api/admin/dashboard', headers=headers)
    assert response.status_code == 403
    assert b'Access denied' in response.data