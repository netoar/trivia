import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from model import Question, db, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres@localhost:5432/trivia_test"
        db.setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.reflect()
            # self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    new_question = {
        "question": "Where does Coco Channel live?",
        "answer": "Paris",
        "category": 1,
        "difficulty": 1,
    }

    new_question_error = {
        "question": "Where does not Coco Channel live?",
        "answer": "Too many correct answers",
        "category": "error",
        "difficulty": 1,
    }

    def test_1_get_categories(self):
        # GET all the categories
        # category = Category.add_category()
        result_raw = self.client().get("/categories/")
        result = json.loads(result_raw.data)
        self.assertTrue(
            result["categories"],
        )

    def test_2_create_question(self):
        # CREATE new question

        result_raw = self.client().post("/questions", json=self.new_question)
        result = json.loads(result_raw.data)
        self.assertTrue(result["success"])
        # this will the first question created in table since we re-create it every time.
        # self.assertEqual(question.question, self.new_question["question"])
        # self.assertEqual(question.answer, self.new_question["answer"])

    def test_3_search_questions(self):
        # SEARCH term success
        searchTerm = "answer"
        result = self.client().post(
            "/questions/search", json={"searchTerm": searchTerm}
        )
        result_json = json.loads(result.data)
        # result_questions = Question.query.filter(
        #     Question.question.ilike(f"%{searchTerm}%")
        # )
        self.assertEqual(result.status_code, 200)

    def test_4_get_category_questions(self):
        # GET all questions of a category
        result = self.client().get("/categories/1/questions")
        result_json = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(result_json["questions"], True)

    def test_5_delete_question(self):
        # DELETE a question
        question = Question.get_first_question()
        path = "/questions/" + str(question.id)
        result = self.client().delete(path)
        results = json.loads(result.data)
        question_deleted = Question.get_question_by_id(question.id)
        self.assertEqual(question_deleted, None)

    def test_6_quizzes_all(self):
        # Get a question from all categories
        # Confirm the question isn't in the previous question
        result = self.client().post(
            "/quizzes",
            json={
                "quiz_category": {"id": 0, "type": "All"},
                "previous_questions": [1, 2],
            },
        )
        result_json = json.loads(result.data)
        question = result_json["question"]
        previous = result_json["previousQuestion"]
        self.assertEqual(result.status_code, 200)
        self.assertNotIn(question["id"], previous)

    def test_7_quizzes_category(self):
        # Get a question from a given category
        result = self.client().post(
            "/quizzes",
            json={
                "quiz_category": {"id": 1, "type": "Science"},
                "previous_questions": [1, 2],
            },
        )
        result_json = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result_json["question"]["category"], "1")

    def test_8_500_viewQuiz(self):
        result = self.client().post(
            "/quizzes",
            json={
                "quiz_category": {"id": 400, "type": "Science"},
                "previous_questions": [1, 2],
            },
        )
        result_json = json.loads(result.data)
        self.assertEqual(result.status_code, 500)

    def test_9_404_get_category_questions(self):
        result = self.client().get("/categories/100/questions")
        result_json = json.loads(result.data)
        self.assertEqual(result.status_code, 404)

    def test_10_422_create_question(self):
        result = self.client().post("/questions", json=self.new_question_error)
        result_json = json.loads(result.data)
        self.assertEqual(result.status_code, 422)
        self.assertEqual(result_json["success"], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
