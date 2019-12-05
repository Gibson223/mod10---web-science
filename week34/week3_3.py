import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime

# paths used by the functions
# change these if another location for the data is used
spotify_path = "spotify_top100/"
datafolder_path = "youtube_top100/"
# datafolder_path = "radio538_alarmschijf/"
# datafolder_path = "radio3fm_megahit/"

# plot the graphs of the views
# as a function of how many songs have more views than that
# used by the run_graphs() function
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

# show the graphs of the ranking over time
# of a certain song in the Youtube or Spotify top100
# used by the plot_ranking() function
def show_dot_graph(title, spotify_list, youtube_list):
    plt.plot(spotify_list, 'o', label="Spotify", ms=5, color="#1ED760")
    plt.plot(youtube_list, 'o', label="Youtube", ms=5, color="#FF0000")
    plt.ylim(ymin=0, ymax=101)
    plt.title(f"Difference Youtube and Spofity ranking over time; {title}")
    plt.ylabel("Position in the ranking")
    plt.xlabel("Elapsed days")
    plt.legend()
    plt.gca().invert_yaxis()
    filename = f"Difference Youtube and Spofity ranking over time {title}"
    filename = "".join(char for char in filename if char.isalnum() or char == ' ' or char == '-')
    plt.savefig(f"plots/{filename}" + ".png")
    # plt.show()
    plt.clf()


# get data dictionaries used in run_graphs()
# prevents having to go over data multiple times
# this function can be used for Youtube, 3FM and Radio538, but not for Spotify.
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

# returns a dictionary with date mapping to a list
# list is song titles from first to last rank for that date
def get_youtube_top100(path):
    title_dict = {}
    artists_dict = {}

    for filename in os.listdir(path):
        if filename.endswith(".json"):
            top100_title = []

            # get the json data from the file
            with open(path + filename, "r") as file:
                json_data = json.load(file)

            # get the date
            date_unformatted = filename.split('_')[0]
            date = datetime.strptime(date_unformatted, "%Y%m%d").date()

            views_and_titles_dict = {}

            for song in json_data:
                title = song["snippet"]["title"]
                views = int(song["statistics"]["viewCount"])
                views_and_titles_dict[views] = title

            views_list = views_and_titles_dict.keys()
            sorted_views_list = sorted(views_list, reverse=True)


            for views in sorted_views_list:
                top100_title.append(views_and_titles_dict[views])

            title_dict[date] = top100_title

    return title_dict

# returns a dictionary with date mapping to a list
# list is song titles from first to last rank for title_dict
# list is lists of artitsts from first to last rank for artitsts_dict
def get_spotify_top100(path):
    title_dict = {}
    artists_dict = {}

    for filename in os.listdir(path):
        if filename.endswith(".json"):
            top100_title = []
            top100_artists = []

            # get the json data from the file
            with open(path + filename, "r") as file:
                json_data = json.load(file)

            # get the date
            date_unformatted = filename.split('_')[0]
            date = datetime.strptime(date_unformatted, "%Y%m%d").date()

            songs = json_data["tracks"]["items"]

            for song in songs:
                track = song["track"]
                title = track["name"]
                top100_title.append(title)

                artists_data = track["artists"]
                artists = []
                for artist in artists_data:
                    artists.append(artist["name"])
                top100_artists.append(artists)

            title_dict[date] = top100_title
            artists_dict[date] = top100_artists

    return title_dict, artists_dict

# plot the amount of views for each song for the days specified in plot_dates
# as a function of how many songs have more than that amount of views
def run_graphs():
    _, _, _, view_dict, date_dict = get_data_dicts(datafolder_path)

    number_of_days = 1

    plot_dates = [0, 150, 300]

    for i in plot_dates:

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


# plots the ranking for the songs of song_names over time
# in both the Spotify and Youtube top100
def plot_ranking():
    youtube_top100_titles_dict = get_youtube_top100(datafolder_path)
    spotify_top100_titles_dict, spotify_top100_artists_dict = get_spotify_top100(spotify_path)

    song_names = ["Hello", "Sorry", "Hotline Bling", "Bitch Better Have My Money", "The Fix", "Come Get Her"]

    for song in song_names:
        spotify_positions = []
        youtube_positions = []
        for date in youtube_top100_titles_dict:

            spotify = spotify_top100_titles_dict[date]
            position = -1
            for index, current_song in enumerate(spotify):
                if current_song == song:
                    # +1 to start index at position 1 for the graph
                    position = index+1
            spotify_positions.append(position)

            position = -1
            youtube = youtube_top100_titles_dict[date]
            for index, current_song in enumerate(youtube):
                if song in current_song:
                    # +1 to start index at position 1 for the graph
                    position = index+1
            youtube_positions.append(position)

        show_dot_graph(song, spotify_positions, youtube_positions)

# execute code
# run_graphs()
plot_ranking()