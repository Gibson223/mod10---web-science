import json
import random
import os
import googleapiclient.discovery

JSON_FILES_PATH = "json/"

YT_API_KEY = "YOUR YOUTUBE API KEY HERE"
START_VID_ID = "YQHsXMglC9A" # Adele - Hello


def get_related_videos(youtube_api_key, video_id):

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=youtube_api_key)

    request = youtube.search().list(
        part="snippet", # get all info
        maxResults=50, #50 is max amount of results per page
        relatedToVideoId=video_id,
        type="video",
        videoCategoryId="10" #category 10 - Music
    )
    response = request.execute()

    with open(f"json/{video_id}.json", 'w', encoding='utf-8') as file:
        json.dump(response, file)

def get_random_id(json_filename):
    with open(JSON_FILES_PATH + json_filename + ".json", "r") as file:
        json_data = json.load(file)

    video_list = json_data["items"]

    random_index = random.randint(0, (len(video_list)-1))

    video = video_list[random_index]
    video_id = video["id"]["videoId"]

    return video_id

def get_viewcount(youtube_api_key, video_id):

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=youtube_api_key)

    request = youtube.videos().list(
        part="statistics", # get all stats
        maxResults=50, #50 is max amount of results per page
        id= video_id
    )
    response = request.execute()

    items = response["items"]

    viewcount_list = []

    for item in items:
        print(item)
        viewcount = item["statistics"]["viewCount"]
        viewcount_list.append(viewcount)

    return viewcount_list[0]


def run_2(youtube_api_key):
    id_list = [START_VID_ID]
    viewcount_list = [get_viewcount(youtube_api_key, START_VID_ID)]

    # get all video ids
    video_id = START_VID_ID
    for number in range(1, 2):
        video_id = get_random_id(video_id)
        id_list.append(video_id)
        viewcount = get_viewcount(youtube_api_key, video_id)
        viewcount_list.append(viewcount)

    return id_list, viewcount_list


# get_related_videos(YT_API_KEY, START_VID_ID)

# print(run_2(YT_API_KEY))