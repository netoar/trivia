import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, abort
from model.db import db
from model.Category import get_categories
import random

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


def map_questions(questions_raw):
    current_questions = [question.format() for question in questions_raw]
    return current_questions


def paginate_questions(page: int) -> tuple:
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    pagination = (start, end)
    return pagination


def get_question_by_id(question_id):
    question = Question.query.filter_by(id=question_id).first()
    return question


def get_first_question():
    question = Question.query.first()
    return question


def get_questions(page):
    questions_raw = Question.query.paginate(
        page=page,
        per_page=QUESTIONS_PER_PAGE,
        error_out=True,
        max_per_page=QUESTIONS_PER_PAGE,
    )
    questions = map_questions(questions_raw.items)
    categories = get_categories()

    return {
        "questions": questions,
        "total_questions": len(questions),
        "currentCategory": None,
        "categories": list(map(lambda category: category["type"], categories)),
        "total_pages": questions_raw.pages,
        "success": True,
    }


def delete_question_by_id(question_id: int):
    category = 0
    try:
        question_to_remove = Question.query.filter_by(id=question_id).first()
        category = question_to_remove.category
        question_to_remove.delete()
    except Exception as e:
        abort(422)
        db.session.rollback()
    finally:
        db.session.close()
    questions = get_questions_category(category, False, 1)
    return questions


def post_question(body):
    try:
        question_new = Question(
            question=body.get("question") or None,
            answer=body.get("answer") or None,
            category=body.get("category") or None,
            difficulty=body.get("difficulty") or None,
        )
        categories = []
        categories_raw = get_categories()
        categories = list(map(lambda category: category["id"], categories_raw))
        if question_new.category in categories:
            question_new.insert()
        else:
            abort(422)
    except Exception as e:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()
    questions = get_questions(1)
    return questions


def get_questions_category(category_id: int, offset: bool, page) -> dict:
    category = category_id + 1 if offset else category_id
    questions_raw = Question.query.filter_by(category=str(category)).paginate(
        page=page,
        per_page=QUESTIONS_PER_PAGE,
        error_out=True,
        max_per_page=QUESTIONS_PER_PAGE,
    )
    if questions_raw.items is not []:
        abort(404)
    questions = map_questions(questions_raw.items)
    return {
        "questions": questions,
        "total_questions": len(questions),
        "total_pages": questions_raw.pages,
        "success": True,
    }


def search_term(search_term, page):
    questions_search = Question.query.filter(
        Question.question.ilike("%" + search_term + "%")
    ).all()
    pagination = paginate_questions(page)
    results = map_questions(questions_search)
    return {"questions": results, "total_questions": len(results), "success": True}


def play(category_id, previous):
    category = category_id
    previous_question = []
    questions = []

    if category == 0:  # all categories
        questions_raw = Question.query.all()
    else:
        questions_raw = Question.query.filter_by(category=str(category)).all()

    if previous != []:
        for question in questions_raw:
            if question.id not in previous:
                questions.append(question)
    else:
        for question in questions_raw:
            questions.append(question)

    question_selected = random.choice(questions)
    current_question = Question.format(question_selected)

    return {"previousQuestion": previous, "question": current_question, "success": True}
