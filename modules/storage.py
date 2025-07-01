import sqlite3
import datetime

class Storage:
    def __init__(self, db_path="appdata.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            speed REAL,
            accuracy REAL,
            chars_typed INTEGER,
            duration REAL
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS recent_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            title TEXT,
            last_opened TEXT,
            favorite INTEGER DEFAULT 0
        )''')
        conn.commit()
        conn.close()

    def add_history(self, speed, accuracy, chars_typed, duration):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('''INSERT INTO history (datetime, speed, accuracy, chars_typed, duration)
                     VALUES (?, ?, ?, ?, ?)''', (now, speed, accuracy, chars_typed, duration))
        conn.commit()
        conn.close()

    def get_history(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT id, datetime, speed, accuracy, chars_typed, duration FROM history ORDER BY id DESC')
        rows = c.fetchall()
        conn.close()
        return rows

    def add_recent_book(self, path, title):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('''INSERT OR REPLACE INTO recent_books (path, title, last_opened, favorite)
                     VALUES (?, ?, ?, COALESCE((SELECT favorite FROM recent_books WHERE path=?), 0))''',
                  (path, title, now, path))
        conn.commit()
        conn.close()

    def get_recent_books(self, only_favorites=False):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        if only_favorites:
            c.execute('SELECT path, title, last_opened, favorite FROM recent_books WHERE favorite=1 ORDER BY last_opened DESC')
        else:
            c.execute('SELECT path, title, last_opened, favorite FROM recent_books ORDER BY last_opened DESC')
        rows = c.fetchall()
        conn.close()
        return rows

    def set_favorite(self, path, favorite=True):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE recent_books SET favorite=? WHERE path=?', (1 if favorite else 0, path))
        conn.commit()
        conn.close() 