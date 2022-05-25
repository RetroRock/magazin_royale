import os
import json
from dotenv import load_dotenv
from threading import Thread
from time import sleep
from queue import Queue

from downloader import Downloader
from webdav import Webdav

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
        thread = Thread(target=self.run, args=(self.videos,))
        thread.start()

    def retrieve_saved_videos(self):
        if os.path.exists(VIDEO_DB_PATH):
            with open(VIDEO_DB_PATH, "r") as file:
                self.videos.put(json.load(file))

    def save_videos(self, videos):
        with open(VIDEO_DB_PATH, "w") as file:
            json.dump(videos, file)

    def run(self, known_videos_queue):
        while True:
            known_videos = known_videos_queue.get()
            print("Request video list")
            videos = self.downloader.get_video_list(VIDEOS_URL)
            print("Checking for new videos")
            new_videos = [v for v in videos if v not in known_videos]
            if new_videos:
                print("Queue videos for download")
                self.downloader.queue_videos_for_download(new_videos)
                print("Saving new videos to json file")
                self.save_videos(videos)
            known_videos_queue.put(videos)

            sleep(FETCH_VIDEOS_INTERVAL_SECONDS)
