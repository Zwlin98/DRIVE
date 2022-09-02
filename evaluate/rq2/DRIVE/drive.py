import collections
from operator import le
from unittest import result
from tqdm import tqdm
import json
import os
from pprint import pprint

from rule import BiDRule, LatentPToQRule, PToQRule


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
        with open(f"/home/arch/dockerfile/evaluate/rq2/DRIVE/conf2/{config}.rule.json") as f:
            js = json.loads(f.read())
            for r in js:
                typ = r['type']
                if typ == 'latent_p->q':
                    rules.append(LatentPToQRule(r))
                if typ == 'p->q':
                    rules.append(PToQRule(r))
                if typ == 'bid':
                    rules.append(BiDRule(r))

    validation_data = "/home/arch/dockerfile/evaluate/rq2/validation"

    dockerfiles = os.listdir(validation_data)

    print("DRIVE: Validating {} dockerfiles".format(len(dockerfiles)))

    results = collections.defaultdict(list)

    for dockerfile in tqdm(dockerfiles):
        dp = os.path.join(validation_data, dockerfile)

        sha = dockerfile.split(".")[0]

        # if sha != "3cd030609b60ef93df0a259c5795657908f07d41":
        #     continue

        parsed_dockerfile = parse(dp)

        for rule in rules:
            detect_result = rule.detect(parsed_dockerfile)
            if detect_result == "FAILED":
                hadolint = rule.hadolint
                results[sha].append(hadolint)

        if sha not in results:
            results[sha] = []

    print("DRIVE: Found {} rule violations".format(
        sum(len(v) for v in results.values())))

    with open("/home/arch/dockerfile/evaluate/rq2/DRIVE/drive.json", "w") as f:
        f.write(json.dumps(results))
