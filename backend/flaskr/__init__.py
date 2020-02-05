import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from random import shuffle


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Helper functions
def pagination_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in selection]
    return formatted_questions[start:end]


def get_next_question(questions, previous_questions):
    for question in questions:
        if question.id not in previous_questions:
            return question


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Configure the CORS
    CORS(app)

    """
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  """
    """
  @TODO: Use the after_request decorator to set Access-Control-Allow
  """

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
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

    @app.route("/categories")
    def get_categories():
        all_categories = Category.query.all()
        # if there is no categories, will return not found
        if len(all_categories) == 0:
            abort(404)
        # categories = [category.type for category in all_categories]
        categories = {}
        for category in all_categories:
            categories[category.id] = category.type

        return jsonify({"success": True, "categories": categories})

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
        # Get the Questions
        selection = Question.query.order_by(Question.id).all()
        current_questions = pagination_questions(request, selection)
        # In case no questions shall return not found
        if len(current_questions) == 0:
            abort(404)

        # Get the Categories
        all_categories = Category.query.all()
        # If there is no categories, will return not found
        if len(all_categories) == 0:
            abort(404)
        # categories = [category.type for category in all_categories]
        categories = {}
        for category in all_categories:
            categories[category.id] = category.type

        # Assumed the current category is the first category
        current_category = categories[1]
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "current_category": current_category,
                "categories": categories,
            }
        )

    """
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """
      This API is used to delete the question
      """
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question == None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = pagination_questions(request, selection)
            return jsonify(
                {
                    "success": True,
                    "deleted": question.id,
                    "questions": current_questions,
                    "total_questions": len(selection),
                }
            )
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
    def add_question():
        """
      This API is used to add question
      """
        body = request.get_json()
        question = body.get("question", None)
        answer = body.get("answer", None)
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)
        search_term = body.get("searchTerm", None)
        # check search term
        if search_term is not None:  # None is explit, to do search in case empty string
            # Remove spaces from the begining and end
            search_term = search_term.strip()
            selection = Question.query.filter(
                Question.question.ilike("%{}%".format(search_term))
            )
            current_questions = pagination_questions(request, selection)
            # Get all the questions to get the count of questions not only the searched .
            all_questions = Question.query.all()
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(all_questions),
                }
            )
        else:
            # Validate that I have all the values
            if not question or not answer or not difficulty or not category:
                abort(422)
            try:
                question = Question(
                    question=question,
                    answer=answer,
                    difficulty=difficulty,
                    category=category,
                )
                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = pagination_questions(request, selection)
                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "questions": current_questions,
                        "total_questions": len(selection),
                    }
                )
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

    """
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  """

    @app.route("/categories/<int:category_id>/questions")
    def get_questions_per_category(category_id):
        # validate the id is of valid category as it is get request it is exposed in url
        category = Category.query.filter(Category.id == category_id).one_or_none()
        # If there is no category, we have to return bad request
        if not category:
            abort(400)

        selection = Question.query.filter(Question.category == category_id).all()
        current_questions = pagination_questions(request, selection)
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "current_category": category.type,
            }
        )

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
    def get_quiz():
        body = request.get_json()
        quiz_category = body.get("quiz_category")
        previous_questions = body.get("previous_questions")
        category = Category.query.filter(
            Category.type == quiz_category.get("type")
        ).one_or_none()
        if category:
            # Then it is one of the categories
            questions = Question.query.filter(Question.category == category.id).all()
        else:
            # then All is selected
            questions = Question.query.all()

        # The user has got all the questions
        if len(questions) == len(previous_questions):
            return jsonify({"success": True})

        # I used to shuffle the array everytime to get a random generations
        shuffle(questions)
        question = get_next_question(questions, previous_questions)
        return jsonify({"success": True, "question": question.format()})

    """
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "internal server error"}
            ),
            500,
        )

    return app

