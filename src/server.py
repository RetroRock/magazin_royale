import os
import pickle
import json
from flask import Flask, render_template, request
import requests
from webdav import Webdav
from config import (
    APP_HOSTNAME,
    APP_PORT,
    APP_RUN_DEBUG,
    VIDEOS_URL,
    WEBDAV_SHARED_URL,
    log,
)


app = Flask(__name__, template_folder="../template")
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = os.getenv("APP_SECRET")


@app.route("/")
def index():
    uploaded_files = scheduler.webdav.get_uploaded_files()
    videos_to_upload = scheduler.webdav.watch_downloaded_files()
    return render_template(
        "index.html",
        uploaded_files=uploaded_files,
        videos_to_upload=videos_to_upload,
        webdav_shared_url=WEBDAV_SHARED_URL,
    )


@app.route("/upload_check", methods=["POST"])
def upload_check():
    return json.dumps(scheduler.webdav.watch_downloaded_files())


if __name__ == "__main__":
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    from scheduler import Scheduler

    scheduler = Scheduler()
    app.run(host=APP_HOSTNAME, debug=APP_RUN_DEBUG)
