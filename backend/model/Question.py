import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from model.db import db
from model.Category import get_categories

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
    # current_questions = questions[pagination[0] : pagination[1]]
    current_questions = questions[0 : pagination[1]]
    return current_questions


def paginate_questions(page: int) -> tuple:
    # TODO arreglar la paginación
    # page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    pagination = (start, end)
    return pagination


def get_questions():
    questions_raw = Question.query.all()
    pagination = paginate_questions(len(questions_raw))
    questions = map_questions(questions_raw, pagination)
    categories = get_categories()

    return {
        "questions": questions,
        "totalQuestions": len(questions),
        "categories": list(map(lambda category: category["type"], categories)),
    }


def delete_question_by_id(question_id: int):
    question_to_remove = Question.filter_by(id=question_id).first()
    try:
        Question.delete(question_to_remove)
    except:
        abort(422)
        db.session.rollback()
    finally:
        db.session.close()
    questions = get_questions()
    return questions


def post_question():
    body = request.get_json()
    question_new.question = body.get("question", None)
    question_new.answer = body.get("answer", None)
    question_new.category = body.get("category", None)
    question_new.difficulty = body.get("difficulty", None)
    try:
        Question.insert(question_new)
    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()
    questions = get_questions()
    return questions


def get_questions_category(category_id: int) -> dict:
    questions_raw = Question.query.filter_by(category=category_id).all()
    pagination = paginate_questions(len(questions_raw))
    questions = map_questions(questions_raw, pagination)
    return {"questions": questions}
