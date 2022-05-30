from os import getenv
import logging

WEBDAV_TIMEOUT = int(getenv("WEBDAV_TIMEOUT")) or 3600
DOWNLOAD_FOLDER = getenv("DOWNLOAD_FOLDER") or "webdav"
FETCH_VIDEOS_INTERVAL_SECONDS = int(getenv("FETCH_VIDEOS_INTERVAL_SECONDS")) or 3600
WATCH_DOWNLOAD_FOLDER_SECONDS = int(getenv("WATCH_DOWNLOAD_FOLDER_SECONDS")) or 600
VIDEOS_URL = getenv("VIDEOS_URL") or "https://www.zdf.de/comedy/zdf-magazin-royale"
SHOW_IDENTIFIER = getenv("SHOW_IDENTIFIER") or "ZDF Magazin Royale vom"
APP_HOSTNAME = "0.0.0.0"
# APP_PORT = int(getenv("APP_PORT")) or 8080
APP_PORT = 8080
APP_RUN_DEBUG = bool(getenv("APP_RUN_DEBUG")) or False

WEBDAV_HOSTNAME = getenv("WEBDAV_HOSTNAME")
WEBDAV_LOGIN = getenv("WEBDAV_LOGIN")
WEBDAV_DEVICE_PASSWORD = getenv("WEBDAV_DEVICE_PASSWORD")
WEBDAV_ROOT_DIR = getenv("WEBDAV_ROOT_DIR")
WEBDAV_SHARED_URL = getenv("WEBDAV_SHARED_URL")


webdav_options = {
    "webdav_hostname": WEBDAV_HOSTNAME,
    "webdav_login": WEBDAV_LOGIN,
    "webdav_password": WEBDAV_DEVICE_PASSWORD,
    "webdav_timeout": WEBDAV_TIMEOUT,
}

YDL_OPTS = {"outtmpl": "webdav/%(title)s.%(ext)s", "quiet": "true"}

logging.basicConfig(
    # filename="magazin_royale.log",
    format="%(asctime)s %(message)s",
    # encoding="utf-8",
    level=logging.INFO,
)
log = logging.getLogger(__name__)
