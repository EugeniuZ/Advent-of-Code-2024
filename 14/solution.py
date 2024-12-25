from copy import deepcopy

import numpy as np


def main():
    robots, w, h = get_input()
    rs = run_sim(deepcopy(robots), w, h, epochs=100)
    ans1 = compute_safety_score(rs, w, h)
    print('Ans1:', ans1)
    ans2 = find_frame_with_tree(deepcopy(robots), w, h)
    print('Ans2:', ans2)


def get_input(infile='input.txt'):
    with open(infile) as f:
        robots = []
        for line in f.readlines():
            p, v = line.strip().split()
            p = tuple(int(n) for n in p[2:].split(','))
            v = tuple(int(n) for n in v[2:].split(','))
            robots.append([p, v])
    w, h = (11, 7) if infile == 'input-small.txt' else (101, 103)
    return robots, w, h


def run_sim(rs, w, h, epochs=1):
    for i in range(epochs):
        for r in rs:
            px = r[0][0]
            py = r[0][1]
            dx = r[1][0]
            dy = r[1][1]
            r[0] = ((px + dx) % w, (py + dy) % h)
    return rs


def compute_safety_score(rs, w, h):
    mx = w // 2
    my = h // 2
    q = [0, 0, 0, 0]
    for r in rs:
        px = r[0][0]
        py = r[0][1]
        if 0 <= px < mx:
            if 0 <= py < my:
                q[0] += 1
            elif my + 1 <= py:
                q[2] += 1
        elif mx + 1 <= px:
            if 0 <= py < my:
                q[1] += 1
            elif my + 1 <= py:
                q[3] += 1
    score = 1
    for qn in q:
        score *= qn
    return score


def find_frame_with_tree(rs, w, h):
    # idea from the chart in https://www.reddit.com/r/adventofcode/comments/1he0asr/2024_day_14_part_2_why_have_fun_with_image/
    min_var_x = np.var([r[0][0] for r in rs])
    min_var_y = np.var([r[0][1] for r in rs])
    
    for i in range(w * h - 1):  # each robot coordinates is going to repeat itself after at most w * h moves
        rs = run_sim(rs, w, h)
        var_x = np.var([r[0][0] for r in rs])
        var_y = np.var([r[0][1] for r in rs])
        if var_x < min_var_x and var_y < min_var_y:
            min_var_x = var_x
            min_var_y = var_y
            epoch = i + 1
    return epoch


# not used but can print the board
def print_board(rs, w, h):
    b = np.full((w, h), '.', dtype='U1')
    for r in rs:
        b[r[0]] = 'X'
    print("\n".join("".join(row) for row in b))


if __name__ == '__main__':
    main()