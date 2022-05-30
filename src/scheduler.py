import os
import json
from config import log
from threading import Thread
from time import sleep
from queue import Queue

from downloader import Downloader
from webdav import Webdav
from config import FETCH_VIDEOS_INTERVAL_SECONDS, VIDEOS_URL


class Scheduler:
    def __init__(self):
        self.webdav = Webdav()
        self.downloader = Downloader()
        self.videos = Queue()
        thread = Thread(
            target=self.run,
            args=(self.videos,),
            daemon=True,
        )
        thread.start()

    def run(self, known_videos_queue):
        while True:
            log.info("Loading saved video list...")
            known_videos = self.webdav.get_uploaded_files()
            log.info("Requesting video list...")
            videos = self.downloader.get_video_list(VIDEOS_URL)
            log.info("Checking for new videos...")
            new_videos = [v for v in videos if f"{v['title']}.mp4" not in known_videos]
            if new_videos:
                log.info("Detected new videos")
                log.info(f"Queue videos for download:\n{new_videos}")
                self.downloader.queue_videos_for_download(new_videos)

            log.info(f"Sleeping for {FETCH_VIDEOS_INTERVAL_SECONDS} seconds")
            sleep(FETCH_VIDEOS_INTERVAL_SECONDS)
