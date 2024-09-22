from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.decorators import role_required

class SomeProtectedResource(Resource):
    @jwt_required()
    @role_required(['admin', 'teacher'])
    def get(self):
        # Only admins and teachers can access this route
        return {'message': 'This is a protected resource'}, 200