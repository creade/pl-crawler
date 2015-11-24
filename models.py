from app import db

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    site_urls = db.relationship("Site_Url", backref="job")
    img_urls = db.relationship("Img_Url", backref="job")

    def __init__(self, site_urls):
        self.site_urls = site_urls

class Site_Url(db.Model):
    __tablename__ = 'site_urls'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    url = db.Column(db.String(2083), unique=False, nullable=False)

    def __init__(self, url):
        self.url = url


class Img_Url(db.Model):
    __tablename__ = 'img_urls'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    url = db.Column(db.String(2083), unique=False, nullable=False)

    def __init__(self, url):
        self.url = url
