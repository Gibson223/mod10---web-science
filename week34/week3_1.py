import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime

datafolder_path = "youtube_top100/"
# datafolder_path = "radio538_alarmschijf/"
# datafolder_path = "radio3fm_megahit/"

nr_of_plots = 1

# show likes, dislikes, difference graph
def ldd_graph(title, labels_list, likes_list, dislikes_list, difference_list):
    plt.plot(labels_list, likes_list, label="likes")
    plt.plot(labels_list, dislikes_list, label="dislikes")
    plt.plot(labels_list, difference_list, label="difference")
    plt.title(title)
    plt.xlabel("Number of views")
    plt.ylabel("Likes/Dislikes")
    plt.autoscale()
    plt.legend()
    filename = "".join(char for char in title if char.isalnum() or char == ' ' or char == '-')
    plt.savefig(f"plots/ldd - {filename}" + ".png")
    # plt.show()
    plt.clf()

# show likes per dislike graph
def lpd_graph(title, total_ratings_list, difference_list):
    plt.plot(total_ratings_list, difference_list, label="Difference = x * (y-1)")
    plt.title(title)
    plt.xlabel("x: Total number of ratings")
    plt.ylabel("y: Likes per dislike ratio")
    plt.autoscale()
    plt.legend()
    filename = "".join(char for char in title if char.isalnum() or char == ' ' or char == '-')
    plt.savefig(f"plots/lpd - {filename}" + ".png")
    # plt.show()
    plt.clf()

# show difference on total ratings graph
def dotr_graph(title, total_ratings_list, difference_list):
    plt.plot(total_ratings_list, difference_list)
    plt.title(title)
    plt.xlabel("x: Total number of ratings")
    plt.ylabel("y: Difference between likes and dislikes")
    plt.autoscale()
    filename = "".join(char for char in title if char.isalnum() or char == ' ' or char == '-')
    plt.savefig(f"plots/dotr - {filename}" + ".png")
    # plt.show()
    plt.clf()

# get the all the necessary data from the dataset at path
# works for Youtube, 3FM and Radio538, NOT Spotify.
def get_data_dicts(path):
    like_dict = {}
    dislike_dict = {}
    difference_dict = {}
    lpd_dict = {}
    total_ratings_dict = {}
    view_dict = {}
    date_dict = {}

    for filename in os.listdir(path):
        if filename.endswith(".json"):

            # get the json data from the file
            with open(path + filename, "r") as file:
                json_data = json.load(file)

            # get the date
            date_unformatted = filename.split('_')[0]
            date = datetime.strptime(date_unformatted, "%Y%m%d").date()

            for song in json_data:
                key = song["snippet"]["title"]
                statistics = song["statistics"]
                likes = int(statistics["likeCount"])
                dislikes = int(statistics["dislikeCount"])
                views = int(statistics["viewCount"])

                if key in date_dict:
                    like_dict[key].append(likes)
                    dislike_dict[key].append(dislikes)
                    difference_dict[key].append(likes-dislikes)
                    lpd_dict[key].append(likes/dislikes)
                    total_ratings_dict[key].append(likes+dislikes)
                    view_dict[key].append(views)
                    date_dict[key].append(date)
                else: 
                    like_dict[key] = [likes]
                    dislike_dict[key] = [dislikes]
                    difference_dict[key] = [likes-dislikes]
                    lpd_dict[key] = [likes/dislikes]
                    total_ratings_dict[key] = [likes+dislikes]
                    view_dict[key] = [views]
                    date_dict[key] = [date]

    return like_dict, dislike_dict, difference_dict, lpd_dict, total_ratings_dict, view_dict, date_dict

# run likes, dislikes, difference graph
def run_ldd():
    like_dict, dislike_dict, difference_dict, _, _, view_dict, _ = get_data_dicts(datafolder_path)
    for song in view_dict:
        ldd_graph(song, view_dict[song], like_dict[song], dislike_dict[song], difference_dict[song])

# run likes per dislike graph
def run_lpd():
    _, _, _, lpd_dict, total_ratings_dict, _, _ = get_data_dicts(datafolder_path)
    for song in total_ratings_dict:
        lpd_graph(song, total_ratings_dict[song], lpd_dict[song])

def run_dotr():
    _, _, difference_dict, _, total_ratings_dict, _, _ = get_data_dicts(datafolder_path)
    for song in total_ratings_dict:
        dotr_graph(song, total_ratings_dict[song], difference_dict[song])

# execute code
# run_ldd()
run_lpd()
run_dotr()