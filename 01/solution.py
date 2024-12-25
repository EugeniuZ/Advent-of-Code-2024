import pandas as pd

from collections import defaultdict


def main():
    l1, l2 = ans1()
    ans2(l1, l2)


def ans1():
    df = pd.read_csv('input.txt', header=None, sep='   ', engine='python')
    df.columns = ['l1', 'l2']
    l1 = df.l1.sort_values().reset_index(drop=True)
    l2 = df.l2.sort_values().reset_index(drop=True)
    ans1 = (l1-l2).abs().sum()
    print('Answer 1:', ans1)
    return l1, l2


def ans2(l1, l2):
    sim_scores = defaultdict(int)
    s = defaultdict(int)

    it1 = iter(l1.values)
    it2 = iter(l2.values)

    try:
        v1 = next(it1)
        v2 = next(it2)
        while True:
            while v1 in s:
                sim_scores[v1] +=  s[v1]
                v1 = next(it1)
            while v1 != v2:
                while v1 < v2:
                    v1 = next(it1)
                while v1 > v2:
                    v2 = next(it2)
            while v2 == v1:
                s[v1] += v1
                v2 = next(it2)
            sim_scores[v1] = s[v1]
            v1 = next(it1)
    except StopIteration:
        pass

    ans2 = sum(sim_scores.values())
    print('Answer 2:', ans2)


if __name__ == '__main__':
    main()
