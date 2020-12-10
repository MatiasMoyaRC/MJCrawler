# -*- coding: utf-8 -*-


class Scraper:

    def __init__(self):
        self.XPATH_PROD_DET_1 = '//div[@class="align-self-center"]//text()'  # Nombre y precio
        self.XPATH_PROD_DET_2 = '//div[@class="align-self-center"]/p/text()'  # Descripcion

    def create_dic(self, parsed, categoria, marca):
        try:
            nombre_precio = parsed.xpath(self.XPATH_PROD_DET_1)
            nombre = nombre_precio[1]
            nombre = nombre.replace('  ', '')

            precio = nombre_precio[3]

            descri = nombre_precio[5]
            descri = descri.replace('\n', '')
            descri = descri.replace('  ', '')

            categoria = str(categoria)
            categoria = categoria.split("n")[-1]
            categoria = categoria.replace('  ', '')
            categoria = categoria.replace("']", "")

            marca = marca.replace('  ', '')

            producto_dic = {
                "BrandName": marca,
                "ProductName": nombre,
                "ProductCategory": categoria,
                "Price": precio,
                "Description": descri
            }
            return producto_dic

        except ValueError as ve:
            print(ve)
