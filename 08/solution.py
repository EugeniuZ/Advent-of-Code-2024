from collections import defaultdict
from itertools import combinations


def main():
    antennas, w, h = get_input()
    ans1 = get_antinodes(antennas, w, h)
    print('Ans1:', ans1)
    ans2 = get_antinodes_ext(antennas, w, h)
    print('Ans2:', ans2)


def get_input(infile='input.txt'):
    antennas = defaultdict(list)
    h = 0
    with open(infile) as f:
        for h, line in enumerate(f.readlines()):
            line = line.strip()
            w = len(line) - 1
            for j, c in enumerate(line):
                if c != '.':
                    antennas[c].append((h, j))
    return antennas, w, h


def is_antinode(a, w, h):
    return 0 <= a[0] <= w and 0 <= a[1] <= h


def get_antinodes(antennas, w, h):
    antinodes = set()
    for c, locs in antennas.items():
        for a1, a2 in combinations(locs, 2):
            dx = a2[0] - a1[0]
            dy = a2[1] - a1[1]
            an1 = (a1[0] - dx), (a1[1] - dy)
            if is_antinode(an1, w, h):
                antinodes.add(an1)
            an2 = (a2[0] + dx), (a2[1] + dy)
            if is_antinode(an2, w, h):
                antinodes.add(an2)
    return len(antinodes)


def get_antinodes_ext(antennas, w, h):
    antinodes = set()
    for c, locs in antennas.items():
        for a1, a2 in combinations(locs, 2):
            dx = a2[0] - a1[0]
            dy = a2[1] - a1[1]
            k = 0
            while True:
                an1 = (a1[0] - k*dx), (a1[1] - k*dy)
                if is_antinode(an1, w, h):
                    antinodes.add(an1)
                else:
                    break
                k += 1
            k = 0
            while True:
                an2 = (a2[0] + k*dx), (a2[1] + k*dy)
                if is_antinode(an2, w, h):
                    antinodes.add(an2)
                else:
                    break
                k += 1
    return len(antinodes)


if __name__ == '__main__':
    main()