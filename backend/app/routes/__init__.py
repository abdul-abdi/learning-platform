from .user_routes import UserRegistration, UserLogin, UserProfileResource
from .learning_material_routes import LearningMaterialResource, LearningMaterialList
from .user_progress_routes import UserProgressResource
from .recommendation_routes import RecommendationResource
from .quiz_routes import QuizResource
from .user_analytics_routes import UserAnalyticsResource
from .learning_path_routes import LearningPathResource, LearningPathListResource, UserLearningPathProgressResource
from .forum_routes import ForumPostResource, ForumPostListResource
from .notification_routes import NotificationResource, NotificationListResource
from .badge_routes import UserBadgeResource
from .dashboard_routes import UserDashboardResource

def initialize_routes(api):
    api.add_resource(UserRegistration, '/api/auth/register')
    api.add_resource(UserLogin, '/api/auth/login')
    api.add_resource(UserProfileResource, '/api/users/profile')
    api.add_resource(LearningMaterialResource, '/api/learning-materials/<int:id>')
    api.add_resource(LearningMaterialList, '/api/learning-materials')
    api.add_resource(UserProgressResource, '/api/user-progress')
    api.add_resource(RecommendationResource, '/api/recommendations')
    api.add_resource(QuizResource, '/api/quizzes/<int:material_id>')
    api.add_resource(UserAnalyticsResource, '/api/user-analytics')
    api.add_resource(LearningPathResource, '/api/learning-paths/<int:path_id>')
    api.add_resource(LearningPathListResource, '/api/learning-paths')
    api.add_resource(UserLearningPathProgressResource, '/api/learning-paths/<int:path_id>/progress')
    api.add_resource(ForumPostResource, '/api/forum/<int:material_id>')
    api.add_resource(ForumPostListResource, '/api/forum')
    api.add_resource(NotificationResource, '/api/notifications/<int:notification_id>')
    api.add_resource(NotificationListResource, '/api/notifications')
    api.add_resource(UserBadgeResource, '/api/user/badges')
    api.add_resource(UserDashboardResource, '/api/dashboard')
