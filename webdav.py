import os
from webdav3.client import Client
from dotenv import load_dotenv
import time
import threading
import random
from queue import Queue

load_dotenv()

WEBDAV_HOSTNAME = "https://space.rocket-fruit.com/remote.php/dav/files/Julius"
WEBDAV_LOGIN = "Julius"
WEBDAV_DEVICE_PASSWORD = os.getenv("WEBDAV_DEVICE_PASSWORD")
WEBDAV_TIMEOUT = 3600
WEBDAV_ROOT_DIR = "Familie/Medien/Serien/ZDF Magazin Royale"


options = {
    "webdav_hostname": WEBDAV_HOSTNAME,
    "webdav_login": WEBDAV_LOGIN,
    "webdav_password": WEBDAV_DEVICE_PASSWORD,
    "webdav_timeout": WEBDAV_TIMEOUT,
}


class Webdav:
    def __init__(self):
        self._client = Client(options)
        self._queue = Queue()
        self._thread = threading.Thread(
            target=self.run, args=(self._queue,), daemon=True
        )
        self._thread.start()

    def upload(self, remote_file_name, local_file_path, callback=None):
        self._client.upload_sync(
            remote_path=WEBDAV_ROOT_DIR + "/" + remote_file_name,
            local_path=local_file_path,
            callback=callback,
            progress=self.progress,
        )

    def progress(current, total):
        print("Progress:", current / total)

    def schedule(self, remote_file_name, local_file_path, callback=None):
        data = {
            "remote_file_name": remote_file_name,
            "local_file_path": local_file_path,
            "callback": callback,
        }
        self._queue.put(data)
        print("Got new job -> Queue size: " + str(self._queue.qsize()))

    def run(self, queue):
        while True:
            data = queue.get()
            self.upload(**data)
            print(data)
            queue.task_done()
