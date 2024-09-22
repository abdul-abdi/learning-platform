from flask_socketio import emit
from app import socketio

@socketio.on('connect')
def handle_connect():
    emit('connected', {'data': 'Connected'})

@socketio.on('join')
def on_join(data):
    user_id = data['user_id']
    socketio.emit('user_joined', {'user_id': user_id}, room=user_id)

def send_notification(user_id, notification):
    socketio.emit('notification', notification, room=user_id)