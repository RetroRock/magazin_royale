import os
import pickle
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
from webdav import Webdav

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret_desktop.json"
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

webdav = None

app = Flask(__name__, template_folder="template")
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = os.getenv("APP_SECRET")


@app.route("/")
def index():
    remote_file_name = "video.mp4"
    local_file_name = "video.mp4"
    webdav.schedule(
        remote_file_name,
        local_file_name,
        lambda: print("Finished uploading " + local_file_name),
    )

    return render_template("index.html")


if __name__ == "__main__":
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    webdav = Webdav()
    app.run("localhost", 8080, debug=True)
