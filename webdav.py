import os
from pathlib import Path
from webdav3.client import Client
from dotenv import load_dotenv
import time
import threading
import random
from queue import Queue
from utils import log

load_dotenv()

WEBDAV_HOSTNAME = os.getenv("WEBDAV_HOSTNAME")
WEBDAV_LOGIN = os.getenv("WEBDAV_LOGIN")
WEBDAV_DEVICE_PASSWORD = os.getenv("WEBDAV_DEVICE_PASSWORD")
WEBDAV_TIMEOUT = int(os.getenv("WEBDAV_TIMEOUT"))
WEBDAV_ROOT_DIR = os.getenv("WEBDAV_ROOT_DIR")
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER")
WATCH_DOWNLOAD_FOLDER_SECONDS = int(os.getenv("WATCH_DOWNLOAD_FOLDER_SECONDS"))


options = {
    "webdav_hostname": WEBDAV_HOSTNAME,
    "webdav_login": WEBDAV_LOGIN,
    "webdav_password": WEBDAV_DEVICE_PASSWORD,
    "webdav_timeout": WEBDAV_TIMEOUT,
}


class Webdav:
    def __init__(self):
        self._client = Client(options)
        # self._queue = Queue()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _upload(self, remote_file_name, local_file_path, callback=None):
        self._client.upload_sync(
            remote_path=WEBDAV_ROOT_DIR + "/" + remote_file_name,
            local_path=local_file_path,
            callback=callback,
            progress=self._progress,
        )

    def get_uploaded_files(self):
        # Filter out parent folder with [1::]
        uploaded_files = self._client.list(WEBDAV_ROOT_DIR)[1::]
        return uploaded_files

    def success_fn(self, msg):
        return lambda: log(msg)

    def _watch_downloaded_files(self):
        log("Checking downloaded files")
        # Only .mp4 files without .temp: ^((?!.temp).)*\.mp4
        downloaded_files = [
            p.name
            for p in Path(DOWNLOAD_FOLDER).glob(r"*.mp4")
            if ".temp" not in p.name
        ]
        log("Checking Checking uploaded files")
        uploaded_files = self.get_uploaded_files()

        files_to_upload = [
            {
                "local_file_path": f"{DOWNLOAD_FOLDER}/{downloaded_file}",
                "remote_file_name": downloaded_file,
            }
            for downloaded_file in downloaded_files
            if downloaded_file not in uploaded_files
        ]
        if len(files_to_upload) == 0:
            log("No changes detected")
            return

        log("Uploading new files:")
        for file in files_to_upload:
            log(f"\tUploading {file['local_file_path']}...")
            success_msg = f"Finished uploading {file['local_file_path']}"
            self._upload(
                file["remote_file_name"],
                file["local_file_path"],
                callback=self.success_fn(success_msg),
            )

    def _progress(current, total):
        log(f"Progress: {current / total}")

    # def schedule(self, remote_file_name, local_file_path, callback=None):
    # data = {
    # "remote_file_name": remote_file_name,
    # "local_file_path": local_file_path,
    # "callback": callback,
    # }
    # self._queue.put(data)
    # print("Got new job -> Queue size: " + str(self._queue.qsize()))

    def _run(self):
        while True:
            self._watch_downloaded_files()
            # data = queue.get()
            # self._upload(**data)
            # print(data)
            # queue.task_done()
            log(f"Sleeping for {WATCH_DOWNLOAD_FOLDER_SECONDS} seconds ...")
            time.sleep(WATCH_DOWNLOAD_FOLDER_SECONDS)
