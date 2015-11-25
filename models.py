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

    def __init__(self, site_urls):
        self.site_urls = site_urls

    def get_status(self):
        return {
            "completed": len([u for u in self.site_urls if u.crawled]),
            "inprogress": len([u for u in self.site_urls if not u.crawled])
        }

class Site_Url(Model):
    __tablename__ = 'site_urls'

    id = Column(db.Integer, primary_key=True)
    job_id = Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    url = Column(db.String(2083), unique=False, nullable=False)
    img_urls = relationship("Img_Url", backref="site_url")
    crawled = Column(db.Boolean, nullable=False)

    def __init__(self, url, job_id = None):
        self.url = url
        self.job_id = job_id
        self.crawled = False


class Img_Url(Model):
    __tablename__ = 'img_urls'

    id = Column(db.Integer, primary_key=True)
    site_url_id = Column(db.Integer, db.ForeignKey('site_urls.id'), nullable=False)
    url = Column(db.String(2083), unique=False, nullable=False)

    def __init__(self, url, site_url_id = None):
        self.url = url
        self.site_url_id = site_url_id
