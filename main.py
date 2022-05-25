from src.scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    scraper.url_parser()
    scraper.dump_json()
