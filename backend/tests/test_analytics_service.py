import pytest
from app.models.user import User
from app.models.learning_material import LearningMaterial
from app.models.user_analytics import UserAnalytics
from app.services.analytics_service import AnalyticsService

def test_track_material_view(init_database):
    user = User.query.filter_by(username='testuser1').first()
    material = LearningMaterial.query.first()

    AnalyticsService.track_material_view(user.id, material.id)

    analytics = UserAnalytics.query.filter_by(user_id=user.id, material_id=material.id).first()
    assert analytics is not None
    assert analytics.view_count == 1

    # Test incrementing view count
    AnalyticsService.track_material_view(user.id, material.id)
    assert analytics.view_count == 2

def test_track_quiz_completion(init_database):
    user = User.query.filter_by(username='testuser1').first()
    material = LearningMaterial.query.first()

    AnalyticsService.track_quiz_completion(user.id, material.id, 80)

    analytics = UserAnalytics.query.filter_by(user_id=user.id, material_id=material.id).first()
    assert analytics is not None
    assert analytics.quiz_attempts == 1
    assert analytics.highest_quiz_score == 80

    # Test updating highest score
    AnalyticsService.track_quiz_completion(user.id, material.id, 90)
    assert analytics.quiz_attempts == 2
    assert analytics.highest_quiz_score == 90

    # Test not updating highest score
    AnalyticsService.track_quiz_completion(user.id, material.id, 85)
    assert analytics.quiz_attempts == 3
    assert analytics.highest_quiz_score == 90