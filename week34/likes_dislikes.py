import json, os
import matplotlib.pyplot as plt


def read(a: str):
    print(os.getcwd())
    return json.loads(a)


if __name__ == "__main__":
    os.chdir("radio3fm_megahit")
    dic = {}
    for item in sorted(os.listdir()):
        # print(item)
        a = open(item, "r")
        x = json.load(a)
        for f in x:
            f["scraped"] = item
            dic.setdefault(f["snippet"]["title"], []).append(f)
        a.close()

    os.chdir("../plots")
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
        plt.xlabel("difference likes and dislikes")
        plt.ylabel("number of views")
        plt.savefig(key + ".png")
        plt.clf()

    # [print(item["snippet"]["title"], item["scraped"]) for item in res]
    # likes = [int(hit["statistics"]["likeCount"]) for hit in res]
    # dislikes = [int(hit["statistics"]["dislikeCount"]) for hit in res]
    # diff = [like - dislike for like, dislike in zip(likes, dislikes)]
    # print(diff)

    # [dic.setdefault(item[""], []).append(item) for name in ]

