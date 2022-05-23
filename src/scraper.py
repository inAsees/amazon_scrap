from dataclasses import dataclass
import requests as req
from bs4 import BeautifulSoup as bs


@dataclass
class ProductInfo:
    product_title: str
    product_image_url: str
    product_price: str
    product_details: str
