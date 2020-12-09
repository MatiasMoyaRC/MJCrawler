import crawler
# import scraper
# import saver
from datetime import datetime

HOME_URL = "https://mhwc.brytemap.com"


def test():
    timestamp = datetime.now().strftime("%H:%M:%S")
    print("{} - Iniciando crawl".format(timestamp))

    get_html = crawler.Crawler(HOME_URL)
    get_html.parse_home()

    timestamp = datetime.now().strftime("%H:%M:%S")
    print("{} - Terminado".format(timestamp))


def run():
    pass
    # timestamp = datetime.now().strftime("%H:%M:%S")
    # print("{} - Guardando la info".format(timestamp))
    #
    # save_in = saver.DataB("Productos_Planta.csv")
    # save_in.save_csv(precios_dic)
    # driver.quit()
    #
    # timestamp = datetime.now().strftime("%H:%M:%S")
    # print("{} - Todo OK".format(timestamp))


if __name__ == '__main__':
    test()
