import requests
from models import Domain, Image, Job
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin, urlparse, urldefrag
from database import db
from rq import Queue
from rq.job import Job as Reddis_Job
from worker import conn

q = Queue(connection=conn)

def extract_domains(site_text):
    domains = set()
    only_a_tags = SoupStrainer("a")
    for link in BeautifulSoup(site_text, "html.parser", parse_only=only_a_tags):
        if link.has_attr('href') and urlparse(link["href"]).scheme not in ["", "mailto"]:
            domains.add(urldefrag(link["href"])[0])
    return list(domains)

def extract_images(site_text):
    images = set()
    only_img_tags = SoupStrainer("img")
    for image in BeautifulSoup(site_text, "html.parser", parse_only=only_img_tags):
        if image.has_attr('src'):
            images.add(image["src"])
    return list(images)

def ensure_absoluteness(url, domain):
    parsed_url = urlparse(url)
    if parsed_url.netloc == '':
        return urljoin(domain, url)
    else:
        return url

def to_absoulte_urls(url_being_crawled, urls):
    return list(map(lambda url_to_check: ensure_absoluteness(url_to_check, url_being_crawled), urls))

def crawl(url_id, recurse, job_id):
    url_to_crawl = db.session.query(Domain).filter_by(id=url_id).first()
    site_text = requests.get(url_to_crawl.url).text
    urls_to_crawl_next = []
    images = []
    if recurse:
        # fetch links
        urls_to_crawl_next = to_absoulte_urls(url_to_crawl.url, extract_domains(site_text))

        # enqueue links as non recursed
        for url_to_crawl_next in urls_to_crawl_next:
            new_url_to_crawl = Domain(url = url_to_crawl_next, job_id = job_id)
            db.session.add(new_url_to_crawl)
            db.session.commit()

            reddis_job = q.enqueue_call(
                func=crawl, args=(new_url_to_crawl.id,False,job_id), result_ttl=5000
            )

    # fetch images
    images = to_absoulte_urls(url_to_crawl.url, extract_images(site_text))

    # add images to domain
    url_to_crawl.images.extend(list(map(lambda image: Image(url = image, domain_id = url_id), images)))
    url_to_crawl.crawled = True

    db.session.add(url_to_crawl)
    db.session.commit()
