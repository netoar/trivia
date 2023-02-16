import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
from model import Question, db, Category


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db.setup_db(app)
    cors = CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"

    @app.route("/")
    def hello():
        return jsonify({"message": "hello"})

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.route("/after_request")
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories/")
    @cross_origin()
    def get_requests():
        categories = Category.get_categories()
        return jsonify({"categories": categories})

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions")
    def get_questions():
        page = request.args.get("page", 1, type=int)
        questions = Question.get_questions(page)
        return jsonify(questions)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        questions = Question.delete_question_by_id(question_id)
        return jsonify(questions)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=["POST"])
    def post_question():
        questions = Question.post_question(request.get_json())
        return jsonify(questions)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions/search", methods=["POST"])
    def search_venues():
        body = request.get_json()
        page = request.args.get("page", 1, type=int)
        search_term = body.get("searchTerm" or None)
        if search_term is not None:
            questions = Question.search_term(search_term, page)
        return jsonify(questions)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_based_category(category_id):
        page = request.args.get("page", 1, type=int)
        questions = Question.get_questions_category(category_id, True, page)
        return jsonify(questions)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def play():
        body = request.get_json()
        previous = body.get("previous_questions" or None)
        category_raw = body.get("quiz_category" or None)
        category_id = category_raw.get("id" or None)
        question = Question.play(category_id, previous)
        return jsonify(question)

    """
    @TODO:
    Create error handlers for all expected errors
    400, 404, 422, and 500.
    """

    @app.errorhandler(400)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 400, "message": "resource not found"}),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 500, "message": "unprocessable"}),
            500,
        )

    return app
