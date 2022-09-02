from pprint import pprint
from typing import List

from typing import Optional


class BaseRule:
    def __init__(self, rule):
        self.meaning = rule['meaning']
        self.level = rule['level']
        self.hadolint = rule.get('hadolint', None)
        self.ID = rule.get('ID', None)

    def __repr__(self):
        return self.meaning

    def detect(self, dockerfile):
        raise NotImplementedError

    @staticmethod
    def find_first_subseq(text: list, pattern: list) -> Optional[list]:
        if len(text) < len(pattern):
            return None

        posi = []
        j = 0
        for i in range(len(text)):
            if j >= len(pattern):
                break
            if text[i] != pattern[j]:
                continue
            else:
                posi.append(i)
                j += 1
        if j >= len(pattern):
            return posi
        else:
            return None

    @staticmethod
    def find_last_subseq(text: list, pattern: list) -> Optional[list]:
        imd = BaseRule.find_first_subseq(text[::-1], pattern[::-1])
        if imd is None:
            return None
        else:
            return [len(text) - 1 - i for i in imd[::-1]]


class PToQRule(BaseRule):
    def __init__(self, rule):
        super().__init__(rule)
        self.p = rule['p']
        self.q = rule['q']

    def detect(self, dockerfile: List[str]):
        if self.find_last_subseq(dockerfile, self.p) is None:
            return "NOT FOUND"

        def check(text):
            last_indexes_p = self.find_last_subseq(text, self.p)
            if last_indexes_p is None:
                return True
            last_indexes_q = self.find_last_subseq(
                text[last_indexes_p[-1]:], self.q)
            if last_indexes_q is None:
                return False
            return check(text[:last_indexes_p[0]])

        return 'OK' if check(dockerfile) else "FAILED"


class LatentPToQRule(BaseRule):
    def __init__(self, rule):
        super().__init__(rule)
        self.latent_p = rule['latent_p']
        self.q = rule['q']

    def detect(self, dockerfile):

        lp_index = -1

        for p in self.latent_p:
            lp = self.find_last_subseq(dockerfile, p)
            if lp is not None:
                lp_index = max(lp_index, lp[-1])

        if lp_index == -1:
            return "NOT FOUND"

        for q in self.q:
            if self.find_first_subseq(dockerfile[lp_index:], q) is not None:
                return "OK"

        return "FAILED"


class QToPRule(BaseRule):
    def __init__(self, rule):
        super().__init__(rule)
        self.q = rule['q']
        self.p = rule['p']

    def detect(self, dockerfile: List[str]):
        if self.find_first_subseq(dockerfile, self.q) is None:
            return "NOT FOUND"

        def check(text):
            first_indexes_q = self.find_first_subseq(text, self.q)
            if first_indexes_q is None:
                return True
            first_indexes_p = self.find_first_subseq(
                text[:first_indexes_q[0]], self.p)
            if first_indexes_p is None:
                return False
            return check(text[first_indexes_q[-1] + 1:])

        return 'OK' if check(dockerfile) else "FAILED"


class BiDRule(BaseRule):
    def __init__(self, rule):
        super().__init__(rule)
        self.p = rule["p"]
        self.q = rule["q"]
        self.r = rule["r"]

    def find_first_seg(self, text, pattern):

        lp = len(pattern)

        for i in range(len(text) - lp):
            if text[i:i + lp] == pattern:
                return list(range(i, i + lp))

        return None

    def detect(self, dockerfile):
        q_index = self.find_first_seg(dockerfile, self.q)
        # print(q_index)
        if q_index is None:
            return "NOT FOUND"

        p_index = self.find_first_subseq(dockerfile[:q_index[0]], self.p)
        r_index = self.find_first_subseq(dockerfile[q_index[-1] + 1:], self.r)

        return "FAILED" if None in [p_index, r_index] else "OK"


# class SpecialRule(BaseRule):
#
#     def detect(self, dockerfile):


# if __name__ == '__main__':
#     rule_config = ['pq', 'bid', 'latentp']

#     rules = []
#     for config in rule_config:
#         with open(f"{config}.rule.json") as f:
#             js = json.loads(f.read())
#             for r in js:
#                 typ = r['type']
#                 if typ == 'latent_p->q':
#                     rules.append(LatentPToQRule(r))
#                 if typ == 'p->q':
#                     rules.append(PToQRule(r))
#                 if typ == 'bid':
#                     rules.append(BiDRule(r))

#     parsed_dockerfiles = "../rule-mining/02-parsed-dockerfiles"

#     # dockerfile_paths = os.listdir(parsed_dockerfiles)

#     dockerfile_paths = ['bid.example.Dockerfile']

#     results = {}

#     for dp in dockerfile_paths:
#         # dp = os.path.join(parsed_dockerfiles, dp)

#         # with open(dp) as f:
#         #     dockerfile = json.loads(f.read())

#         dockerfile = parse_path(dp)

#         print(dockerfile)

#         for rule in rules:
#             detect_result = rule.detect(dockerfile)
#             if detect_result != "NOT FOUND":
#                 meaning = rule.meaning
#                 if meaning not in results:
#                     results[meaning] = collections.Counter()
#                 results[meaning][detect_result] += 1

#     pprint(results)
