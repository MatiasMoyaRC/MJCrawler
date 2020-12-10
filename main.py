# -*- coding: utf-8 -*-
import crawler
from datetime import datetime

HOME_URL = "https://mhwc.brytemap.com"


def run():
    timestamp = datetime.now().strftime("%H:%M:%S")
    print("{} - Iniciando crawl".format(timestamp))

    get_html = crawler.Crawler(HOME_URL)
    get_html.parse_home()

    timestamp = datetime.now().strftime("%H:%M:%S")
    print("{} - Terminado".format(timestamp))


if __name__ == '__main__':
    run()
