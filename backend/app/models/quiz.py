from app import db
from datetime import datetime

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('learning_material.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'material_id': self.material_id,
            'title': self.title,
            'description': self.description,
            'questions': [question.to_dict() for question in self.questions],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 'multiple_choice', 'true_false', 'short_answer'
    correct_answer = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON)  # For multiple choice questions

    def to_dict(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'options': self.options
        }