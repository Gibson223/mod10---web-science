import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime

# datafolder_path = "youtube_top100/"
# datafolder_path = "radio538_alarmschijf/"
datafolder_path = "radio3fm_megahit/"

nr_of_plots = 1

def show_graph(title, labels_list, likes_list, dislikes_list, difference_list):
    plt.plot(labels_list, likes_list, label="likes")
    plt.plot(labels_list, dislikes_list, label="dislikes")
    plt.plot(labels_list, difference_list, label="difference")
    plt.title(title)
    plt.xlabel("Number of views")
    plt.ylabel("Likes/Dislikes")
    plt.autoscale()
    plt.legend()
    filename = "".join(char for char in title if char.isalnum() or char == ' ' or char == '-')
    plt.savefig(f"plots/{filename}" + ".png")
    # plt.show()
    plt.clf()


def get_data_dicts(path):
    like_dict = {}
    dislike_dict = {}
    difference_dict = {}
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
                    view_dict[key].append(views)
                    date_dict[key].append(date)
                else: 
                    like_dict[key] = [likes]
                    dislike_dict[key] = [dislikes]
                    date_dict[key] = [date]
                    difference_dict[key] = [likes-dislikes]
                    view_dict[key] = [views]

    return like_dict, dislike_dict, difference_dict, view_dict, date_dict


# execute code
like_dict, dislike_dict, difference_dict, view_dict, date_dict = get_data_dicts(datafolder_path)
for song in date_dict:
    show_graph(song, view_dict[song], like_dict[song], dislike_dict[song], difference_dict[song])