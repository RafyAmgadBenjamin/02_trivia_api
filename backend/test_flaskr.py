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
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    # TODO  # the error scenario for the above API
    # delete all categores, create the test, add all the categories
    # def test_404_for_no_catigories(self):
    #     categories = Category.query.all()
    #     with app.app_context():
    #         self.db = SQLAlchemy()
    #         for category in categories:
    #             self.db.session.delete(category)
    #         try:
    #             self.db.session.commit()
    #         except:
    #             self.db.session.rollback()

    #         res = self.client().get("/categories")
    #         data = json.loads(res.data)
    #         self.assertEqual(res.status_code, 404)

    #         for category in categories:
    #             self.db.session.add(Category)
    #         try:
    #             self.db.session.commit()
    #         except:
    #             self.db.session.rollback()

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
