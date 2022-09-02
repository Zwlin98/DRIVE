import os
from random import sample
import shutil


if __name__ == '__main__':
    origin_dataset = "/home/arch/dockerfile/rule-mining/00-datasets"

    dst_dataset = "/home/arch/dockerfile/evaluate/rq2/validation"

    languages = [
        "C",
        "Cpp",
        "Go",
        "Java",
        "Javascript",
        "PHP",
        "Python",
        "Ruby",
        "Rust",
        "Typescript"
    ]

    res = []

    for lan in languages:
        src = os.path.join(origin_dataset, lan)

        dockerfiles = os.listdir(src)

        dockerfiles = sample(dockerfiles, len(dockerfiles) // 10)

        print("{} files selected for {}".format(len(dockerfiles), lan))

        for dockerfile in dockerfiles:
            src_file = os.path.join(src, dockerfile)
            dst_file = os.path.join(dst_dataset, dockerfile)
            shutil.copy(src_file, dst_file)
