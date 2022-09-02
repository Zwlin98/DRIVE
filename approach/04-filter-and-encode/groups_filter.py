import json
from tqdm import tqdm

file_path = "../03-group-by-command/groups.json"
with open(file_path, "r") as f1:
    try:
        invalid_cmds = []
        #        invalid_cmds+=[
        #            "install",
        #            "cd",
        #            "["
        #        ]

        groups = json.loads(f1.read())
        for cmd, docker_files in tqdm(groups.items()):
            if len(docker_files) < 20:
                invalid_cmds.append(cmd)

        print(f"Origin groups: {len(groups)}")

        for cmd in invalid_cmds:
            del groups[cmd]

        print(f"Filtered groups: {len(groups)}")

        with open("filtered_groups.json", 'w') as f2:
            f2.write(json.dumps(groups))

    except Exception as err:
        print(err)
        exit(1)
