import os
import json
from dotenv import load_dotenv
from threading import Thread
from time import sleep
from queue import Queue

from downloader import Downloader
from webdav import Webdav
from utils import log

load_dotenv()

VIDEOS_URL = os.getenv("VIDEOS_URL")
FETCH_VIDEOS_INTERVAL_SECONDS = int(os.getenv("FETCH_VIDEOS_INTERVAL_SECONDS"))
VIDEO_DB_PATH = os.getenv("VIDEO_DB_PATH")


class Scheduler:
    def __init__(self):
        self.webdav = Webdav()
        self.downloader = Downloader()
        self.videos = Queue()
        self.videos.put([])
        self.retrieve_saved_videos()
        thread = Thread(target=self.run, args=(self.videos,), daemon=True)
        thread.start()

    def retrieve_saved_videos(self):
        log(f"Loading saved video list from {VIDEO_DB_PATH}...")
        if os.path.exists(VIDEO_DB_PATH):
            with open(VIDEO_DB_PATH, "r") as file:
                self.videos.put(json.load(file))

    def save_videos(self, videos):
        with open(VIDEO_DB_PATH, "w") as file:
            json.dump(videos, file)

    def run(self, known_videos_queue):
        while True:
            log("Loading saved video list...")
            known_videos = known_videos_queue.get()
            log("Requesting video list...")
            videos = self.downloader.get_video_list(VIDEOS_URL)
            log("Checking for new videos...")
            new_videos = [v for v in videos if v not in known_videos]
            if new_videos:
                log("Detected new videos")
                print(f"Queue videos for download:\n{new_videos}")
                self.downloader.queue_videos_for_download(new_videos)
                print(f"Saving new videos to {VIDEO_DB_PATH}")
                self.save_videos(videos)
            known_videos_queue.put(videos)

            log(f"Sleeping for {FETCH_VIDEOS_INTERVAL_SECONDS} seconds")
            sleep(FETCH_VIDEOS_INTERVAL_SECONDS)
