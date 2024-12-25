from collections import deque, defaultdict

import numpy as np

START = 'S'
END = 'E'
WALL = '#'
FREE = '.'
INF = float('inf')


def main():
    orig_maze, start, end = get_input()
    maze = orig_maze.copy()
    best_paths, min_cost = find_best_paths(maze, start)
    print('Ans1:', min_cost)
    tiles = set()
    for bp in best_paths:
        tiles.update(bp)
    print('Ans2:', len(tiles))


def get_input(infile='input.txt'):
    maze = np.genfromtxt(infile, dtype='U1', delimiter=1, comments=None)
    return maze, find_point(maze, START), find_point(maze, END)


def find_point(maze, c):
    return list(zip(*np.where(maze == c)))[0]


def print_maze(maze, tiles=None):
    if tiles:
        maze = maze.copy()
        for t in tiles:
            maze[t] = 'O'
    print('\n'.join(''.join(row) for row in maze))


def find_best_paths(maze, start):
    orient = (0, 1)  # "orient east initially"
    costs = np.full(maze.shape, INF)
    queue = deque(
        [
            [[start], orient, 0]
        ]
    )
    min_cost = float('inf')
    best_paths = defaultdict(list)
    
    rotations = {
        (0, 1): [(1, 0), (-1, 0)],
        (0, -1): [(1, 0), (-1, 0)],
        (1, 0): [(0, 1), (0, -1)],
        (-1, 0): [(0, 1), (0, -1)],
    }
    
    while queue:
        path, orient, cost = queue.popleft()
        if cost > min_cost:
            continue
        head = path[-1]
        if maze[head] == END:
            min_cost = min(min_cost, cost)
            if cost == min_cost:
                best_paths[cost].append(path)
            continue
        nxt = head[0] + orient[0], head[1] + orient[1]
        if maze[nxt] != WALL and nxt not in path and cost + 1 <= costs[nxt] + 1000:  # +1000 if the path is not complete we can always turn from this point as next step
            costs[nxt] = cost + 1
            entry = [
                path + [nxt], 
                orient, 
                cost + 1
            ]
            queue.append(entry)
        for rot in rotations[orient]:
            rnxt = head[0] + rot[0], head[1] + rot[1]
            if maze[rnxt] != WALL and rnxt not in path and cost + 1001 <= costs[rnxt]:
                costs[nxt] = min(costs[nxt], cost + 1001)
                entry = [
                    path + [rnxt],
                    rot,
                    cost + 1001
                ]
                queue.append(entry)
    return best_paths[min_cost], min_cost


if __name__ == '__main__':
    main()