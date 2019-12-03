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

def show_graph(title, labels_list, views_list):
    plt.plot(labels_list, views_list, 'o', label="x songs have more than y views")
    plt.title(title)
    plt.ylabel("y: Total number of views")
    plt.xlabel("x: Number of songs")
    # plt.xscale("log")
    # plt.yscale("log")
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
_, _, _, view_dict, date_dict = get_data_dicts(datafolder_path)

number_of_days = 1

# for i in range(number_of_days):
def run_graphs():
    for i in [0, 150, 300]:

    views_for_songs_on_date_list = []

    for song in view_dict: 
        try:
            views_for_songs_on_date_list.append(view_dict[song][i])
        except:
            pass

    views_for_songs_on_date_list = sorted(views_for_songs_on_date_list, reverse=False)
    # test_graph("views", views_for_songs_on_date_list)
    lst = list(range(len(views_for_songs_on_date_list)))[::-1]
    show_graph(f"Songs with amount of views; Day {i}", lst, views_for_songs_on_date_list)

run_graphs()