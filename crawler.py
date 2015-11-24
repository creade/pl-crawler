import requests
from models import Site_Url, Img_Url
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin, urlparse

class Crawler():
    def extract_site_urls(site_text):
        site_urls = []
        only_a_tags = SoupStrainer("a")
        for link in BeautifulSoup(site_text, "html.parser", parse_only=only_a_tags):
            if link.has_attr('href'):
                site_urls.append(link["href"])
        return site_urls

    def extract_img_urls(site_text):
        img_urls = []
        only_img_tags = SoupStrainer("img")
        for img in BeautifulSoup(site_text, "html.parser", parse_only=only_img_tags):
            if img.has_attr('src'):
                img_urls.append(img["src"])
        return img_urls

    def ensure_absoluteness(url, site):
        parsed_url = urlparse(url)
        if parsed_url.netloc == '':
            return urljoin(site, url)
        else:
            return url
