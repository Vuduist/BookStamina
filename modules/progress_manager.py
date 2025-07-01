import sqlite3
import os

class ProgressManager:
    def __init__(self, db_path="progress.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS progress (
            book_title TEXT PRIMARY KEY,
            position INTEGER
        )''')
        conn.commit()
        conn.close()

    def save_progress(self, book_title, position):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('REPLACE INTO progress (book_title, position) VALUES (?, ?)', (book_title, position))
        conn.commit()
        conn.close()

    def load_progress(self, book_title):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT position FROM progress WHERE book_title=?', (book_title,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else 0 