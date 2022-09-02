import json


result_drive = "/home/arch/dockerfile/evaluate/rq2/DRIVE/drive.json"
result_hadolint = "/home/arch/dockerfile/evaluate/rq2/hadolint/hadolint.json"


with open(result_drive, "r") as f:
    drive_results = json.loads(f.read())

with open(result_hadolint, "r") as f:
    hadolint_results = json.loads(f.read())

cnt = 0
for sha in hadolint_results:
    r_drive = drive_results.get(sha, [])

    r_hadolint = hadolint_results[sha]

    r_drive.sort()
    r_hadolint.sort()

    if r_hadolint == r_drive == []:
        cnt += 1
        print(sha)
        print("DRIVE: {}".format(r_drive))
        print("HADOLINT: {}".format(r_hadolint))

    # if len(r_hadolint) < len(r_drive):
    #     cnt += 1
    #     print(sha)
    #     print("DRIVE: {}".format(r_drive))
    #     print("HADOLINT: {}".format(r_hadolint))


print(cnt)
