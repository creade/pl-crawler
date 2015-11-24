from flask import Flask
import os
app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

@app.route("/")
def ping():
    return "PING", 200

if __name__ == "__main__":
    app.run()
