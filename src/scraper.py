import json
from typing import List, Tuple, Dict, Optional
import csv
import requests as req
from bs4 import BeautifulSoup as bs


class Scraper:
    def __init__(self, file_path: str, headers: Dict):
        self._file_path = file_path
        self._country_codes_and_asins = self._get_country_code_and_asin()
        self._urls_to_scrap = ["https://www.amazon.{}/dp/{}".format(ccode, asin) for ccode, asin in
                               self._country_codes_and_asins]
        self._headers = headers
        self._products_info = []

    def dump_json(self) -> None:
        data = {
            "products_info": self._products_info
        }
        with open('../products_detail.json', 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def url_parser(self) -> None:
        for url in self._urls_to_scrap:
            response = req.get(url, headers=self._headers)
            if self._is_status_equals_404_error(response.status_code):
                print(url, " not available")
                continue
            response_soup = bs(response.text, "html.parser")

            self._products_info.append(self._scrap_product_info(url, response_soup))

    def _scrap_product_info(self, url: str, response_soup: bs) -> Dict:
        if self._is_product_category_equals_perfume_cosmetic(response_soup):
            prod_info = self._scrap_prod_info_for_perfume_cosmetics(response_soup)
            return prod_info
        dic = {}
        product_title = self._get_product_title(response_soup)
        product_image_url = self._get_product_image_url(response_soup)
        product_price = self._get_product_price(url, response_soup)
        product_detail = self._get_product_detail(response_soup)

        dic["title"] = product_title
        dic["image_url"] = product_image_url
        dic["price"] = product_price
        dic["detail"] = product_detail

        print(url)

        return dic

    def _scrap_prod_info_for_perfume_cosmetics(self, response_soup: bs) -> Dict:
        dic = {}
        product_title = self._get_product_title(response_soup)
        product_image_url = self._get_img_url_for_perfume_cosmetics(response_soup)
        product_price = self._get_price_for_perfume_cosmetics(response_soup)
        product_detail = self._get_details_for_perfume_cosmetics(response_soup)

        dic["title"] = product_title
        dic["image_url"] = product_image_url
        dic["price"] = product_price
        dic["detail"] = product_detail

        return dic

    @staticmethod
    def _get_details_for_perfume_cosmetics(response_soup: bs) -> Dict:
        dic = {}
        r_set = response_soup.find("table", {"class": "a-normal a-spacing-micro"}).findAll("tr")
        for i in r_set:
            key = i.find("td", {"class": "a-span3"}).text
            value = i.find("td", {"class": "a-span9"}).text
            dic[key] = value
        return dic

    @staticmethod
    def _get_price_for_perfume_cosmetics(response_soup: bs) -> str:
        return response_soup.find("span", {"class": "a-offscreen"}).text

    @staticmethod
    def _get_img_url_for_perfume_cosmetics(response_soup: bs) -> str:
        return response_soup.find("div", {"id": "imgTagWrapperId"}).img.get("src")

    @staticmethod
    def _is_product_category_equals_perfume_cosmetic(response_soup: bs) -> bool:
        try:
            category = response_soup.find("span", {"id": "nav-search-label-id"}).text
            return category == "Perfume & Cosmetic"
        except AttributeError:
            return False

    def _get_product_price(self, url: str, response_soup: bs) -> Optional[str]:
        if ".de/" in url:
            return self._get_germany_price(response_soup)

        elif ".fr/" in url:
            return self._get_french_price(response_soup)

        elif ".es/" in url:
            return self._get_spanish_price(response_soup)

        elif ".it/" in url:
            return self._get_italian_price(response_soup)

    @staticmethod
    def _get_germany_price(response_soup: bs) -> Optional[str]:
        price = response_soup.find("div", {"id": "tmmSwatches"}).find("span",
                                                                      {"class": "a-color-base"}).text.strip()
        if len(price) == 1:
            return None
        elif "from" in price:
            new_price = price.split()
            return new_price[1]
        return price

    @staticmethod
    def _get_french_price(response_soup: bs) -> Optional[str]:
        txt = response_soup.find("div", {"id": "tmmSwatches"}).find("span",
                                                                    {"class": "a-color-base"}).text.strip()
        if len(txt) == 1:
            return None
        lst = txt.strip().split()
        return lst[-1] + lst[-2]

    @staticmethod
    def _get_spanish_price(response_soup: bs) -> Optional[str]:
        txt = response_soup.find("div", {"id": "tmmSwatches"}).find("span",
                                                                    {"class": "a-color-base"}).text.strip()
        if len(txt) == 1:
            return None
        lst = txt.strip().split()
        return lst[-1] + lst[-2]

    @staticmethod
    def _get_italian_price(response_soup: bs) -> Optional[str]:
        txt = response_soup.find("div", {"id": "tmmSwatches"}).find("span",
                                                                    {"class": "a-color-base"}).text.strip()
        if len(txt) == 1:
            return None
        lst = txt.strip().split()
        return lst[-1] + lst[-2]

    @staticmethod
    def _get_product_detail(response_soup: bs) -> Optional[Dict]:
        dic = {}
        txt = response_soup.find("ul", {"class": "a-unordered-list a-nostyle a-vertical a-spacing-none"
                                                 " detail-bullet-list"}).findAll("li")

        for raw_txt in txt:
            new_val = raw_txt.span.text.encode("ascii", "ignore")
            rem_newline = new_val.decode().replace("\n", "")
            rem_space = rem_newline.replace(" ", "")
            lst = rem_space.split(":")
            dic[lst[0]] = lst[1]

        return dic

    @staticmethod
    def _get_product_image_url(response_soup: bs) -> str:
        return response_soup.find("div", {"id": "img-canvas"}).img.get("src")

    @staticmethod
    def _get_product_title(response_soup: bs) -> str:
        return response_soup.find("span", {"id": "productTitle"}).text.strip()

    @staticmethod
    def _is_status_equals_404_error(status_code: int) -> bool:
        return status_code == 404

    def _get_country_code_and_asin(self) -> List[Tuple]:
        res = []
        with open(self._file_path, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                res.append((row[3], row[2]))
        return res
