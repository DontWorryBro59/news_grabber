# В этом файлике я тестирую скрипты
# delete_null() - удаляем пустые строки из БД
# red_title() - редактируем заголовки
# red_modified_new() - редактируем новость
# red_img_autor_new() - редактируем автора фотографии
# add_flag() - добавляем флаг в БД о том что новость отредактирована
# start_redacting_news() - управляющая функция

import sqlite3


def delete_null():
    print("[MESSAGE] Удаление пустых строк в БД")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT url FROM news WHERE title is NULL or modified_new is NULL""")
    to_del = cursor.fetchall()
    if to_del != []:
        for el in to_del:
            url = el[0]
            cursor.execute(f"""DELETE FROM news WHERE url = '{url}'""")
            conn.commit()
    conn.commit()
    cursor.close()
    conn.close()


def red_title():
    print("[MESSAGE] Редактирование заголовков")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url, title FROM news WHERE flag_redact is NULL")
    to_red = cursor.fetchall()
    if to_red != []:
        for el in to_red:
            url = el[0]
            title = el[1]
            title = title.replace('*', '')
            title = title.replace('"', '')
            if "\n" in title:
                title = title.split('\n')
                title = title[2]
            title = f'<b>{title}</b>'
            cursor.execute(f"""
            UPDATE news SET title = '{title}' WHERE url = '{url}'
            """)
            conn.commit()
    conn.commit()
    cursor.close()
    conn.close()


def red_modified_new():
    print("[MESSAGE] Редактирование статей")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url, modified_new FROM news WHERE flag_redact is NULL")
    to_red = cursor.fetchall()
    if to_red != []:
        for el in to_red:
            url = el[0]
            text = el[1]
            if '#' in text:
                text = text.split('\n')
                del text[0]
                del text[0]
                text = '\n'.join(text)
                text = text.replace('**', ' ')
            try:
                if text[0] == '"' and text[len(text)-1] == '"':
                    text = text[1:len(text)-1]
            except:
                pass
            cursor.execute(f"""
            UPDATE news SET modified_new = '{text}' WHERE url = '{url}'
            """)
            conn.commit()
    conn.commit()
    cursor.close()
    conn.close()


def red_img_autor_new():
    print("[MESSAGE] Редактирование авторов фотографий")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url, img_autor FROM news WHERE flag_redact is NULL")
    to_red = cursor.fetchall()
    if to_red != []:
        for el in to_red:
            url = el[0]
            img_autor = el[1]
            if img_autor[0] != '(':
                img_autor = '('+img_autor+')'
            img_autor = '<em>'+img_autor+'</em>'
            cursor.execute(f"""
            UPDATE news SET img_autor = '{img_autor}' WHERE url = '{url}'
            """)
            conn.commit()
    conn.commit()
    cursor.close()
    conn.close()


def add_flag():
    print("[MESSAGE] Пометка о редактировании установлена")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM news WHERE flag_redact is NULL")
    to_red = cursor.fetchall()
    if to_red != []:
        for el in to_red:
            url = el[0]
            cursor.execute(f"""
            UPDATE news SET flag_redact = TRUE WHERE url = '{url}'
            """)
            conn.commit()
    conn.commit()
    cursor.close()
    conn.close()


def start_redacting_news():
    print("[MESSAGE] ############ Редактирование данных запущено ############")
    delete_null()
    red_title()
    red_modified_new()
    red_img_autor_new()
    add_flag()
    print("[MESSAGE] ############ Редактирование данных завершено ############")