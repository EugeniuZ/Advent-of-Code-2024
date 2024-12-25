from collections import defaultdict
from functools import cmp_to_key


def main():
    rules, updates = get_input()
    ans1, bad_updates = solve_1(rules, updates)
    print('Ans1:', ans1)
    ans2 = solve_2(rules, bad_updates)
    print('Ans2:', ans2)


def get_input(infile='input.txt'):
    rules = defaultdict(set)
    updates = []
    with open(infile) as f:
        initer = iter(f)
        while True:
            try:
                line = next(initer).strip()
                if line:
                    p1, p2 = line.split('|')
                    rules[int(p1)].add(int(p2))
                else:
                    while True:
                        updates.append([int(n) for n in next(initer).split(',')])
            except StopIteration:
                break
    return rules, updates


def solve_1(rules, updates):
    ans1 = 0
    bad_updates = []
    for update in updates:
        assert len(update) % 2 == 1
        mid = update[len(update)//2]
        for n1, n2 in zip(update[:-1], update[1:]):
            if (
                (n1 in rules and n2 not in rules[n1])
                or (n2 in rules and n1 in rules[n2])
            ):
                bad_updates.append(update)
                break
        else:
            ans1 += mid
    return ans1, bad_updates


def solve_2(rules, bad_updates):

    def cmp_by_rules(n1, n2):
        if n1 in rules and n2 in rules[n1]:
            return -1
        if n2 in rules and n1 in rules[n2]:
            return 1
        return 0

    ans2 = 0
    for update in bad_updates:
        good_update = sorted(update, key=cmp_to_key(cmp_by_rules))
        ans2 += good_update[len(good_update)//2]
    return ans2


if __name__ == '__main__':
    main()
