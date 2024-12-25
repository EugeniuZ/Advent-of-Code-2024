from functools import lru_cache
from collections import defaultdict


def main():
    d = defaultdict(int)
    for s in get_input():
        d[s] += 1

    d = arrange_stones(d, 25)
    print('Ans1:', sum(d.values()))

    d = arrange_stones(d, 50)
    print('Ans2:', sum(d.values()))
    

def arrange_stones(d, blinks):
    for _ in range(blinks):
        tt = defaultdict(int)
        for k, v in d.items():
            for n in blink(k):
                tt[n] += v
        d = tt
    return d

def get_input(infile='input.txt'):
    with open(infile) as f:
        return [int(n) for n in f.read().split(' ')]


@lru_cache(maxsize=None)
def blink(n):
    if n == 0:
        return (1,)
    if len(f'{n}') % 2 == 0:
        s = f'{n}'
        mid = len(s) // 2
        n1, n2 = int(s[:mid]), int(s[mid:])
        return n1, n2
    else:
        return (n * 2024,)


if __name__ == '__main__':
    main()