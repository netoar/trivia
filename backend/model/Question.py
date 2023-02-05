import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from model.db import db

QUESTIONS_PER_PAGE = 10


class Question(db.Model):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "difficulty": self.difficulty,
        }


def map_questions(questions_raw, pagination):
    questions = [question.format() for question in questions_raw]

    # questions = list(map(lambda question: question.format(), questions_raw))

    current_questions = questions[pagination[0] : pagination[1]]

    return current_questions
    """
        questions_json = []
        for question in questions_raw:
            question_json.id = question.id
            question_json.question: question.question
            questions_json.append(question_json)
        return questions_json
        """


def paginate_questions(page: int) -> tuple:
    # page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    pagination = (start, end)
    return pagination


def get_questions():
    questions_raw = Question.query.all()
    # pagination = paginate_questions(request.page)  # request????

    questions = map_questions(questions_raw, (1, 5))
    return {"questions": questions}
