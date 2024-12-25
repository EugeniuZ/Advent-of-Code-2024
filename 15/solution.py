import numpy as np

from io import StringIO


wall = '#'
robot = '@'
box = 'O'
box_l = '['
box_r = ']'
box2 = (box_l, box_r)
free = '.'


def main():
    orig_map, moves = get_input()
    rpos = get_robot_pos(orig_map)

    map = orig_map.copy()
    rp = rpos
    for m in moves:
        if push(map, rp, m):
            rp = rp[0] + m[0], rp[1] + m[1]
    ans1 = compute_score(map)
    print('Ans1:', ans1)

    orig_wmap = widen(orig_map)
    wrpos = get_robot_pos(orig_wmap)

    wmap = orig_wmap.copy()
    wrp = wrpos
    for m in moves:
        if push2(wmap, wrp, m):
            push2(wmap, wrp, m, update=True)
            wrp = wrp[0] + m[0], wrp[1] + m[1]
    ans2 = compute_score(wmap, box=box_l)
    print('Ans2:', ans2)


def get_input(infile='input.txt'):
    with open(infile) as f:
        c = f.read().split('\n\n')
        map = np.genfromtxt(StringIO(c[0]), dtype='U1', delimiter=1, comments=None)
        moves = []
        for a in c[1].strip().replace('\n', ''):
            if a == '<':
                moves.append((0, -1))
            elif a == '>':
                moves.append((0, 1))
            elif a == 'v':
                moves.append((1, 0))
            elif a == '^':
                moves.append((-1, 0))
            else:
                raise Exception(f'Unknown move: {a}')
    return map, moves


def get_robot_pos(map):
    return list(zip(*np.where(map == robot)))[0]


def print_map(map):
    print('\n'.join(''.join(row) for row in map))


def push(map, rp, m):
    rnp = rp[0] + m[0], rp[1] + m[1]
    el = map[rnp]
    if el == wall:
        return False
    if el == free or push(map, rnp, m):
        map[rnp], map[rp] = map[rp], map[rnp]
        return True
    return False


def compute_score(map, box=box):
    return sum(gx * 100 + gy for gx, gy in list(zip(*np.where(map == box))))


def widen(map):
    wmap = []
    for row in map:
        wrow = []
        for c in row:
            if c == wall:
                wrow.append(wall)
                wrow.append(wall)
            elif c == box:
                wrow.append(box_l)
                wrow.append(box_r)
            elif c == free:
                wrow.append(free)
                wrow.append(free)
            elif c == robot:
                wrow.append(robot)
                wrow.append(free)
            else:
                raise Exception(f'Unknown char:{c}')
        wmap.append(wrow)
    return np.array(wmap)


def push2(wmap, wrp, m, update=False):
    wrnp = wrp[0] + m[0], wrp[1] + m[1]
    el = wmap[wrnp]
    if el == wall:
        return False
    if (
        el == free
        or (
            el in box2 and m[0] == 0
            and push2(wmap, wrnp, m, update=update)
        )
    ):  # left or right push is just like the 1-cell case
        if update:
            wmap[wrnp], wmap[wrp] = wmap[wrp], wmap[wrnp]
        return True
    if el in box2 and m[1] == 0: # up or down push -> one box can move 2 other boxes!
        if (
            push2(wmap, wrnp, m, update=update)
            and push2(wmap, (wrnp[0], wrnp[1] + (1 if el == box_l else -1)), m, update=update)
        ):
            if update:
                wmap[wrnp], wmap[wrp] = wmap[wrp], wmap[wrnp]
            return True
    return False


if __name__ == '__main__':
    main()
