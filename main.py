import os
import json
import youtube_dl
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
SERVICE_ACCOUNT_FILE = "./service.json"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")

urls = ["https://www.zdf.de/comedy/zdf-magazin-royale"]
ydl_opts = {}


def download_videos(urls):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # ydl.download(urls)
        ie = ydl.extract_info(urls[0], download=False)
        for video in ie["entries"]:
            txt = "Title: {title}\nUrl: {url}\nDescription: {description}\n".format(
                title=video["title"],
                url=video["webpage_url"],
                description=video["description"],
            )
            print(txt)
            with open("json/" + video["title"] + ".json", "w") as file:
                json.dump(video, file)
            ydl.download([video["webpage_url"]])
            upload_video(
                video["title"],
                video["description"],
                "ZDF Magazin Royale vom 20. Mai 2022-220520_2300_sendung433tui_zmr.mp4",
            )
            break


def get_authorized_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build(api_service_name, api_version, credentials=credentials)


def upload_video(title, description, path_to_video):
    youtube = get_authorized_service()

    request = youtube.videos().insert(
        part="snippet, status",
        body={
            "snipppet": {
                "categoryId": "22",
                "description": description,
                "title": title,
            },
            "status": {"privacyStatus": "unlisted"},
        },
        media_body=MediaFileUpload(path_to_video),
    )
    response = request.execute()

    print(response)


def main():
    download_videos(urls)


if __name__ == "__main__":
    main()
