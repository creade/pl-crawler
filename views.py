from flask import Blueprint, request
from database import db
from models import Job, Site_Url
from flask import jsonify

blueprint = Blueprint("jobs", __name__)

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

    return jsonify({"job_id" : job.id}), 202
