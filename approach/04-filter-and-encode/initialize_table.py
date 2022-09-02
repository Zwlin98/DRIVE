import json
import sys
import os
from typing import Iterable
from tqdm import tqdm


def initialize():
    s = set()
    file_path = "filtered_groups.json"
    with open(file_path, "r") as f:
        try:
            groups = json.loads(f.read())
            for cmd, docker_files in tqdm(groups.items()):
                for docker_file in docker_files:
                    for word in docker_file:
                        s.add(word)
        except Exception as err:
            print(err)
            exit(1)

    w_to_n = {}
    n_to_w = {}
    for i, w in enumerate(s):
        w_to_n[w] = i
        n_to_w[i] = w
    with open("table.json", "w") as f:
        f.write(json.dumps({"w_to_n": w_to_n, "n_to_w": n_to_w}))


if __name__ == "__main__":
    initialize()
