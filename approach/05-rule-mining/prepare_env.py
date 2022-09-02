#!/usr/bin/python3
import json
import os
import hashlib

with open("../04-filter-and-encode/encoded_groups.json") as encoded_groups:
    j = json.loads(encoded_groups.read())
    os.makedirs("groups", exist_ok=True)

    for key, input_text in list(j.items()):
        # key_digest = hashlib.md5(key.encode()).hexdigest()[:5]
        # n_key = "".join([c if c.isalnum() else "-" for c in key])
        os.makedirs(f"groups/{key}",exist_ok=True)

        with open(f"groups/{key}/meta.json", "w") as f:
            f.write(
                json.dumps(
                    {
                        "name": key,
                        "lines_num": input_text.count("\n"),
                        "support": 40 - 10,
                        "success": False,
                    }
                )
            )

        with open(f"groups/{key}/input.txt", "w") as f:
            f.write(input_text)
