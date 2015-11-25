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

def to_absoulte_urls(url_being_crawled, urls):
    return list(map(lambda url_to_check: ensure_absoluteness(url_to_check, url_being_crawled), urls))

def crawl(url_id, recurse, job_id):
    url_to_crawl = db.session.query(Site_Url).filter_by(id=url_id).first()
    site_text = requests.get(url_to_crawl.url).text
    urls_to_crawl_next = []
    img_urls = []
    if recurse:
        # fetch links
        urls_to_crawl_next = to_absoulte_urls(url_to_crawl.url, extract_site_urls(site_text))
        # enqueue links as non recursed

        for url_to_crawl_next in urls_to_crawl_next:
            new_url_to_crawl = Site_Url(url = url_to_crawl_next, job_id = job_id)
            db.session.add(new_url_to_crawl)
            db.session.commit()

            reddis_job = q.enqueue_call(
                func=crawl, args=(new_url_to_crawl.id,False,job_id), result_ttl=5000
            )

    # fetch img
    img_urls = to_absoulte_urls(url_to_crawl.url, extract_img_urls(site_text))

    # add images to job
    current_job = db.session.query(Job).filter_by(id=job_id).first()

    current_job.img_urls.extend(list(map(lambda img_url: Img_Url(img_url), img_urls)))
    db.session.add(current_job)
    db.session.commit()
