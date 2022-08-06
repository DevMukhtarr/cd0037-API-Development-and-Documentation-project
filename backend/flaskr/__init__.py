import os
from unicodedata import category
from flask import Flask, request, abort, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from sqlalchemy import delete

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=["GET"])
    @cross_origin()
    def get_categories():
        try: 
            all_categories = {}
            categories = Category.query.order_by(Category.id).all()
            # formatted_categories = [category.format() for category in categories]
            for category in categories:
                all_categories[category.id] = category.type
            return jsonify({
                'success': True,
                'categories': all_categories
            })
        except:
            abort(404)
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
    @app.route("/questions", methods=["GET"])
    @cross_origin()
    def get_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()
            category_object = {}
            questions_list= []
            page = request.args.get('page', 1, type=int)
            start = ( page - 1 ) * QUESTIONS_PER_PAGE
            end = start + 10
            for category in categories:
                category_object[category.id] = category.type
            for question in questions:
                questions_list.append({
                    "id": question.id,
                    "question": question.question,
                    "answer": question.answer,
                    "difficulty": question.difficulty,
                    "category": question.category
                })
            return jsonify({
                "success": True,
                "questions": questions_list[start:end],
                "totalQuestions": len(questions),
                "categories": category_object
                })
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:id>", methods=["DELETE"])
    @cross_origin()
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()

            question.delete()

            return jsonify({
                "success": True,
                "message": "Question deleted successfully"
                })

        except:
            abort(422)
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
    @cross_origin()
    def new_question():
        try:
            body = request.get_json()
            if "question" in body:
                new_question = body.get("question")
            if "answer" in body:
                new_answer = body.get("answer")
            if "difficulty" in body:
                new_difficulty= body.get("difficulty")
            if "category" in body:
                new_category = body.get("category")
            else:
                return jsonify({
                    'success': False,
                    'message': "required body not present" 
                })

            try:
                new_question_to_add = Question(
                question = new_question,
                answer = new_answer,
                difficulty= new_difficulty,
                category = new_category
                )

                new_question_to_add.insert()
                return jsonify({
                    'success': True,
                    'message': "new question added" 
                })
            except:
                return jsonify({
                    'success': False,
                    'message': "could not add" 
                })
        except:
            abort(422)      

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
    @cross_origin()
    def search_question():
        try:
            body = request.get_json()
            all_questions = []
            all_categories = {}
            categories = Category.query.order_by(Category.id).all()
            questions = Question.query.order_by(Question.id).all()
            if "searchTerm" in body:
                search_term = body.get("searchTerm")

            for question in questions:
                if(search_term) in question.question.lower():
                    all_questions.append({
                        "id": question.id,
                        "question": question.question,
                        "answer": question.answer,
                        "difficulty": question.difficulty,
                        "category": question.category
                    })
            for category in categories:
                all_categories[category.id] = category.type

            else:   
                return jsonify({
                    'success': True,
                    'questions': all_questions,
                    'totalQuestions': len(questions),
                    'currentCategory': all_categories[all_questions[0]["category"]]
                })
        except:
            abort(404)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:id>/questions", methods=["GET"])
    @cross_origin()
    def get_questions_based_on_category(id):
        try:
            all_categories = {}
            all_questions = []
            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()
            for question in questions:
                if question.category == id:
                    all_questions.append({
                        "id": question.id,
                        "question": question.question,
                        "answer": question.answer,
                        "difficulty": question.difficulty,
                        "category": question.category
                    })
            for category in categories:
                all_categories[category.id] = category.type
            return jsonify({
                "success": True,
                "questions": all_questions,
                "totalQuestions": len(questions),
                "currentCategory": all_categories[all_questions[0]["category"]]
            }) 
        except:
            abort(404)
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
    @cross_origin()
    def get_next_question():
        try:
            body = request.get_json()
            questions = Question.query.order_by(Question.id).all()
            selected_question = {}
            all_questions_id = []
            if "previous_questions" in body:
                previous_questions = body.get("previous_questions")
            if "quiz_category" in body:
                quiz_category = body.get("quiz_category")
                quiz_category_id = quiz_category['id']

            for question in questions:
                all_questions_id.append(question.id)
            if quiz_category_id == 0:
                new_question = random.choice(all_questions_id)
                for question in questions:
                    if question.id == new_question and question.id not in previous_questions :
                        selected_question["id"] = question.id
                        selected_question["question"] = question.question
                        selected_question["answer"] = question.answer
                        selected_question["difficulty"] = question.difficulty
                        selected_question["category"] = question.category
            else:  
                questions = Question.query.filter(Question.category == quiz_category_id).all()
                for question in questions:
                    new_question = random.choice(questions)
                if new_question.id not in previous_questions:
                    selected_question["id"] = new_question.id
                    selected_question["question"] = new_question.question
                    selected_question["answer"] = new_question.answer
                    selected_question["difficulty"] = new_question.difficulty
                    selected_question["category"] = new_question.category
                else:
                    return jsonify({
                "success": "False",
                "message": "All questions have been provided"
            })
            return jsonify({
                "success": True,
                "question": selected_question
            })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    # not found
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": 'resource not found',
            "error": 404
        }), 404
    #unprocessable 
    @app.errorhandler(422)
    def operation_unprocessable(error):
        return jsonify({
            "success": False,
            "message": 'operation unprocessable',
            "error": 422
        }), 422

    return app

