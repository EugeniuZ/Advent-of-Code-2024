import heapq

from collections import defaultdict

import numpy as np

START = 'S'
END = 'E'
WALL = '#'
FREE = '.'
INF = float('inf')


def main():
    board, start, end = get_input()
    orig_path, _ = find_path(board, start, end)
    cheats = find_cheats(orig_path, 2, 100)
    print('Ans1:', sum(cheats.values()))
    cheats = find_cheats(orig_path, 20, 100)
    print('Ans2:', sum(cheats.values()))


def get_input(infile='input.txt'):
    board = np.genfromtxt(infile, dtype='U1', delimiter=1, comments=None)
    start, end = find_point(board, START), find_point(board, END)
    return board, start, end


def find_point(board, c):
    return list(zip(*np.where(board == c)))[0]


def print_board(board, tiles=None):
    if tiles:
        board = board.copy()
        for t in tiles:
            board[t] = '|'
    print('\n'.join(''.join(row) for row in board))


def find_path(board, start, end):
    dirs = [
        (1, 0),
        (0, 1),
        (0, -1),
        (-1, 0)
    ]
    costs = np.full(board.shape, INF)
    costs[start] = 0
    min_cost = INF
    best_path = None
    heap = [
        [0, [start]]
    ]
    n = board.shape[0] - 1
    while heap:
        cost, path = heapq.heappop(heap)
        if cost > min_cost:
            continue
        head = path[-1]
        if cost > costs[head]:
            continue
        if head == end:
            if cost <= min_cost:
                min_cost = cost
                best_path = path
                continue
        for nxt in dirs:
            nxt = nxt[0] + head[0], nxt[1] + head[1]
            if (
                (not (0 <= nxt[0] <= n and 0 <= nxt[1] <= n))
                 or board[nxt] == WALL
                 or nxt in path
                 or cost + 1 >= costs[nxt]
            ):
                continue
            costs[nxt] = cost + 1
            heapq.heappush(
                heap,
                [
                    cost + 1,
                    path + [nxt],
                ]
            )

    if not best_path:
        raise Exception(f'Could not find a path from {start} to {end}')
    return best_path, min_cost


def find_cheats(orig_path, max_cheat, min_delta):
    cheats = defaultdict(int)
    path = {pos: i for i, pos in enumerate(orig_path)}
    for i, p1 in enumerate(orig_path[:-1]):
        for p2 in orig_path[i+1:]:
            md = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
            if md > max_cheat:
                continue
            ad = path[p2] - path[p1]
            cost_saving = ad - md
            if cost_saving >= min_delta:
                cheats[cost_saving] += 1
    return cheats


if __name__ == '__main__':
    main()
