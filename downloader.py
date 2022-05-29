from dotenv import load_dotenv
from queue import Queue
from threading import Thread
import json
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
import os
from config import log, YDL_OPTS, SHOW_IDENTIFIER


class Downloader:
    def __init__(self):
        print("Downloader init")
        self._videos_to_download = Queue()
        thread = Thread(target=self.run, args=(self._videos_to_download,), daemon=True)
        thread.start()

    def get_video_list(self, url, opts={}):
        with YoutubeDL(opts) as ydl:
            ie = ydl.extract_info(url, download=False)
            videos = [
                {
                    "title": video["title"],
                    "url": video["webpage_url"],
                    "description": video["description"],
                }
                for video in ie["entries"]
                if SHOW_IDENTIFIER in video["title"]
            ]
            return videos

    def queue_videos_for_download(self, videos):
        self._videos_to_download.put(videos)

    def download_videos(self, videos, opts={}):
        with YoutubeDL(opts) as ydl:
            try:
                ydl.download([video["url"] for video in videos])
            except DownloadError as e:
                log.error(e)
            except FileNotFoundError as e:
                log.error(e)

    def run(self, videos_to_download_queue):
        while True:
            videos_to_download = videos_to_download_queue.get()
            print(videos_to_download)
            if len(videos_to_download) > 0:
                log.info(f"Downloading {videos_to_download}...")
                self.download_videos(videos_to_download, opts=YDL_OPTS)
            videos_to_download_queue.task_done()
