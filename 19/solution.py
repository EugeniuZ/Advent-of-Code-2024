from functools import lru_cache


def main():
    towels, patterns = get_input()
    ans1 = sum(match(p, towels) for p in patterns)
    print('Ans1:', ans1)
    ans2 = sum(match_count(p, towels) for p in patterns)
    print('Ans2:', ans2)


def get_input(infile='input.txt'):
    with open(infile) as f:
        towels = tuple(f.readline().strip().split(', '))
        f.readline()
        patterns = [line.strip() for line in f.readlines()]
    return towels, patterns


def match(p, towels):
    if not p:
        return True
    for t in towels:
        if p.startswith(t):
            m = match(p[len(t):], towels)
            if m:
                return True
    return False


@lru_cache(maxsize=None)
def match_count(p, towels):
    accs = 0
    for t in towels:
        if p == t:
            accs += 1
        if p.startswith(t):
            m = match_count(p[len(t):], towels)
            if m:
                accs += m
    return accs


if __name__ == '__main__':
    main()