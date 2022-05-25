from src.scraper import Scraper
import os

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'amazon_scraping_sheet1.csv')
    headers = {
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
    scraper = Scraper(file_path, headers)
    scraper.url_parser()
    scraper.dump_json()
