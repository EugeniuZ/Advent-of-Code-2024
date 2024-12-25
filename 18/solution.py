import heapq

from collections import defaultdict, deque

import numpy as np


WALL = '|'
FREE = '.'
INF = float('inf')
WATER = '~'


def main():
    bpos, orig_board, n_drop = get_input('input.txt')
    board = orig_board.copy()
    n = board.shape[0]
    START = (0, 0)
    END = (n-1, n-1)
    for x, y in bpos[:n_drop]:
        board[x, y] = WALL

    _, min_cost = find_path(board, START, END)
    print('Ans1:', min_cost)

    li = n_drop
    ri = len(bpos)
    sz = (ri + li) // 2
    while li < ri:
        sz = (ri+li)//2
        b = board.copy()
        for t in bpos[li: sz+1]:
            b[t] = WALL
        if flood(b, START, END):
            li = sz+1
            board = b
        else:
            ri = sz
    y, x = bpos[ri]
    print(f'Ans2: {x},{y}')


def get_input(infile='input.txt'):
    with open(infile) as f:
        bpos = []
        for line in f.readlines():
            y, x = line.strip().split(',')
            bpos.append((int(x), int(y)))
        n, n_drop = (70, 2**10) if infile == 'input.txt' else (6, 12)
        return bpos, np.full((n+1, n+1), FREE), n_drop


def print_map(map, tiles=None):
    map = map.copy()
    if tiles:
        for t in tiles:
            map[t] = 'O'
    print('\n'.join(''.join(row) for row in map))


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
    best_paths = defaultdict(list)
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
                best_paths[min_cost].append(path)
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

    if not best_paths:
        raise Exception(f'Could not find a path from {start} to {end}')
    return best_paths[min_cost], min_cost


def flood(board, start, end, show=False):
    b = board.copy()
    queue = deque([start])
    dirs = [
        (1, 0),
        (0, 1),
        (0, -1),
        (-1, 0)
    ]
    n = b.shape[0] - 1
    while queue:
        head = queue.pop()
        if head == end:
            break
        for nxt in dirs:
            nxt = nxt[0] + head[0], nxt[1] + head[1]
            if (
                (not (0 <= nxt[0] <= n and 0 <= nxt[1] <= n))
                 or b[nxt] == WALL
                 or b[nxt] == WATER
            ):
                continue
            b[nxt] = WATER
            queue.append(nxt)
    if show:
        print_map(b)
    return head == end


if __name__ == '__main__':
    main()
