import os
from pathlib import Path
from webdav3.client import Client
from webdav3.exceptions import LocalResourceNotFound, ResponseErrorCode
import time
import threading
import random
from queue import Queue
from config import (
    log,
    webdav_options,
    WEBDAV_ROOT_DIR,
    DOWNLOAD_FOLDER,
    WATCH_DOWNLOAD_FOLDER_SECONDS,
)


class Webdav:
    def __init__(self):
        self._client = Client(webdav_options)
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
        self.remove_already_uploaded_files_from_local_disk(uploaded_files)

        return uploaded_files

    def remove_already_uploaded_files_from_local_disk(self, uploaded_files):
        # Remove already uploaded files
        for p in Path(DOWNLOAD_FOLDER).glob(r"*.mp4"):
            if p.name in uploaded_files:
                os.remove(p.absolute())

    def delete_local_file(self, local_file_path, msg):
        # Remove file from local disk after it has been uploaded successfully
        return lambda: log.info(msg) and os.remove(local_file_path)

    def _watch_downloaded_files(self):
        log.info("Checking downloaded files")
        # Only .mp4 files without .temp: ^((?!.temp).)*\.mp4
        downloaded_files = [
            p.name
            for p in Path(DOWNLOAD_FOLDER).glob(r"*.mp4")
            if ".temp" not in p.name
        ]
        log.info("Checking Checking uploaded files")
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
            log.info("No changes detected")
            return

        log.info("Uploading new files:")
        for file in files_to_upload:
            log.info(f"\tUploading {file['local_file_path']}...")
            success_msg = f"Finished uploading {file['local_file_path']}"
            try:
                self._upload(
                    file["remote_file_name"],
                    file["local_file_path"],
                    callback=self.delete_local_file(
                        file["local_file_path"], success_msg
                    ),
                )
            except LocalResourceNotFound as e:
                log.error(e)
            except ResponseErrorCode as e:
                log.error(e)

    def _progress(current, total):
        log.info(f"Progress: {current / total}")

    def _run(self):
        while True:
            self._watch_downloaded_files()
            log.info(f"Sleeping for {WATCH_DOWNLOAD_FOLDER_SECONDS} seconds ...")
            time.sleep(WATCH_DOWNLOAD_FOLDER_SECONDS)
