import sqlite3


class TextDB:
    def __init__(self, db_name: str = "texts.sqlite3") -> None:
        self.conn = sqlite3.connect(db_name)
        self.init_tables()

    def init_tables(self) -> None:
        """
        Initialize the tables in the database.

        Creates tables Documents, Questions, and Answers if they do not exist.
        
        :return: None
        """
        with self.conn as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS Documents (
                    id INTEGER PRIMARY KEY,
                    doc TEXT NOT NULL,
                    topic_id INT,
                    FOREIGN KEY (topic_id) REFERENCES Topics(id)
                )
                """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS Questions (
                    id INTEGER PRIMARY KEY,
                    question TEXT NOT NULL,
                )
                """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS Answers (
                    id INTEGER PRIMARY KEY,
                    doc_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES Questions(id) ON DELETE CASCADE,
                    FOREIGN KEY (doc_id) REFERENCES Documents(id) ON DELETE CASCADE
                """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS Topics (
                    id INTEGER PRIMARY KEY,
                    topic_id INT NOT NULL,
                    topic_terms TEXT
                """)
                         
            
    def insert_document(self, doc: str) -> int:
        with self.conn as conn:
            conn.execute("INSERT INTO Documents (doc) VALUES (?)", (doc,))
            return conn.lastrowid
        
    def insert_question(self, question: str) -> int:
        with self.conn as conn:
            conn.execute("INSERT INTO Questions (question) VALUES (?)", (question))
            return conn.lastrowid
    
    def remove_question(self, question_id: int) -> None:
        with self.conn as conn:
            conn.execute("DELETE FROM Questions WHERE id = ?", (question_id,))
    
    def insert_answer(self, doc_id: int, question_id: int, answer: str) -> int:
        with self.conn as conn:
            conn.execute("INSERT INTO Answers (doc_id, question_id, answer) VALUES (?, ?, ?)", (doc_id, question_id, answer))
            return conn.lastrowid
    
    def _get_all(self, table: str) -> list:
        with self.conn as conn:
            cursor = conn.execute(f"SELECT * FROM ?", (table,))
            return cursor.fetchall()
    
    def get_documents(self) -> list:
        return self._get_all("Documents")
    
    def get_questions(self) -> list:
        return self._get_all("Questions")
    
    def get_answers(self) -> list:
        return self._get_all("Answers")
        
    def get_answers_by_doc(self, doc_id: int) -> list:
        with self.conn as conn:
            cursor = conn.execute("SELECT * FROM Answers WHERE doc_id = ?", (doc_id,))
            return cursor.fetchall()
