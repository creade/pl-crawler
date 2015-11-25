from flask import Blueprint, request
from database import db
from models import Job, Site_Url
from flask import jsonify
from rq import Queue
from rq.job import Job as Reddis_Job
from worker import conn

blueprint = Blueprint("jobs", __name__)
q = Queue(connection=conn)

@blueprint.route("/")
def ping():
    return "PING", 200

@blueprint.route("/jobs", methods=['POST'])
def add_job():
    site_urls = []

    for url in request.get_json():
        site_urls.append(Site_Url(url))

    job = Job(site_urls)

    db.session.add(job)
    db.session.commit()

    for url in job.site_urls:
        reddis_job = q.enqueue_call(
            func="crawler.crawl", args=[url.id, True, job.id], result_ttl=5000
        )

    return jsonify({"job_id" : job.id}), 202
