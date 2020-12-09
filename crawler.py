import requests
# from bs4 import BeautifulSoup
import lxml.html as html
# import os
# import time
import scraper
import saver

XPATH_CATEGORIAS = '//div[@class="dropdown category-dropdown"]/a/@href'   # href de categorias

XPATH_MARCAS = '//div[@class="dropdown category-dropdown"]/div[@arialabelledby="idcatedoria"]/a/@href'  # href de marcas
XPATH_MARCAS_NAME = '//div[@class="dropdown category-dropdown"]/div[@arialabelledby="idcatedoria"]/a/text()'
# nombres de marcas

XPATH_PRODUCT_DETAILS = '//div[@class="card-footer"]/a/@href'  # href del product details


# en url del product details
XPATH_PROD_DET_1 = '//div[@class="align-self-center"]/h5/text()'  # Nombre y precio
XPATH_PROD_DET_2 = '//div[@class="align-self-center"]/p/text()'   # Descripcion


class Crawler:

    def __init__(self, url):
        self.home_url = url

    def parse_details(self, link, categ, marca):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                page = response.content
                # page = response.content.decode('cp1252')
                parsed = html.fromstring(page)

                obj = scraper.Scraper()
                dictionary = obj.crear_dic(parsed, categ, marca)

                obj = saver.DataB()
                obj.save_csv(dictionary)

            else:
                raise ValueError('Error {}'.format(response.status_code))

        except ValueError as ve:
            print(ve)

    def parse_marca(self, link, categ):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                page = response.content
                # page = response.content.decode('cp1252')
                parsed = html.fromstring(page)
                idmarca = link.split('=')[-1]
                marca_get = parsed.xpath('//div/a[@href="/public/category.php?category_id={}"]/text()'.format(idmarca))
                marca = marca_get[0]
                if len(marca) < 2:
                    marca = "-"

                productos = parsed.xpath(XPATH_PRODUCT_DETAILS)

                for link in productos:
                    home = self.home_url
                    link_send = home + link
                    Crawler.parse_details(self, link_send, categ, marca)

            else:
                raise ValueError('Error {}'.format(response.status_code))
        except ValueError as ve:
            print(ve)

    def parse_categoria(self, link):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                page = response.content
                # page = response.content.decode('cp1252')
                parsed = html.fromstring(page)
                idcat = link.split('=')[-1]
                categoria = parsed.xpath('//div/a[@id="{}"]/text()'.format(idcat))
                xpath_marcas2 = '//div/div[@arialabelledby="{}"]/a/@href'.format(idcat)
                print(xpath_marcas2)
                marcas = parsed.xpath(xpath_marcas2)
                if len(marcas) != 0:
                    for link2 in marcas:
                        home = self.home_url
                        link_send = home + link2
                        Crawler.parse_marca(self, link_send, categoria)
                else:
                    Crawler.parse_marca(self, link, categoria)
            else:
                raise ValueError('Error {}'.format(response.status_code))
        except ValueError as ve:
            print(ve)

    def parse_home(self):
        try:
            response = requests.get(self.home_url)
            if response.status_code == 200:
                home = response.content
                # home = response.content.decode('cp1252')
                parsed = html.fromstring(home)
                categorias = parsed.xpath(XPATH_CATEGORIAS)

                for link in categorias:
                    home = self.home_url
                    link_send = home + link
                    Crawler.parse_categoria(self, link_send)

            else:
                raise ValueError('Error {}'.format(response.status_code))
        except ValueError as ve:
            print(ve)

    # def __init__(self):
    #     self.browser =
    #     self.head = head

    # def create_driver(self):
    #     options = Options()
    #     options.headless = self.head
    #
    #     if self.browser == "chrome":
    #         # options = Options()
    #         # options.headless = self.head
    #         driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
    #     else:
    #         driver = webdriver.Firefox(executable_path="geckodriver.exe")
    #     driver.maximize_window()
    #
    #     return driver
    #
    # def crawl(self, drive, url):
    #     drive.get(url)
    #     time.sleep(5)
