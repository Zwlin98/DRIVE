import collections
import json
import os
from pprint import pprint

from tqdm import tqdm

tokens = collections.Counter()
groups = collections.defaultdict(list)

for parsed_dockerfile in tqdm(os.listdir("../02.1-parsed-selected-dockerfiles")):
    file = os.path.join("../02.1-parsed-selected-dockerfiles", parsed_dockerfile)
    with open(file) as f:
        try:
            line = json.loads(f.read())
            for token in line:
                if token.startswith("SHELL-CMD-"):
                    if '=' not in token:
                        tokens[token] += 1
                        groups[token].append(line)
        except:
            print(file)

print(len(groups))

with open("groups.json", "w") as f:
    f.write(json.dumps(groups))

pairs = []
with open("groups_details.txt", "w") as f:
    for k, v in groups.items():
        pairs.append((k, len(v)))
    pairs.sort(key=lambda x: x[1], reverse=True)
    for k, v in pairs:
        f.write(f"{v} {k}\n")
