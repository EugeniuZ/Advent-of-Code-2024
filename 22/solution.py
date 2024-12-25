from collections import defaultdict
from itertools import pairwise


def main():
    secrets = get_input('input.txt')
    ans1 = 0
    sums = defaultdict(int)
    for n in secrets:
        ns = n
        prices = [ns % 10]
        for _ in range(2000):
            ns = generate(ns)
            prices.append(ns % 10)
        ans1 += ns
        diffs = []
        for p1, p2 in pairwise(prices):
            diffs.append(p2 - p1)
        d = {}
        for i in range(len(diffs) - 4):
            key = tuple(diffs[:4])
            price = prices[4]
            if key not in d:
                d[key] = price  # record only first prices for the sequence
                sums[key] += price
            diffs = diffs[1:]
            prices = prices[1:]
    print('Ans1:', ans1)
    print('Ans2:', max(sums.values()))  


def get_input(infile='input.txt'):
    with open(infile) as f:
        return [int(s.strip()) for s in f.readlines()]


def generate(n):
    n = (n ^ (n << 6)) & 0xFFFFFF
    n = (n ^ (n >> 5)) & 0xFFFFFF
    n = (n ^ (n << 11)) & 0xFFFFFF
    return n


if __name__ == '__main__':
    main()