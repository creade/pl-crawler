from database import (
    Column,
    Model,
    db,
    relationship,
)
class Job(Model):
    __tablename__ = 'jobs'

    id = Column(db.Integer, primary_key=True)
    domains = relationship("Domain", backref="job")

    def __init__(self, domains):
        self.domains = domains

    def get_status(self):
        return {
            "completed": len([u for u in self.domains if u.crawled]),
            "inprogress": len([u for u in self.domains if not u.crawled])
        }

    def get_results(self):
        result = {"id": self.id, "domains":{}}
        for domain in self.domains:
            images_for_site = [u.url for u in domain.images]
            result["domains"][domain.url] = images_for_site
        return result

class Domain(Model):
    __tablename__ = 'domains'

    id = Column(db.Integer, primary_key=True)
    job_id = Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    url = Column(db.String(2083), unique=False, nullable=False)
    images = relationship("Image", backref="domain")
    crawled = Column(db.Boolean, nullable=False)

    def __init__(self, url, job_id = None):
        self.url = url
        self.job_id = job_id
        self.crawled = False


class Image(Model):
    __tablename__ = 'images'

    id = Column(db.Integer, primary_key=True)
    domain_id = Column(db.Integer, db.ForeignKey('domains.id'), nullable=False)
    url = Column(db.String(2083), unique=False, nullable=False)

    def __init__(self, url, domain_id = None):
        self.url = url
        self.domain_id = domain_id
