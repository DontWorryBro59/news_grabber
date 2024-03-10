from datetime import date
import sqlite3


def clear_db():
    day_today = int(str(date.today()).split("-")[2])
    if day_today % 5 == 0:
        print('[MESSAGE] Запущен процесс чистки базы данных')
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(f"""DELETE FROM news WHERE date != '{date.today()}'""")
        conn.commit()
        cursor.close()
        conn.close()
        print('[MESSAGE] База данных очищена от старых записей')
