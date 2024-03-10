# Описание функций
# start_posting - главная функция связывающая bot.py
# get_data - извлекаем данные из БД
# extract_data - исполняющая функция
# prepere_the_info - подготовка новостей к нужному формату
# post - публикация новости в ТГ канал

import json
import telebot
import sqlite3
import time


# Читаем файл конфига
with open("config.json") as file:
    config = json.load(file)

bot = telebot.TeleBot(config['API_TOKEN'])
channal = config['CHANNAL_LOGIN']


def get_data():
    print('[MESSAGE] ############ Запущен скрипт для публикации записей в ТГ ############')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Выбираем все данные из БД, которые не были отправлены в ТГ
    cursor.execute("""SELECT url,modified_new,img,img_autor,title FROM news WHERE flag_post is NULL""")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def extract_data(data: list):
    count = 1
    for el in data:
        print(f'[MESSAGE] Публикация новости № {count}')
        post(el)
        count += 1
        #time.sleep(150)
        print(f'[MESSAGE] Новость успешно опубликована')


def post(data: list):
    url = data[0]
    text = data[1]
    img = data[2]
    text_autor = data[3]
    title = data[4]
    a_href = f'<a href="https://t.me/Info_R_F">Инфополе РФ</a>'
    try:
        text_to_send = f"{text_autor}\n\n{title}\n\n{text}\n\n{a_href}"
        bot.send_photo(channal, img, text_to_send, parse_mode="HTML")
    except:
        print(f'[ERROR] Ошибка публикации данных')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    UPDATE news SET flag_post = 'TRUE' WHERE url = '{url}'
    """)
    conn.commit()
    cursor.close()
    conn.close()


def start_posting():
    data = get_data()
    extract_data(data)
    print(f'[MESSAGE] Все новости успешно опубликованы')


