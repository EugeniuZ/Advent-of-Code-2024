from collections import defaultdict, deque
from functools import lru_cache

import numpy as np


UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'
PUSH = 'A'
EMPTY = ''

npad = np.array([
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['', '0', 'A']
])

dpad = np.array([
    ['', '^', 'A'],
    ['<', 'v', '>']
])

dirs = {
    (0, 1): RIGHT,
    (0, -1): LEFT,
    (1, 0): DOWN,
    (-1, 0): UP
}
opposite = {
    LEFT: RIGHT,
    RIGHT: LEFT,
    UP: DOWN,
    DOWN: UP
}


@lru_cache
def switches(s):
    if not s:
        return 0
    cur = s[0]
    res = 0
    for c in s[1:]:
        if c != cur:
            res += 1
            cur = c
    return res


def ffill(pad, start):
    queue = deque([
        [start]
    ])
    paths = defaultdict(list)
    h, w = pad.shape

    while queue:
        path = queue.popleft()
        start = path[0]
        end = path[-1]
        orig_pair = f'{pad[start]}{pad[end]}'
        if start == end:
            paths[orig_pair] = [[EMPTY]]
        c1 = pad[start]
        for delta, direction in dirs.items():
            nxt = end[0] + delta[0], end[1] + delta[1]
            if not (0 <= nxt[0] < h):
                continue
            if not (0 <= nxt[1] < w):
                continue
            c2 = pad[nxt]
            if c2 == EMPTY:
                continue
            new_pair = f'{pad[start]}{pad[nxt]}'
            new_path = path + [nxt]
            new_dirs = [p + [direction] for p in paths[orig_pair]]
            include_paths = False
            if new_pair not in paths:
                for new_dir in new_dirs:
                    paths[new_pair].append(new_dir)
                    include_paths = True
            else:
                adir = paths[new_pair][0]
                for new_dir in new_dirs:
                    if len(new_dir) > len(adir):
                        continue
                    elif len(adir) == len(new_dir):
                        if all(new_dir != adir for adir in paths[new_pair]):
                            paths[new_pair].append(new_dir)
                            include_paths = True
                        else:
                            continue
                    else:
                        raise Exception('Unexpected state')
            if include_paths:
                queue.append(new_path)
                queue.append([nxt])
    return {
        p: sorted(
            [
                ''.join(ap) + PUSH
                for ap in pp
                # filter paths by minimum number of key switches (to reduce path lengths for downstream robots
                if switches(''.join(ap)) == min(switches(''.join(aap)) for aap in pp)
            ])
        for p, pp in sorted(paths.items())
    }


def main():
    codes = get_input()
    d_paths = ffill(dpad, (0, 2))
    n_paths = ffill(npad, (3, 2))
    paths = n_paths | d_paths

    @lru_cache(maxsize=None)
    def min_path_length(code, depth):
        if depth == 0:
            return len(code)
        total_length = 0
        prev = PUSH
        for c in code:
            total_length += min(min_path_length(path, depth-1) for path in paths[f'{prev}{c}'])
            prev = c
        return total_length

    ans1 = sum(min_path_length(code, 3) * int(code.replace('A', '')) for code in codes)
    print('Ans1:', ans1)
    ans2 = sum(min_path_length(code, 26) * int(code.replace('A', '')) for code in codes)
    print('Ans2:', ans2)


def get_input(infile='input.txt'):
    with open(infile) as f:
        return [line.strip() for line in f.readlines()]


if __name__ == '__main__':
    main()
