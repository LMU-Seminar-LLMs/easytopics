import sqlite3


class TextDB:
    def __init__(self, db_name: str = "texts.sqlite3") -> None:
        self.conn = sqlite3.connect(db_name)
        self.init_tables()
    
    def __del__(self) -> None:
        self.close_connection()

    def close_connection(self) -> None:
        self.conn.close()

    def init_tables(self) -> None:
        """
        Initialize the tables in the database.

        Creates tables Documents, Questions,  Answers, Topics if they do not exist.

        """
        with self.conn as conn:
            cursor = conn.cursor()                         
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Documents (
                    id INTEGER PRIMARY KEY,
                    doc TEXT NOT NULL
                )
                """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Topics (
                    id INTEGER PRIMARY KEY,
                    external_id INT NOT NULL,
                    topic_representation TEXT NOT NULL
                )
                """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Questions (
                    id INTEGER PRIMARY KEY,
                    question TEXT NOT NULL
                )
                """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Answers (
                    id INTEGER PRIMARY KEY,
                    doc_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    topic_id INTEGER,
                    FOREIGN KEY (question_id) REFERENCES Questions(id) ON DELETE CASCADE,
                    FOREIGN KEY (doc_id) REFERENCES Documents(id) ON DELETE CASCADE,
                    FOREIGN KEY (topic_id) REFERENCES Topics(id)
                )
                """)
            
    def insert_document(self, doc: str) -> int:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Documents (doc) VALUES (?)", (doc, ))
            return cursor.lastrowid
    
    def insert_topic(self, external_id: int, topic_representation: str) -> int:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Topics (external_id, topic_representation) VALUES (?, ?)", (external_id, topic_representation))
            return cursor.lastrowid
        
    def insert_question(self, question: str) -> int:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Questions (question) VALUES (?)", (question, ))
            return cursor.lastrowid
    
    def remove_question(self, question_id: int) -> None:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Questions WHERE id = ?", (question_id, ))
    
    def insert_answer(self, doc_id: int, question_id: int, answer: str) -> int:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Answers (doc_id, question_id, answer) VALUES (?, ?, ?)", (doc_id, question_id, answer))
            return cursor.lastrowid
    
    def remove_answer(self, answer_id: int) -> None:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Answers WHERE id = ?", (answer_id, ))
    
    def get_documents(self) -> list[str]:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor = cursor.execute("SELECT * FROM Documents")
            return cursor.fetchall()
    
    def get_questions(self) -> list[str]:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor = cursor.execute("SELECT * FROM Questions")
            return cursor.fetchall()
    
    def get_answers(self) -> list[str]:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor = cursor.execute("SELECT * FROM Answers")
            return cursor.fetchall()
    
    def get_topics(self) -> list[str]:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor = cursor.execute("SELECT * FROM Topics")
            return cursor.fetchall()
        
    def get_answers_by_doc(self, doc_id: int) -> list[tuple]:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor = cursor.execute("SELECT * FROM Answers WHERE doc_id = ?", (doc_id, ))
            return cursor.fetchall()
