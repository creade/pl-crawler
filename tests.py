from app import create_app, db
from models import Job, Domain, Image
import json
from io import StringIO
import unittest
from crawler import extract_domains,ensure_absoluteness, extract_images

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
        domains = extract_domains(site_text)
        self.assertEqual(len(domains), 1)
        self.assertEqual(domains[0], "http://example.com")

    def test_should_extract_relative_hrefs_from_a_tag(self):
        site_text = '<a href="http://example.com">text</a>'
        domains = extract_domains(site_text)
        self.assertEqual(len(domains), 1)
        self.assertEqual(domains[0], "http://example.com")

    def test_should_extract_hrefs_from_a_tags(self):
        site_text = '<a href="http://example.com">text</a><a href="http://example2.com">text</a>'
        domains = extract_domains(site_text)
        self.assertEqual(len(domains), 2)

    def test_should_ignore_duplicate_links(self):
        site_text = '<a href="http://example2.com/index.html">text</a><a href="http://example2.com/index.html">text</a>'
        domains = extract_domains(site_text)
        self.assertEqual(len(domains), 1)

    def test_should_ignore_duplicate_links_that_are_page_anchors(self):
        site_text = '<a href="http://example2.com/index.html">text</a><a href="http://example2.com/index.html#anchor">text</a>'
        domains = extract_domains(site_text)
        self.assertEqual(len(domains), 1)

    def test_should_extract_src_from_img_tag(self):
        site_text = '<img src="http://example.com/1.png">'
        images = extract_images(site_text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], "http://example.com/1.png")

    def test_should_absoulteize_relative_urls(self):
        url = '1.png'
        site = "http://example.com"
        self.assertEqual(ensure_absoluteness(url, site), "http://example.com/1.png")

    def test_should_ignore_absoulte_urls(self):
        url = 'http://example.com/1.png'
        site = "http://example.com"
        self.assertEqual(ensure_absoluteness(url, site), "http://example.com/1.png")

    def test_should_handle_webm_link(self):
        site_text = '<a href="//upload.wikimedia.org/wikipedia/commons/4/4e/Plasma_globe_23s.webm" title="Play media" target="new"><span class="play-btn-large"><span class="mw-tmh-playtext">Play media</span></span></a>'
        images = extract_domains(site_text)
        self.assertEqual(len(images), 0)

    def test_should_not_follow_mailtos(self):
        site_text = '<a href="mailto:contact@postlight.com">contact@postlight.com</a>'
        images = extract_domains(site_text)
        self.assertEqual(len(images), 0)

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

  def test_should_accept_domain_in_post_to_job(self):
    response = self.app.post('/jobs', content_type='application/json', data='["http://example.com"]')

    self.assertEqual(response.status_code, 202)
    self.assertEqual(json.loads(response.data.decode()), {"job_id": 1})

    fetched_job = db.session.query(Job).filter_by(id=1).first()
    self.assertEqual(fetched_job.domains[0].url, "http://example.com")

  def test_should_reject_domain_without_protocol_in_post_to_job(self):
    response = self.app.post('/jobs', content_type='application/json', data='["example.com"]')

    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data.decode()), {"error": "Invalid Url"})

  def test_should_accept_domains_in_post_to_job(self):
    response = self.app.post('/jobs', content_type='application/json', data='["http://example.com", "http://example2.com"]')

    self.assertEqual(response.status_code, 202)
    self.assertEqual(json.loads(response.data.decode()), {"job_id": 1})

    fetched_job = db.session.query(Job).filter_by(id=1).first()
    self.assertEqual(fetched_job.domains[0].url, "http://example.com")
    self.assertEqual(fetched_job.domains[1].url, "http://example2.com")

  def test_should_expose_job_status(self):
    self.app.post('/jobs', content_type='application/json', data='["http://example.com", "http://example2.com"]')

    response = self.app.get('/jobs/1/status')
    status = json.loads(response.data.decode())
    self.assertEqual(status["inprogress"] + status["completed"], 2)

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

  def test_job_should_have_domains(self):
    first_domain = Domain("http://example.com")
    job = Job([first_domain])
    db.session.add(job)
    db.session.commit()

    fetched_job = db.session.query(Job).filter_by(id=job.id).first()

    self.assertEqual(len(fetched_job.domains), 1)

  def test_domain_should_have_images(self):
    first_domain = Domain("http://example.com")
    first_img_url = Image("http://example.com/1.png")
    first_domain.images.append(first_img_url)
    job = Job([first_domain])

    db.session.add(job)
    db.session.commit()

    fetched_job = db.session.query(Job).filter_by(id=job.id).first()

    self.assertEqual(len(fetched_job.domains[0].images), 1)


  def test_images_should_have_backref_to_domain(self):
    first_domain = Domain("http://example.com")
    first_img_url = Image("http://example.com/1.png")
    first_domain.images.append(first_img_url)
    job = Job([first_domain])

    db.session.add(job)
    db.session.commit()

    self.assertEqual(first_img_url.domain.id, first_domain.id)

  def test_domains_should_have_backref_to_job(self):
    first_domain = Domain("http://example.com")
    job = Job([first_domain])
    db.session.add(job)
    db.session.commit()

    self.assertEqual(first_domain.job.id, job.id)


  def test_job_should_emit_status_for_uncrawled_urls(self):
    first_domain = Domain("http://example.com")
    second_domain = Domain("http://example.com/2")
    job = Job([first_domain,second_domain])

    self.assertEqual(job.get_status()["inprogress"], 2)

  def test_job_should_emit_status_for_crawled_urls(self):
    first_domain = Domain("http://example.com")
    first_domain.crawled = True
    job = Job([first_domain])

    self.assertEqual(job.get_status()["completed"], 1)

  def test_job_should_emit_status_for_all_urls(self):
    first_domain = Domain("http://example.com")
    first_domain.crawled = True
    second_domain = Domain("http://example.com/2")
    job = Job([first_domain,second_domain])

    self.assertEqual(job.get_status()["completed"], 1)
    self.assertEqual(job.get_status()["inprogress"], 1)


  def test_job_should_emit_results_for_all_urls(self):
    first_domain = Domain("http://example.com")
    first_img_url = Image("http://example.com/1.png")
    second_img_url = Image("http://example.com/2.png")
    third_img_url = Image("http://example.com/3.png")

    first_domain.images.extend([first_img_url, second_img_url, third_img_url])

    second_domain = Domain("http://example.com/2")
    fourth_img_url = Image("http://example.com/4.png")
    second_domain.images.extend([fourth_img_url])

    job = Job([first_domain,second_domain])

    self.assertEqual(job.get_results(), {
        "id": job.id,
        "domains":{
            "http://example.com":[
                "http://example.com/1.png",
                "http://example.com/2.png",
                "http://example.com/3.png"
            ],
            "http://example.com/2":[
                "http://example.com/4.png"
            ]
        }
    })






if __name__ == '__main__':
    unittest.main()
