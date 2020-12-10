# -*- coding: utf-8 -*-
import requests
import lxml.html as html
from datetime import datetime
import scraper
import saver

XPATH_CATEGORIAS = '//div[@class="dropdown category-dropdown"]/a/@href'   # href de categorias
XPATH_PRODUCT_DETAILS = '//div[@class="card-footer"]/a/@href'  # href del product details


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
                dictionary = obj.create_dic(parsed, categ, marca)

                obj = saver.DataB()
                obj.save_csv(dictionary)
                timestamp = datetime.now().strftime("%H:%M:%S")
                print("{} - Product saved".format(timestamp))
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
