# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.insert
# NOTES:
# 1. This sample code uploads a file and can't be executed via this interface.
#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/code-samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload

import os
import json
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


scopes = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]
path_to_video = "video.mp4"


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_desktop.json"
    credentials = None

    if os.path.exists("token.pickle"):
        print("Loading credentials from file...")
        with open("token.pickle", "rb") as file:
            credentials = pickle.load(file)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing token...")
            credentials.refresh(Request())

        else:
            print("Fetching new tokens")
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes=scopes
            )
            flow.run_local_server(
                port=8080, prompt="consent", authorization_prompt_message=""
            )
            credentials = flow.credentials

            with open("token.pickle", "wb") as file:
                print("Saving credentials for future use...")
                pickle.dump(credentials, file)

    youtube = build(api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails", maxResults=25, playlistId="PLBCF2DAC6FFB574DE"
    )
    response = request.execute()
    print(response)

    # Get credentials and create an API client
    # flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    # credentials = flow.run_console()
    # flow.run_local_server(
    # port=8080, prompt="consent", authorization_prompt_message="Authorize"
    # )


#
# c = credentials.to_json()
# with open("credentials.json", "w") as file:
# json.dump(c, file)

# youtube = googleapiclient.discovery.build(
# api_service_name, api_version, credentials=credentials
# )

# request = youtube.videos().insert(
# part="snippet, status",
# body={
# "snipppet": {
# "categoryId": "22",
# "description": "Test",
# "title": "Titel",
# },
# "status": {"privacyStatus": "unlisted"},
# },
# media_body=MediaFileUpload(path_to_video),
# )
# response = request.execute()


#
# print(response)


if __name__ == "__main__":
    main()
