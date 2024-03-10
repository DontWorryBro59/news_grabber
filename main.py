from art import tprint
import time
from scrapy_rbk import scrapy_rbk_urls
from scrapy_lenta import scrapy_lenta_urls
from generation_text import retell_the_news
from redacting_news import start_redacting_news
from bot import start_posting
from clear_db import clear_db


def main():
    tprint("News Graber")
    flag = True
    while flag != False:
        scrapy_rbk_urls()
        scrapy_lenta_urls()
        retell_the_news()
        start_redacting_news()
        start_posting()
        clear_db()
        print("[TIMESLEEP] Запущен процесс ожидания")
        #time.sleep(800)


if __name__ == '__main__':
    main()
