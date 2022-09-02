import sys
import json
from tqdm import tqdm
from collections import defaultdict
from pprint import pprint

with open("table.json", "r") as f:
    w_to_n = json.loads(f.read()).get("w_to_n")

with open("filtered_groups.json", "r") as f:
    groups = json.loads(f.read())

# samples = []
# def add_samples(x):
#     if len(samples)<10:
#         samples.append(x)
#     else:
#         for i in samples:
#             print(i)
#         exit(0)

encoded_groups = {}
for cmd, docker_files in tqdm(groups.items()):
    l = []
    for docker_file in docker_files:
        for word in docker_file:
            l.append(str(w_to_n[word]) + " ")
            l.append("-1 ")
        l.append("-2" + "\n")
    encoded_groups[cmd] = "".join(l)
    # add_samples("".join(l))

with open("encoded_groups.json", "w") as f:
    f.write(json.dumps(encoded_groups))
