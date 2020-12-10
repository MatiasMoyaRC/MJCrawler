# -*- coding: utf-8 -*-
import csv
import os


class DataB:

    def __init__(self):
        self.__file_name = "PruebaMJCrawler.csv"

    def save_csv(self, producto_dic):
        with open('{}'.format(self.__file_name), 'a+', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=producto_dic.keys())

            if os.stat(self.__file_name).st_size == 0:
                writer.writeheader()

            writer.writerow(producto_dic)
