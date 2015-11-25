from app import create_app, db
from models import Job, Site_Url, Img_Url
import json
from io import StringIO
import unittest
from crawler import extract_site_urls,ensure_absoluteness

class CrawlerTests(unittest.TestCase):

    def setUp(self):
        _app = create_app("config.TestConfig")
        ctx = _app.test_request_context()
        ctx.push()
        db.session.commit()
        db.drop_all()
        db.create_all()


    def test_should_extract_href_from_a_tag(self):
        site_text = '<a href="http://example.com">text</a>'
        site_urls = extract_site_urls(site_text)
        self.assertEqual(len(site_urls), 1)
        self.assertEqual(site_urls[0], "http://example.com")

    def test_should_extract_relative_hrefs_from_a_tag(self):
        site_text = '<a href="http://example.com">text</a>'
        site_urls = extract_site_urls(site_text)
        self.assertEqual(len(site_urls), 1)
        self.assertEqual(site_urls[0], "http://example.com")

    def test_should_extract_hrefs_from_a_tags(self):
        site_text = '<a href="http://example.com">text</a><a href="http://example2.com">text</a>'
        site_urls = extract_site_urls(site_text)
        self.assertEqual(len(site_urls), 2)

    def test_should_extract_src_from_img_tag(self):
        site_text = '<img src="http://example.com/1.png">'
        img_urls = extract_img_urls(site_text)
        self.assertEqual(len(img_urls), 1)
        self.assertEqual(img_urls[0], "http://example.com/1.png")

    def test_should_absoulteize_relative_urls(self):
        url = '1.png'
        site = "http://example.com"
        self.assertEqual(ensure_absoluteness(url, site), "http://example.com/1.png")

    def test_should_ignore_absoulte_urls(self):
        url = 'http://example.com/1.png'
        site = "http://example.com"
        self.assertEqual(ensure_absoluteness(url, site), "http://example.com/1.png")


class APITest(unittest.TestCase):

  def setUp(self):
    app = create_app("config.TestConfig")
    ctx = app.test_request_context()
    ctx.push()

    self.app = app.test_client()

    db.session.commit()
    db.drop_all()
    db.create_all()


  def test_should_have_ping_endpoint(self):
    response = self.app.get('/', content_type='html/text')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, b"PING")

  def test_should_accept_post_to_job(self):
    response = self.app.post('/jobs', content_type='application/json', data="[]")
    self.assertEqual(response.status_code, 202)
    self.assertEqual(json.loads(response.data.decode()), {"job_id": 1})

    fetched_job = db.session.query(Job).filter_by(id=1).first()
    self.assertEqual(fetched_job.id, 1)

  def test_should_accept_site_url_in_post_to_job(self):
    response = self.app.post('/jobs', content_type='application/json', data='["http://example.com"]')

    self.assertEqual(response.status_code, 202)
    self.assertEqual(json.loads(response.data.decode()), {"job_id": 1})

    fetched_job = db.session.query(Job).filter_by(id=1).first()
    self.assertEqual(fetched_job.site_urls[0].url, "http://example.com")

  def test_should_accept_site_urls_in_post_to_job(self):
    response = self.app.post('/jobs', content_type='application/json', data='["http://example.com", "http://example2.com"]')

    self.assertEqual(response.status_code, 202)
    self.assertEqual(json.loads(response.data.decode()), {"job_id": 1})

    fetched_job = db.session.query(Job).filter_by(id=1).first()
    self.assertEqual(fetched_job.site_urls[0].url, "http://example.com")
    self.assertEqual(fetched_job.site_urls[1].url, "http://example2.com")


class ModelTest(unittest.TestCase):

  def setUp(self):
    _app = create_app("config.TestConfig")
    ctx = _app.test_request_context()
    ctx.push()
    #
    # self.app = create_app("config.TestConfig")

    db.session.commit()
    db.drop_all()
    db.create_all()


  def test_job_should_have_job_id(self):
    job = Job([])
    db.session.add(job)
    db.session.commit()
    job_id = job.id
    fetched_job = db.session.query(Job).filter_by(id=job_id).first()
    self.assertEqual(fetched_job.id, job_id)

  def test_job_should_have_site_urls(self):
    first_site_url = Site_Url("http://example.com")
    job = Job([first_site_url])
    db.session.add(job)
    db.session.commit()

    fetched_job = db.session.query(Job).filter_by(id=job.id).first()

    self.assertEqual(len(fetched_job.site_urls), 1)

  def test_job_should_have_img_urls(self):
    first_img_url = Img_Url("http://example.com/1.png")
    job = Job([])
    job.img_urls.append(first_img_url)
    db.session.add(job)
    db.session.commit()

    fetched_job = db.session.query(Job).filter_by(id=job.id).first()

    self.assertEqual(len(fetched_job.img_urls), 1)


  def test_img_urls_should_have_backref_to_job(self):
    first_img_url = Img_Url("http://example.com/1.png")
    job = Job([])
    job.img_urls.append(first_img_url)
    db.session.add(job)
    db.session.commit()

    self.assertEqual(first_img_url.job_id, job.id)

  def test_site_urls_should_have_backref_to_job(self):
    first_site_url = Site_Url("http://example.com")
    job = Job([first_site_url])
    db.session.add(job)
    db.session.commit()

    self.assertEqual(first_site_url.job_id, job.id)




if __name__ == '__main__':
    unittest.main()
