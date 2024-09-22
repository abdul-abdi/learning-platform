from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.notification import Notification
from app.events import send_notification

class NotificationResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        notifications = Notification.query.filter_by(user_id=user_id, read=False).order_by(Notification.created_at.desc()).all()
        return [notification.to_dict() for notification in notifications], 200

    @jwt_required()
    def put(self, notification_id):
        user_id = get_jwt_identity()
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first_or_404()
        notification.read = True
        db.session.commit()
        return {'message': 'Notification marked as read'}, 200

class NotificationListResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        notification = Notification(user_id=user_id, message=data['message'], type=data['type'])
        db.session.add(notification)
        db.session.commit()
        send_notification(user_id, notification.to_dict())
        return notification.to_dict(), 201