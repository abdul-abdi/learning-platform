from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.quiz import Quiz, QuizQuestion
from app.models.user_progress import UserProgress

class QuizResource(Resource):
    @jwt_required()
    def get(self, material_id):
        quiz = Quiz.query.filter_by(material_id=material_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        return quiz.to_dict(), 200

    @jwt_required()
    def post(self, material_id):
        user_id = get_jwt_identity()
        data = request.get_json()
        
        quiz = Quiz.query.filter_by(material_id=material_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        score = 0
        total_questions = len(quiz.questions)

        for answer in data['answers']:
            question = QuizQuestion.query.get(answer['question_id'])
            if question.correct_answer == answer['user_answer']:
                score += 1

        percentage_score = (score / total_questions) * 100

        # Update user progress
        progress = UserProgress.query.filter_by(user_id=user_id, material_id=material_id).first()
        if progress:
            progress.progress_percentage = max(progress.progress_percentage, percentage_score)
            if percentage_score == 100:
                progress.status = 'completed'
        else:
            progress = UserProgress(user_id=user_id, material_id=material_id, 
                                    status='in_progress', progress_percentage=percentage_score)
            db.session.add(progress)

        db.session.commit()

        return {
            'score': score,
            'total_questions': total_questions,
            'percentage_score': percentage_score
        }, 200