from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Job



@app.route("/")
def ping():
    return "PING", 200

if __name__ == "__main__":
    app.run()
