from dataclasses import dataclass
from typing import List, Tuple, Dict
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
        self._urls_to_scrap = ["https://www.amazon.{}/dp/{}".format(ccode, asin) for ccode, asin in
                               self._country_codes_and_asins]
        self._headers = {
            'cookie': 'session-id=258-3723382-3489961; i18n-prefs=EUR; lc-acbde=en_GB; sp-cdn="L5Z9:IN"; '
                      'ubid-acbde=259-4780058-9673219; session-token="UdJ+3NvMuV2KSFtdn+uiKR1/EPEBmI7h606fWB6fn3xUGbuq'
                      'fhkxO5KjFeD9CgFpprhbJoyTBf89mwZf8Kq6HjA1gvnLMKrxuHyLN4pXD9neWvKGc7/uULzI87zCpqT//RtnrCF00JTaAXc'
                      'cxiksrzPXCCc02XaFNEOycrDKjDN2NR6vgePKxPMibGD+So7JjR233qRqXZCGBYsZ1Ua6BA=="; csm-hit=tb:WW50E5C0R'
                      'WP61M11AQ8Q+s-WW50E5C0RWP61M11AQ8Q|1653399106140&t:1653399106140&adb:adblk_no;'
                      ' session-id-time=2082754801l; i18n-prefs=EUR; session-id=257-9403444-2905827; '
                      'session-id-time=2082787201l; session-token="jX13VNnq9rnnG/b2cTz5sHMU3pftTGxQYB5J0xfA8aqJMEc/'
                      'Yc579O0glsPU0MDipLVJnKQS6s/I6Srs9gQAYFyGx8/5yL7GfGZGxLqFJzQoo/tL4qtYIZdvw1x/urcK9WfGKVVC8U44nnSn'
                      '/Fh4JeKJJkj/qv84QE2DwrahkUMq6vaO81n+tEUvsoobD5/0yAJmSqdKZbyLO7/kP8KvAw=="; sp-cdn="L5Z9:IN"; '
                      'ubid-acbde=257-5191887-3697469',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/101.0.4951.67 Safari/537.36',
            'viewport-width': '1229'
        }

    def url_parser(self):
        for url in self._urls_to_scrap[:100]:
            response = req.get(url, headers=self._headers)
            if self._is_status_equals_404_error(response.status_code):
                print(url, " not available")
                continue
            response_soup = bs(response.text, "html.parser")
            self._scrap_product_info(response_soup)

    def _scrap_product_info(self, response_soup: bs) -> Dict:
        product_title = self._get_product_title(response_soup)
        product_image_url = self._get_product_image_url(response_soup)

    @staticmethod
    def _get_product_image_url(response_soup: bs) -> str:
        try:
            return response_soup.find("div", {"id": "img-canvas"}).img.get("src")
        except AttributeError:
            pass

    @staticmethod
    def _get_product_title(response_soup: bs) -> str:
        return response_soup.find("span", {"id": "productTitle"}).text.strip()

    @staticmethod
    def _is_status_equals_404_error(status_code: int) -> bool:
        return status_code == 404

    @staticmethod
    def _get_country_code_and_asin() -> List[Tuple]:
        res = []
        with open(r"C:\Users\DELL\Desktop\Credicxo\amazon_scraping_sheet1.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                res.append((row[3], row[2]))
        return res
