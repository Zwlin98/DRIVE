import os
import re

dirs = os.listdir("./groups")
for dir in dirs:
    if not os.path.isdir(f"./groups/{dir}"):
        continue
    res = []
    with open(f"./groups/{dir}/sub_seq_filtered_output.txt") as f:
        for line in f.readlines():
            tokens = line.strip().split()
            pattern = re.compile(r"SHELL-CMD-\[(.+)]")
            ok = True
            for i, token in enumerate(tokens):
                def check():
                    ma = pattern.match(token)
                    if ma:
                        cmd = ma.group(1)
                        arg_pattern = f"CMD-[{cmd}]-ARG-["
                        print(arg_pattern)
                        find_arg = False
                        for tk in tokens[i + 1:]:
                            if arg_pattern in tk:
                                find_arg = True
                                break
                        return find_arg
                    else:
                        return True


                ok = ok and check()
            if ok:
                res.append(line.strip())

    with open(f"./groups/{dir}/no_arg.txt", "w") as f:
        f.write("\n".join(res))
        f.write("\n")
