from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.decorators import role_required

class AdminDashboardResource(Resource):
    @jwt_required()
    @role_required(['admin'])
    def get(self):
        # Admin dashboard logic here
        return {'message': 'Admin dashboard data'}, 200

class TeacherManagementResource(Resource):
    @jwt_required()
    @role_required(['admin'])
    def get(self):
        # Teacher management logic here
        return {'message': 'Teacher management data'}, 200