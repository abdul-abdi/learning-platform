from celery import Celery
from celery.schedules import crontab
from app import create_app, db
from app.models.user import User
from app.models.learning_material import LearningMaterial
from app.services.recommendation_service import RecommendationService
from datetime import datetime
import os

celery = Celery(__name__)
celery.conf.broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
celery.conf.result_backend = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

app = create_app(os.getenv('FLASK_ENV', 'development'))
app.app_context().push()

@celery.task
def generate_recommendations(user_id):
    with app.app_context():
        recommendations = RecommendationService.get_recommendations(user_id)
        # Store recommendations in the database or cache
        # This is a placeholder - you'd need to implement the storage logic
        return recommendations

@celery.task
def update_learning_materials():
    with app.app_context():
        materials = LearningMaterial.query.all()
        for material in materials:
            material.last_updated = datetime.utcnow()
        db.session.commit()

@celery.task
def update_all_user_recommendations():
    with app.app_context():
        users = User.query.all()
        for user in users:
            generate_recommendations.delay(user.id)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Update recommendations for all users every day at midnight
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        update_all_user_recommendations.s(),
    )

    # Update learning materials every week on Monday at 1:00 AM
    sender.add_periodic_task(
        crontab(hour=1, minute=0, day_of_week=1),
        update_learning_materials.s(),
    )