from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask import jsonify

import os
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Job, Site_Url

@app.route("/")
def ping():
    return "PING", 200

@app.route("/jobs", methods=['POST'])
def add_job():
    site_urls = []

    for url in request.get_json():
        site_urls.append(Site_Url(url))

    job = Job(site_urls)

    db.session.add(job)
    db.session.commit()

    return jsonify({"job_id" : job.id}), 202

if __name__ == "__main__":
    app.run()
