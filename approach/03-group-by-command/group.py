import json
import os
from collections import defaultdict

from tqdm import tqdm

with open("commands.json") as f:
    cmds = json.loads(f.read())

groups = defaultdict(list)

for parsed_dockerfile in tqdm(os.listdir("../02-parsed-dockerfiles")):
    file = os.path.join("../02-parsed-dockerfiles", parsed_dockerfile)
    with open(file) as f:
        try:
            line = json.loads(f.read())
            for cmd in cmds:
                fmt = f"SHELL-CMD-[{cmd}]"
                if fmt in line:
                    groups[fmt].append(line)
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
