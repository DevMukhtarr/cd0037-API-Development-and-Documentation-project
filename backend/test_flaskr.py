import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import TEST_DB_NAME, DB_USER


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
        self.database_path = DB_USER+"://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
        self.new_question = {
            "question": "who is the fastest runner in the world",
            "answer": "usain bolt",
            "category": 6,
            "difficulty": 1
        }
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

        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["categories"])

    def test_add_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"])

    def test_add_new_question_not_successful(self):
        res = self.client().post("/questions", json={
            "question": "who is the fastest runner in the world",
            "answer": "usain bolt",
            "category": 6
        })
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])


    def test_search_new_question_gotten(self):
        res = self.client().post("/questions/search", json={"searchTerm": "who"})
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["currentCategory"])

    def test_search_new_question_not_successful(self):
        res = self.client().post("/questions/search", json={"searchTerm": "xjjjwijbwqi"})
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])
        self.assertEqual(data["error"], 404)


    def test_get_categories_of_questions_by_id(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["currentCategory"])

    def test_get_categories_of_questions_by_id_not_successful(self):
        res = self.client().get("/categories/9/questions")
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])
        self.assertEqual(data["error"], 404)


    def test_get_categories_of_questions_by_id(self):
        res = self.client().post("/quizzes", json={"previous_questions": [], 
        'quiz_category': {'id': '5', 'type': 'Entertainment'}})
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_get_categories_of_questions_by_id(self):
        res = self.client().post("/quizzes", json={"previous_questions": [], 
        'quiz_category': {}})
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])
        self.assertTrue(data["error"])


    def test_delete_question_by_id_not_successful(self):
        res = self.client().delete("/questions/2000")
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_delete_question_by_id_successful(self):
        res = self.client().delete("/questions/12")
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()