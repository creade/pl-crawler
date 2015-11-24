from database import (
    Column,
    Model,
    db,
    relationship,
)
class Job(Model):
    __tablename__ = 'jobs'

    id = Column(db.Integer, primary_key=True)
    site_urls = relationship("Site_Url", backref="job")
    img_urls = relationship("Img_Url", backref="job")

    def __init__(self, site_urls):
        self.site_urls = site_urls

class Site_Url(Model):
    __tablename__ = 'site_urls'

    id = Column(db.Integer, primary_key=True)
    job_id = Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    url = Column(db.String(2083), unique=False, nullable=False)

    def __init__(self, url):
        self.url = url


class Img_Url(Model):
    __tablename__ = 'img_urls'

    id = Column(db.Integer, primary_key=True)
    job_id = Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    url = Column(db.String(2083), unique=False, nullable=False)

    def __init__(self, url):
        self.url = url
