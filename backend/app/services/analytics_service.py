from app.models.user_analytics import UserAnalytics
from app import db

class AnalyticsService:
    @staticmethod
    def track_material_view(user_id, material_id):
        analytics = UserAnalytics.query.filter_by(user_id=user_id, material_id=material_id).first()
        if analytics:
            analytics.view_count += 1
        else:
            analytics = UserAnalytics(user_id=user_id, material_id=material_id, view_count=1)
        db.session.add(analytics)
        db.session.commit()

    @staticmethod
    def track_quiz_completion(user_id, material_id, score):
        analytics = UserAnalytics.query.filter_by(user_id=user_id, material_id=material_id).first()
        if analytics:
            analytics.quiz_attempts += 1
            analytics.highest_quiz_score = max(analytics.highest_quiz_score, score)
        else:
            analytics = UserAnalytics(user_id=user_id, material_id=material_id, quiz_attempts=1, highest_quiz_score=score)
        db.session.add(analytics)
        db.session.commit()