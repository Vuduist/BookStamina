from modules.ui import run_app
import sys
import sqlite3

def clear_all():
    # Очищаем таблицы в appdata.db
    conn = sqlite3.connect('appdata.db')
    c = conn.cursor()
    c.execute('DELETE FROM history')
    c.execute('DELETE FROM recent_books')
    conn.commit()
    conn.close()
    # Очищаем таблицу в progress.db
    conn = sqlite3.connect('progress.db')
    c = conn.cursor()
    c.execute('DELETE FROM progress')
    conn.commit()
    conn.close()
    print('Все данные приложения успешно очищены.')

if __name__ == "__main__":
    if '--clear' in sys.argv:
        clear_all()
    else:
        run_app() 