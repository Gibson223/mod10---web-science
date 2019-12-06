import json
import random
import os
import googleapiclient.discovery
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

JSON_FILES_PATH = "json/"

YOUTUBE_API_KEY = "YOUTUBE_API_KEY_HERE"

START_VID_ID = "YQHsXMglC9A" # Adele - Hello
START_VID_TITLE = "Adele - Hello"

# plot the graphs of the views
# as a function of how many songs have more views than that
# used by the run_graphs() function
def show_graph(views_list, loglog=False):
    plt.plot(views_list, 'o', label="x videos have more than y views")
    plt.ylabel("y: Total number of views")
    plt.xlabel("x: Number of videos")
    plt.title("Distribution on views for recommended videos")

    filename = "Youtube Recommendations Views Plot"
    if loglog:
        filename = "Youtube Recommendations Views Log-Log Plot"
        plt.title("Log-Log Distribution on views for recommended videos")
        plt.xscale("log")
        plt.yscale("log")

    plt.autoscale()
    plt.legend()
    
    plt.savefig(f"plots/{filename}" + ".png")
    plt.show()
    plt.clf()


def get_related_videos(youtube_api_key, video_id):

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

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

def get_random_video(json_filename):
    with open(JSON_FILES_PATH + json_filename + ".json", "r") as file:
        json_data = json.load(file)

    video_list = json_data["items"]

    random_index = random.randint(0, (len(video_list)-1))

    video = video_list[random_index]
    video_id = video["id"]["videoId"]
    video_title = video["snippet"]["title"]

    return video_id, video_title

def get_viewcounts(youtube_api_key, video_id_list):

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=youtube_api_key)

    repeat_times = (len(video_id_list)//50) + 1

    viewcount_list = []

    for repeat in range(repeat_times):
        try:
            request_list = video_id_list[:50]
            video_id_list = video_id_list[50:]

            ids_string = str(request_list)
            ids_string = ids_string.replace("[", "")
            ids_string = ids_string.replace("]", "")
            ids_string = ids_string.replace("'", "")

            request = youtube.videos().list(
                part="statistics", # get all stats
                maxResults=50, #50 is max amount of results per page
                id= ids_string
            )
            response = request.execute()
            items = response["items"]

            for item in items:
                viewcount = int(item["statistics"]["viewCount"])
                viewcount_list.append(viewcount)
        except:
            pass

    return viewcount_list


def run_50(youtube_api_key):
    id_list = [START_VID_ID]
    title_list = [START_VID_TITLE]
    viewcount_list = []

    # get all video ids
    video_id = START_VID_ID
    for number in range(1, 80):
        try:
            get_related_videos(youtube_api_key, video_id)
            video_id, video_title = get_random_video(video_id)
            id_list.append(video_id)
            title_list.append(video_title)
        except:
            pass

    try:
        viewcount_list = get_viewcounts(youtube_api_key, id_list)
    except:
        pass

    return viewcount_list, id_list, title_list

def run_low_cost():
    id_list = []
    title_list = []

    count = 0
    for filename in os.listdir(JSON_FILES_PATH):
        if filename.endswith(".json"):
            count += 1
            if count <= 1000:
                with open(JSON_FILES_PATH + filename, "r") as file:
                    json_data = json.load(file)

                video_list = json_data["items"]

                for video in video_list:
                    video_id = video["id"]["videoId"]
                    id_list.append(video_id)
                    video_title = video["snippet"]["title"]
                    title_list.append(video_title)

    viewcount_list = get_viewcounts(YOUTUBE_API_KEY, id_list)

    print(id_list)
    print(title_list)
    print(viewcount_list)

    graph_list = sorted(viewcount_list, reverse=True)
    show_graph(graph_list)
    show_graph(graph_list, loglog=True)


def run_code():
    viewcount_list, id_list, title_list = run_50(YOUTUBE_API_KEY)
    print(id_list)
    print(title_list)
    print(viewcount_list)

    graph_list = sorted(viewcount_list, reverse=True)
    show_graph(graph_list)
    show_graph(graph_list, loglog=True)


# execute the code
# run_code()
run_low_cost()