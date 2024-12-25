import numpy as np

from collections import deque


def main():
    garden = get_input()
    plots = get_plots(garden.copy())
    print('Ans1:', sum(len(p) * get_perimeter(p) for p in plots))
    print('Ans2:', sum(len(p) * get_perimeter2(p) for p in plots))


def get_input(infile='input.txt'):
    return np.genfromtxt(infile, dtype='U1', delimiter=1)


def get_plots(g):
    w, h = g.shape
    w -= 1
    h -= 1
    starts = [(0, 0)]
    plots = []
    
    while starts:
        pos = starts.pop()
        if g[pos] == '.':
            continue
        queue = deque([pos])
        veg = g[pos]
        plot = []
        pos = None
        while queue:
            r, c = queue.pop()
            if g[r, c] == '.':
                continue
            plot.append((r, c))
            g[r, c] = '.'
            if r < h:
                down = r + 1, c
                if g[down] == veg:
                    queue.append(down)
                elif g[down] != '.':
                    starts.append(down)
            if r > 0:
                up = r - 1, c
                if g[up] == veg:
                    queue.append(up)
                elif g[up] != '.':
                    starts.append(up)
            if c < w:
                right = r, c + 1
                if g[right] == veg:
                    queue.append(right)
                elif g[right] != '.':
                    starts.append(right)
            if c > 0:
                left = r, c - 1
                if g[left] == veg:
                    queue.append(left)
                elif g[left] != '.':
                    starts.append(left)
        plots.append(plot)
    return plots


def _get_sides(plot):
    sides = set()
    for r, c in plot:
        for s in [
            ((r, c), (r, c+1)),
            ((r, c), (r+1, c)),
            ((r+1, c), (r+1, c+1)),
            ((r, c+1), (r+1, c+1)),
        ]:
            if s in sides:
                sides.remove(s)  # if sides overlap they are not part of the perimeter
            else:
                sides.add(s)
    return sides


def get_perimeter(plot):
    return len(_get_sides(plot))


def get_perimeter2(plot):
    sides = _get_sides(plot)
    
    horiz_sides = [s for s in sides if s[0][0] == s[1][0]]
    vert_sides = [s for s in sides if s[0][1] == s[1][1]]

    nsides = 0
    
    sides = sorted(horiz_sides, key=lambda seg: (seg[0][0], seg[1][0], seg[0][1], seg[1][1]))
    s0 = sides[0]
    nsides += 1
    hsides = []
    p1 = s0[0]
    for s in sides[1:]:
        if (
            s0[0][0] != s[1][0]  # different rows
            or 
            s0[1] != s[0]  # same row but not connected
        ):
            hsides.append((p1, s0[1]))
            p1 = s[0]
            nsides += 1
        s0 = s
    hsides.append((p1, s0[1]))
    
    sides = sorted(vert_sides, key=lambda seg: (seg[0][1], seg[1][1], seg[0][0], seg[1][0]))
    s0 = sides[0]
    nsides += 1
    vsides = []
    p1 = s0[0]
    for s in sides[1:]:
        if (
            s0[0][1] != s[1][1]  # different columns
            or 
            s0[1] != s[0]  # same column but not connected
        ):
            vsides.append((p1, s0[1]))
            p1 = s[0]
            nsides += 1
        s0 = s
    vsides.append((p1, s0[1]))
    
    # check for the special case of inside holes (lines can intersect)
    for hside in hsides:
        for vside in vsides:
            if hside[0][1] < vside[0][1] < hside[1][1] and vside[0][0] < hside[0][0] < vside[1][0]:
                nsides += 2  # a cross of 2 longer lines counts as 4 lines now
    return nsides

    
if __name__ == '__main__':
    main()