import collections
import json
import os
from pprint import pprint
from unittest import result
from tqdm import tqdm
from typing import Tuple
from subprocess import Popen, PIPE, STDOUT


validation_set = "/home/arch/dockerfile/evaluate/rq2/validation"


class CmdMixin:
    def execute(self, args, position=os.getcwd()) -> Tuple[str, bool]:
        try:
            with Popen(args, stderr=STDOUT, stdout=PIPE, cwd=position) as proc:
                out_or_err = proc.stdout.read().decode()
            return out_or_err, proc.returncode == 0
        except Exception as err:
            return str(err), False


def hadolint(dockerfile):
    command = "/home/arch/dockerfile/evaluate/rq2/hadolint/hadolint --config /home/arch/dockerfile/evaluate/rq2/hadolint/hadolint.yaml -f json {}".format(
        dockerfile)
    out, success = CmdMixin().execute(command.split())
    j = json.loads(out)
    res = set()
    for r in j:
        code = r['code']
        if code in ["DL3042", "DL3038", "DL3019", "DL3034", "DL3030", "DL3014", "DL3015", "DL3009", "DL3040", "DL3032"]:
            res.add(code)
    return list(res)


if __name__ == '__main__':
    dockerfiles = os.listdir(validation_set)
    print("hadolint: Validating {} dockerfiles".format(len(dockerfiles)))

    results = {}
    for dockerfile in tqdm(dockerfiles):
        sha = dockerfile.split(".")[0]
        src_file = os.path.join(validation_set, dockerfile)
        res = hadolint(src_file)
        results[sha] = res

    print("hadolint: Found {} rule violations".format(
        sum(len(r) for r in results.values())))

    with open("/home/arch/dockerfile/evaluate/rq2/hadolint/hadolint.json", "w") as f:
        f.write(json.dumps(results))
