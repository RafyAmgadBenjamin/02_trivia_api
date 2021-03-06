import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "rafy", "admin", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)
        self.question = Question(
            question="What is the capital of egypt ?",
            answer="cario",
            category=3,
            difficulty=2,
        )

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    @TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        # Act
        res = self.client().get("/categories")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_paginated_questions(self):
        # Act
        res = self.client().get("/questions")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_beyond_valid_page_for_questions(self):
        # Act
        res = self.client().get("/questions?page=10000")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question(self):
        """
        To keep the database consistent and to be able to run this test many times i will add a question then delete
        the added quesion.
        """
        # Arrange
        self.question.insert()
        question_id = self.question.id

        # Act
        res = self.client().delete(f"/questions/{question_id}")
        data = json.loads(res.data)
        # shall return None as I have deleted this question
        question = Question.query.filter(Question.id == question_id).one_or_none()

        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], question_id)
        self.assertTrue(data["questions"])
        self.assertEqual(question, None)

    def test_404_if_question_does_not_exist(self):
        # Act
        res = self.client().delete("/questions/999999")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")

    def test_add_new_question(self):
        # Arrange
        # convert the question object to Json object
        question = {
            "question": self.question.question,
            "category": self.question.category,
            "answer": self.question.answer,
            "difficulty": self.question.difficulty,
        }
        # Act
        res = self.client().post("/questions", json=question)
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_405_if_question_adding_not_allowed(self):
        # Arrange
        # convert the question object to Json object
        question = {
            "question": self.question.question,
            "category": self.question.category,
            "answer": self.question.answer,
            "difficulty": self.question.difficulty,
        }

        # Act
        res = self.client().post("/questions/45", json=question)
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "not allowed")

    def test_422_if_question_is_not_processable(self):
        """
        Posting a question but without answer shall be not processable
        """
        # Arrange
        # convert the question object to Json object
        question = {
            "question": self.question.question,
            "category": self.question.category,
            "answer": None,
            "difficulty": self.question.difficulty,
        }
        # Act
        res = self.client().post("/questions", json=question)
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_get_question_search_with_results(self):
        # ACT
        search_term = {"searchTerm": "penicillin"}
        res = self.client().post("/questions", json=search_term)
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertEqual(len(data["questions"]), 1)
        self.assertEqual(data["total_questions"], 1)

    def test_get_question__search_without_results(self):
        # ACT
        search_term = {"searchTerm": "dfnaksdfdilkjlf3jiojjojjd"}
        res = self.client().post("/questions", json=search_term)
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 0)
        self.assertEqual(data["total_questions"], 0)

    def test_get_question_per_category(self):
        # Act
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 3)
        self.assertEqual(data["total_questions"], 3)
        self.assertEqual(data["current_category"], "Science")

    def test_400_if_the_category_is_not_valid(self):
        # Act
        res = self.client().get("/categories/1000/questions")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data["message"], "bad request")

    def test_get_quiz(self):
        # Act
        posted_data = {
            "previous_questions": [28],
            "quiz_category": {"type": "Sports", "id": "6"},
        }
        res = self.client().post("/quizzes", json=posted_data)
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        # validate that the returned question of the same category I have selected
        self.assertEqual(data["question"]["category"], 6)

    def test_400_post_invalid_category_for_quiz(self):
        # Act
        posted_data = {
            "previous_questions": [28],
            "quiz_category": {"type": "", "id": ""},
        }
        res = self.client().post("/quizzes", json=posted_data)
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data["message"], "bad request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
