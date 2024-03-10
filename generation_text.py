# Описание функций:
# get_text - получение перефразированной статьи
# send_on_g4f - прослойка
# retell_the_news_news - генерация статей для сайта рбк (исполняющий)
# redact_text_news - редактор сгенерированных статей (удаление ненужных символов)
import g4f
from g4f.client import Client
import sqlite3


def get_text(text):
    client = Client()
    response = client.chat.completions.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": text}],
        provider=g4f.Provider.You,
        stream=False,
    )
    text_to_return = response.choices[0].message.content
    return text_to_return


def send_on_g4f(text='') -> str:
    if text == '':
        return '[ERROR]: Отправлен пустой запрос генерации статьи'
    else:
        answer = get_text(text)
    return answer


def retell_the_news():
    print('[MESSAGE] ############ Генерация статей запущена ############')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT url,text_new from news WHERE text_new is not NULL and modified_new is NULL
    """)
    resoult = cursor.fetchall()
    conn.close()
    count = 1
    for res in resoult:
        try:
            print(f'[MESSAGE] Генерация ответа, статья номер: {count}')
            text = res[1]
            url = res[0]
            modified_new = f'''Перефразируй новость своими словами, в новостном стиле, 
            длина ответа должна получиться не больше 600 символов: "{text}"'''
            modified_new = send_on_g4f(modified_new)
            print(f'[MESSAGE] Генерация заголовка статьи')
            title = f'''Придумай лаконичный заголовок к статье: {text}'''
            title = send_on_g4f(title)
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(f"""
            UPDATE news SET modified_new = '{modified_new}', title = '{title}' WHERE url = '{url}'
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print(f'[MESSAGE] Генерация ответа, выполнена успешно')
        except:
            print(f'[ERROR] Ошибка генерации статьи или заголовка номер {count}')
        count += 1
    print('[MESSAGE] Генерация статей для сайта РБК завершена')




