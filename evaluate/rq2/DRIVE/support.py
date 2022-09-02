import collections
import json
import os
from pprint import pprint
from tqdm import tqdm

from rule import BiDRule, LatentPToQRule, PToQRule

goldset = "/home/arch/dockerfile/rule-mining/02.1-parsed-selected-dockerfiles"


def parse(file_path):
    filename = os.path.basename(file_path)
    # 0a1b8b3f4e8ef18048c50458c369b59e987ac72f.Dockerfile

    all_parsed = "/home/arch/dockerfile/rule-mining/02-parsed-dockerfiles"

    sha = filename.split(".")[0]

    parsed_filename = f"{sha}.Dockerfile.parsed"

    parsed_path = os.path.join(all_parsed, parsed_filename)

    if os.path.exists(parsed_path):
        with open(os.path.join(all_parsed, parsed_filename), "r") as f:
            r = json.loads(f.read())
        return r
    return []


if __name__ == '__main__':
    rule_config = ['pq', 'bid', 'latentp']

    rules = []
    for config in rule_config:
        with open(f"/home/arch/dockerfile/evaluate/rq2/DRIVE/conf/{config}.rule.json") as f:
            js = json.loads(f.read())
            for r in js:
                typ = r['type']
                if typ == 'latent_p->q':
                    rules.append(LatentPToQRule(r))
                if typ == 'p->q':
                    rules.append(PToQRule(r))
                if typ == 'bid':
                    rules.append(BiDRule(r))

    dockerfiles = os.listdir(goldset)

    print("DRIVE: Validating {} dockerfiles".format(len(dockerfiles)))

    results = collections.defaultdict(list)

    for dockerfile in tqdm(dockerfiles):
        dp = os.path.join(goldset, dockerfile)

        sha = dockerfile.split(".")[0]

        with open(dp, "r") as f:
            parsed_dockerfile = json.loads(f.read())

        for rule in rules:
            detect_result = rule.detect(parsed_dockerfile)
            id = rule.ID
            results[id].append(detect_result)

    for id, result in results.items():
        cnt = collections.Counter(result)
        OK = cnt['OK']
        FAILED = cnt['FAILED']
        print(id)
        print("OK: {}".format(OK))
        print("FAILED: {}".format(FAILED))
        print("Support: {}%".format(100 * OK / (OK + FAILED)))
