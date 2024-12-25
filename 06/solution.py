from copy import deepcopy

import numpy as np

from tqdm import tqdm

WALL = '#'

EXIT = -1
LOOP = 1

ROT90 = {
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1),
    (0, 1): (1, 0)
}


def main():
    board = get_input()
    guard, orient = find_point(board, '^'), (-1, 0)

    full_path, cond = walk(board, [(guard, orient)])
    trace = []
    for p in full_path:
        if p[0] not in trace:
            trace.append(p[0])
    print('Ans1:', len(trace))

    ans2 = 0
    bb = board.copy()
    path = [(guard, orient)]
    pb = tqdm(trace[1:])
    for obst in pb:
        b = bb.copy()
        b[obst] = WALL
        apath, cond = walk(b, path)
        if cond == LOOP:
            ans2 += 1
            pb.set_description(f"Found {ans2} loops")
            path = []
            for p1, p2 in zip(apath, full_path):
                if p1 != p2:
                    break
                path.append(p2)
    print('Ans2:', ans2)


def get_input(infile='input.txt'):
    return np.genfromtxt(infile, dtype='U1', delimiter=1, comments=None)


def print_map(map, gpath=None):
    orient = {(1, 0): 'v', (-1, 0): '^', (0, 1): '>', (0, -1): '<'}
    if gpath:
        map = map.copy()
        for p, o in gpath:
            map[p] = orient[o]
    print('\n'.join(''.join(row) for row in map))


def find_point(map, c):
    return list(zip(*np.where(map == c)))[0]


def walk(board, path):
    h, w = board.shape
    path = deepcopy(path)
    d = set(path)
    while True:
        head, orient = path[-1]
        nxt = head[0] + orient[0], head[1] + orient[1]
        if not(0 <= nxt[0] < h and 0 <= nxt[1] < w):
            return path, EXIT
        if board[nxt] == WALL:
            nxt, orient = head, ROT90[orient]
        if (nxt, orient) in d:
            return path, LOOP
        path.append((nxt, orient))
        d.add((nxt, orient))


if __name__ == '__main__':
    main()
