from dataclasses import dataclass
from typing import List, Tuple
import csv

import requests as req
from bs4 import BeautifulSoup as bs


@dataclass
class ProductInfo:
    product_title: str
    product_image_url: str
    product_price: str
    product_details: str


class Scraper:
    def __init__(self):
        self._country_codes_and_asins = self._get_country_code_and_asin()

    def _get_country_code_and_asin(self) -> List[Tuple]:
        res = []
        with open(r"C:\Users\DELL\Desktop\Credicxo\Amazon Scraping - Sheet1.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                res.append((row[3], row[2]))
        return res


if __name__ == "__main__":
