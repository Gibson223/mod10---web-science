import datetime as dt
import json
import os

import matplotlib.pyplot as plt

import matplotlib.dates as mdates
import numpy as np
from matplotlib.dates import AutoDateFormatter, AutoDateLocator


def graph_youtube(root):
    os.chdir(root)
    dic = {}
    for item in sorted(os.listdir()):
        a = open(item, "r")
        x = json.load(a)
        for f in x:
            f["scraped"] = item
            dic.setdefault(f["snippet"]["title"], []).append(f)
        a.close()

    if not os.path.exists("../plots"):
        os.mkdir("../plots")
    os.chdir("../plots")

    if os.path.exists(root.split("_")[0]):
        print("already existed")
    else:
        os.mkdir(root.split("_")[0])
        print("created dir")

    os.chdir(root.split("_")[0])
    for key, item in dic.items():
        plt.plot(
            [int(view["statistics"]["viewCount"]) for view in item],
            [
                int(view["statistics"]["likeCount"])
                - int(view["statistics"]["dislikeCount"])
                for view in item
            ],
            "ro-",
        )
        plt.title("difference in likes and dislikes for " + key)
        plt.ylabel("difference likes and dislikes")
        plt.xlabel("number of views")
        plt.savefig(
            "".join(char for char in key if char.isalnum() or char == " ") + ".png"
        )
        plt.clf()

    os.chdir("../..")

    return dic


def dump_smaller():
    a = json.load(open("spotify_top100/20151109_1328_data.json"))
    print(a)
    a["tracks"]["items"] = a["tracks"]["items"][0:10:2]
    with open("res.json", "w") as f:
        f.write(json.dumps(a))


def graph_alarm(root):
    os.chdir(root)
    dic = {}
    for item in sorted(os.listdir()):
        a = open(item, "r")
        x = json.load(a)
        for f in x:
            f["scraped"] = item.split("_")[0]
            dic.setdefault(f["snippet"]["title"], []).append(f)
        a.close()

    if not os.path.exists("../plots"):
        os.mkdir("../plots")
    os.chdir("../plots")

    if os.path.exists(root.split("_")[0]):
        print("already existed")
    else:
        os.mkdir(root.split("_")[0])
        print("created dir")

    os.chdir(root.split("_")[0])

    for key, item in dic.items():
        fig, ax = plt.subplots()
        ax.plot_date(
            [dt.datetime.strptime(view["scraped"], "%Y%m%d") for view in item],
            [int(view["statistics"]["viewCount"]) for view in item],
            "ro-",
        )
        ax.set_title("difference in likes and dislikes for\n " + key)
        ax.set_ylabel("views")
        ax.set_xlabel("date")

        # locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        locator = mdates.AutoDateLocator()
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

        plt.gcf().autofmt_xdate()

        fig.savefig(
            "".join(char for char in key if char.isalnum() or char == " ") + ".png"
        )
    os.chdir("../..")

    return dic


if __name__ == "__main__":
    # graph_youtube("radio3fm_megahit")
    # graph_youtube("youtube_top100")
    # graph_alarm(root="radio538_alarmschijf")
    graph_youtube(root="radio538_alarmschijf")
