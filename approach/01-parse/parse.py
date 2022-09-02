import os
import re
from pprint import pprint

import dockerfile
import abstractions
import subprocess
import json
from tqdm import tqdm

CMD = ""


def parse(file):
    global CMD
    try:
        parsed = dockerfile.parse_file(file)
        items = []
        for directive in parsed:

            if directive.cmd == "FROM":
                if len(directive.flags) != 0:
                    pass
                if ":" in directive.value[0]:
                    image, tag = directive.value[0].split(':')
                else:
                    image = directive.value[0]
                    tag = "latest"
                if tag != "latest":
                    tag = "specific"
                if len(directive.value) == 1:
                    items.append(f"FROM-IMAGE-[{image}]-TAG-[{tag}]")
                if len(directive.value) == 3:
                    items.append(f"FROM-IMAGE-[{image}]-TAG-[{tag}]-AS-NAME")

            if directive.cmd == "RUN":
                it = parse_shell(directive.value[0])
                if it is None:
                    return None
                for i in it:
                    if isinstance(i, str):
                        items.append(f"SHELL-CMD-[{i}]")
                        CMD = i
                    else:
                        for v in i:
                            for abst in abstract(v):
                                items.append(f"CMD-[{CMD}]-ARG-[{abst}]")

            if directive.cmd in ["LABEL", "ENV"]:
                pass
                # assert len(directive.value) % 2 == 0
                # item_set = []
                # values = directive.value
                # for k, v in list(
                #         map(lambda x: values[x * 2: x * 2 + 2], range(len(values) // 2))
                # ):
                #     item_set.append(f"{directive.cmd}-{k}:{v}")
                # items.append(item_set)

            if directive.cmd == "MAINTAINER":
                pass

            if directive.cmd in [
                "EXPOSE",
                "VOLUME",
                "USER",
                "WORKDIR",
                "ARG",
                "ONBUILD",
                "STOPSIGNAL",
            ]:
                for v in directive.value:
                    items.append(f"{directive.cmd}-[{v}]")

            if directive.cmd in ["ADD", "COPY"]:
                if len(directive.flags) != 0:
                    flag = directive.flags[0]
                    if "--from" in flag:
                        flag = "FROM[NAME]"
                    if "--chown" in flag:
                        flag = "CHOWN[OWNER]"
                    dst = directive.value[-1]
                    dst = abstract_single(dst)
                    for src in directive.value[:-1]:
                        for abst in abstract(src):
                            items.append(f"{directive.cmd}-{flag}-[{abst}]-[{dst}]")
                else:
                    dst = directive.value[-1]
                    dst = abstract_single(dst)
                    for src in directive.value[:-1]:
                        for abst in abstract(src):
                            items.append(f"{directive.cmd}-[{abst}]-[{dst}]")

            if directive.cmd in ["ENTRYPOINT", "CMD", "HEALTHCHECK", "SHELL"]:
                token = f"{directive.cmd}"
                for v in directive.value:
                    token += f"-[{v}]"
                items.append(token)

        return items
    except Exception:
        return None


def abstract(token):
    token = token.split()
    token = " ".join(token)
    names = []
    for abss in abstractions.ABSTRACTIONS:
        for abs in abss:
            pattern, name = abs[0], abs[1]
            if pattern.findall(token):
                names.append(name)
                break
    if len(names) > 0:
        return names
    return [token]


def abstract_single(token):
    token = token.split()
    token = " ".join(token)
    for abs in abstractions.ABSTRACTIONS_SINGLE:
        pattern, name = abs[0], abs[1]
        if pattern.findall(token):
            return name
    return token


def merge(token):
    mp = {
        "pip3": "pip"
    }
    if token in mp.keys():
        return mp[token]
    return token


def parse_shell(shell_str):
    try:
        r = subprocess.run(
            ["./shellparser"], input=shell_str, text=True, capture_output=True
        )
        cmds = json.loads(r.stdout)
        items = []
        if cmds is None:
            return None
        for cmd in cmds:
            items.append(cmd["cmd"])
            args = cmd.get("args")
            if args:
                items.append(args)
        return items
    except Exception as e:
        raise e


if __name__ == '__main__':
    with open("selected.json") as f:
        selected = json.loads(f.read())
    datasets = "../00-datasets"
    dst = "../02.1-parsed-selected-dockerfiles"
    for dir in os.listdir(datasets):
        dir = os.path.join(datasets, dir)
        if not os.path.isdir(dir):
            continue
        for dfile in tqdm(os.listdir(dir)):
            sha, _ = dfile.split(".")
            if sha not in selected:
                continue
            file = os.path.join(dir, dfile)
            items = parse(file)
            if items:
                r = []
                for it in items:
                    for x in abstract(it):
                        r.append(x)
                with open(f"{dst}/{dfile}.parsed", "w") as f:
                    f.write(json.dumps(r))
# print("\n".join(parse("exp1.Dockerfile")))
