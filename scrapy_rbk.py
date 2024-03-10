# Описание функций:
# get_urls - Получение всех ссылок с новостями
# write_to_db_urls - Запись всех полученных ссылок в базу данных
# get_new_from_urls - Связная функция для получения новостей
# get_scrapy - Формирование text, img, autor_img
# add_date_in_base - Добавление ^^^^^^^^^^^^^^^^ в базу данных
# scrapy_rbk_urls - Главная функция, выполняющая все последовательности (исполняющий)
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import date


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 "
                  "Safari/537.36",
}


# Получаем ссылки
def get_urls():
    # Получаем список ссылок на новости
    print('[MESSAGE] Получаем ссылки на новости')
    url = "https://perm.rbc.ru/"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
    else:
        print('[ERROR] Ошибка получения данных со страницы')

    quotes = soup.find_all("a", class_="news-feed__item js-visited js-news-feed-item js-yandex-counter")
    print('[MESSAGE] Список ссылок получен')
    return quotes


def write_to_db_urls(quotes: list) -> None:
    # Записываем ссылки в БД
    count = 0
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    print(f'[MESSAGE] Соединение с БД открыто')
    for el in quotes:
        # Фильтры
        if 'www.rbc.ru' not in el.get('href'):
            continue
        if 'crypto' in el.get('href'):
            continue

        cursor.execute(f"SELECT * FROM news WHERE url = '{el.get('href')}'")
        if cursor.fetchone() == None:
            cursor.execute(f"INSERT INTO news(url,date) VALUES('{el.get('href')}','{date.today()}')")
            count += 1
            conn.commit()
    if count != 0:
        print(f'[MESSAGE] Количество добавленных ссылок на новости: {count}')
    else:
        print(f'[MESSAGE] Новых новостей не найдено:')
    cursor.close()
    conn.close()
    print(f'[MESSAGE] Соединение с БД закрыто')


def get_news_from_urls() -> None:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    print(f'[MESSAGE] Процесс получения новостей запущен')
    # Получаем все записи, где новости еще не получены
    cursor.execute("""
    SELECT url FROM news WHERE text_new is NULL
    """)
    count = 1
    resoult = []
    for el in cursor.fetchall():
        resoult.append(el[0])
    cursor.close()
    conn.close()
    for el in resoult:
        print(f'[MESSAGE] Извлекаем новость под номером {count}')
        new = scrapy_new(el)
        if type(new) == str:
            count += 1
            continue
        add_date_in_base(
            url=new[0],
            text=new[1],
            autor=new[2],
            photo=new[3]
        )
        print(f'[MESSAGE] Новость добавлена в БД')
        count += 1
    print('[MESSAGE] Все новости успешно добавлены в БД')


def scrapy_new(url: str) -> list:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")

    # Извлечение новости со странички
    try:
        text = soup.find('div', class_='article__text article__text_free').find_all('p')
    except:
        print('[ERROR] Не смог извлечь текст')
        print('[MESSAGE] Запись с пустыми полями удалена')
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM news WHERE url = '{url}'")
        conn.commit()
        cursor.close()
        conn.close()
        return '[ERROR] Не смог извлечь текст'

    text_new = []
    for el in text:
        text_new.append(el.text)
    text_new = " ".join(text_new)

    # print(text_new)
    # Извлекаем автора фотографии
    try:
        photo_autor = soup.find('div', class_='article__text article__text_free').find('span',
                                                                                       class_="article__main-image__author")
        photo_autor = photo_autor.text.replace('\\', ' ').strip()
    except:
        print('[ERROR] Не найден автор фотографии')
        print('[MESSAGE] Запись с пустыми полями удалена')
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM news WHERE url = '{url}'")
        conn.commit()
        cursor.close()
        conn.close()
        return '[ERROR] Не найден автор фотографии'

    # Извлекаем ссылку на картинку:
    try:
        photo_url = soup.find('div', class_='article__text article__text_free').find('img', class_="smart-image__img")
        photo_url = photo_url.get('src')
    except:
        print('[ERROR] Фотография не найдена')
        print('[MESSAGE] Запись с пустыми полями удалена')
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM news WHERE url = '{url}'")
        conn.commit()
        cursor.close()
        conn.close()
        return '[ERROR] Фотография не найдена'

    # Для получения изображения в виде бинарного кода:
    # url_photo = requests.get(url_photo.get('src'))
    # В результате выполнения функции получаем: text_new, photo_autor, photo_url
    resoult = [url, text_new, photo_autor, photo_url]
    return resoult


def add_date_in_base(url: str, text: str, autor: str, photo: str):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f"""
        UPDATE news SET text_new = '{text}', img = '{photo}', img_autor = '{autor}' WHERE url = '{url}';    
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print('[MESSAGE] Данные успешно обновлены в БД')
    except:
        print('[ERROR] Ошибка добавления данных')



def scrapy_rbk_urls():
    print('[MESSAGE] ############ Копирование новостей с сайта РБК.ру запущено ############')
    write_to_db_urls(get_urls())
    get_news_from_urls()
