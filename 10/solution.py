from collections import deque

import numpy as np


def main():
    map = get_input()
    w, h = map.shape
    w -= 1
    h -= 1

    trailheads = list(zip(*np.where(map == 0)))

    scores = 0
    ratings = 0

    for th in trailheads:
        queue = deque([th])
        peaks = set()
        while queue:
            pos = queue.pop()
            if map[pos] == 9:
                peaks.add(pos)
                ratings += 1
                continue
            r, c = pos
            nv = map[pos] + 1
            if r < h:
                down = (r+1, c)
                if map[down] == nv:
                    queue.append(down)
            if r > 0:
                up = (r-1, c)
                if map[up] == nv:
                    queue.append(up)
            if c < w:
                right = (r, c+1)
                if map[right] == nv:
                    queue.append(right)
            if c > 0:
                left = (r, c-1)
                if map[left] == nv:
                    queue.append(left)
        scores += len(peaks)

    print('Ans1:', scores)
    print('Ans2:', ratings)


def get_input(infile='input.txt'):
    with open(infile) as f:
        return np.genfromtxt(infile, dtype='int8', delimiter=1)


if __name__ == '__main__':
    main()
