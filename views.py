from flask import Blueprint, request, abort
from database import db
from models import Job, Domain
from flask import jsonify
from urllib.parse import urlparse
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
    domains = []

    for url in request.get_json():
        if urlparse(url).scheme not in ["", "mailto"]:
            domains.append(Domain(url))
        else:
            return jsonify({"error": "Invalid Url"}), 400

    job = Job(domains)

    db.session.add(job)
    db.session.commit()

    for url in job.domains:
        reddis_job = q.enqueue_call(
            func="crawler.crawl", args=[url.id, True, job.id], result_ttl=5000
        )

    return jsonify({"job_id" : job.id}), 202

@blueprint.route("/jobs/<int:job_id>/status")
def job_status(job_id):
    job = db.session.query(Job).filter_by(id=job_id).first()

    if not job:
        abort(404)

    return jsonify(job.get_status())

@blueprint.route("/jobs/<int:job_id>/")
def job_results(job_id):
    job = db.session.query(Job).filter_by(id=job_id).first()

    if not job:
        abort(404)

    return jsonify(job.get_results())
