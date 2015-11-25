import requests
from models import Site_Url, Img_Url, Job
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin, urlparse
from database import db
from rq import Queue
from rq.job import Job as Reddis_Job
from worker import conn

q = Queue(connection=conn)

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

def crawl(url_to_crawl, recurse, job_id):
    site_text = requests.get(url_to_crawl).text
    urls_to_crawl_next = []
    img_urls = []
    if recurse:
        # fetch links
        urls_to_crawl_next = list(map(lambda url_to_check: Site_Url(ensure_absoluteness(url_to_check, url_to_crawl)), extract_site_urls(site_text)))
        # enqueue links as non recursed
        for url_to_crawl_next in urls_to_crawl_next:
            reddis_job = q.enqueue_call(
                func=crawl, args=(url_to_crawl_next.url,False,job_id), result_ttl=5000
            )
        print(urls_to_crawl_next)
    # fetch img
    img_urls = list(map(lambda url_to_check: Img_Url(ensure_absoluteness(url_to_check, url_to_crawl)), extract_img_urls(site_text)))

    # add images to job
    current_job = db.session.query(Job).filter_by(id=job_id).first()

    current_job.site_urls.extend(urls_to_crawl_next)
    current_job.img_urls.extend(img_urls)
    db.session.add(current_job)
    db.session.commit()
