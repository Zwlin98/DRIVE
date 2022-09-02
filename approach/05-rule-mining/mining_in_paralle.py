import json
import os
from functools import partial
from multiprocessing.dummy import Pool
from subprocess import run, PIPE



def process(dir):
    cwd = os.getcwd()
    ab_path = os.path.join(cwd, "groups", dir)
    with open(os.path.join(ab_path, "meta.json"), "r+") as meta:
        s = meta.read()
        j = json.loads(s)
        if j.get("success") is True:
            return
        support = j.get("support") + 10

        command = ["java", "-jar", "spmf/spmf.jar", "run", "PrefixSpan",
                   f"{ab_path}/input.txt", f"{ab_path}/output.txt", f"{str(support)}%"]
        try:
            result = run(command, shell=False, capture_output=True, timeout=15)
            if result.returncode == 0:
                j["success"] = True
                print(f"{dir} mining finished")
            else:
                print(f"Error:{dir} | {result.stdout+result.stderr}")
        except Exception as e:
            print(f"Error:{dir} | {str(e)}")
        j["support"] = support
        meta.seek(0)
        meta.truncate()
        meta.write(json.dumps(j))


def main():
    pool = Pool(50)
    pool.map(process,os.listdir("groups"))

if __name__ == '__main__':
    main()