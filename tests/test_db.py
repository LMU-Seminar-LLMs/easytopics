import unittest
from db import TextDB  # Import the TextDB class from your module

class TestTextDB(unittest.TestCase):

    def set_up(self):
        self.db = TextDB(":memory:")  # Use an in-memory SQLite database for testing

    def tear_down(self):
        del self.db  # Close the connection and delete the instance

    def test_insert_document(self):
        doc_id = self.db.insert_document("Test Document")
        self.assertIsNotNone(doc_id)

    def test_insert_topic(self):
        topic_id = self.db.insert_topic(1, "Test Topic")
        self.assertIsNotNone(topic_id)

    def test_insert_question(self):
        question_id = self.db.insert_question("Test Question")
        self.assertIsNotNone(question_id)

    def test_remove_question(self):
        question_id = self.db.insert_question("Test Question")
        self.db.remove_question(question_id)
        questions = self.db.get_questions()
        self.assertNotIn((question_id, "Test Question"), questions)

    def test_insert_answer(self):
        doc_id = self.db.insert_document("Test Document")
        question_id = self.db.insert_question("Test Question")
        answer_id = self.db.insert_answer(doc_id, question_id, "Test Answer")
        self.assertIsNotNone(answer_id)

    def test_remove_answer(self):
        doc_id = self.db.insert_document("Test Document")
        question_id = self.db.insert_question("Test Question")
        answer_id = self.db.insert_answer(doc_id, question_id, "Test Answer")
        self.db.remove_answer(answer_id)
        answers = self.db.get_answers()
        self.assertNotIn((answer_id, doc_id, question_id, "Test Answer", None), answers)

    def test_get_documents(self):
        self.db.insert_document("Test Document 1")
        self.db.insert_document("Test Document 2")
        documents = self.db.get_documents()
        self.assertEqual(len(documents), 2)

    def test_get_questions(self):
        self.db.insert_question("Test Question 1")
        self.db.insert_question("Test Question 2")
        questions = self.db.get_questions()
        self.assertEqual(len(questions), 2)

    def test_get_answers(self):
        doc_id = self.db.insert_document("Test Document")
        question_id = self.db.insert_question("Test Question")
        self.db.insert_answer(doc_id, question_id, "Test Answer")
        answers = self.db.get_answers()
        self.assertEqual(len(answers), 1)

    def test_get_topics(self):
        self.db.insert_topic(1, "Test Topic 1")
        self.db.insert_topic(2, "Test Topic 2")
        topics = self.db.get_topics()
        self.assertEqual(len(topics), 2)

    def test_get_answers_by_doc(self):
        doc_id = self.db.insert_document("Test Document")
        question_id = self.db.insert_question("Test Question")
        answer_id = self.db.insert_answer(doc_id, question_id, "Test Answer")
        answers = self.db.get_answers_by_doc(doc_id)
        self.assertIn((answer_id, doc_id, question_id, "Test Answer", None), answers)

if __name__ == '__main__':
    unittest.main()
