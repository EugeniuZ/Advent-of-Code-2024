import re

import numpy as np


RE_NUM = re.compile('\d+')


def main():
    games = get_input()
    coins = sum(
        sol[0] * 3 + sol[1] 
        for g in games 
        for sol in [solve(g)] 
        if sol is not None
    )
    print('Ans1:', coins)

    delta = 10000000000000
    coins = sum(
        sol[0] * 3 + sol[1] 
        for g in games 
        for sol in [solve((g[0], g[1], (g[2][0] + delta, g[2][1] + delta)))] 
        if sol is not None
    )
    print('Ans2:', coins)
    

def get_input(infile='input.txt'):
    arcades = []
    with open(infile) as f:
        while True:
            ba = [int(n) for n in RE_NUM.findall(f.readline())]
            if not ba:
                break
            bb = [int(n) for n in RE_NUM.findall(f.readline())]
            loc = [int(n) for n in RE_NUM.findall(f.readline())]
            arcades.append([ba, bb, loc])
            f.readline()
    return arcades


def solve(g):
    A = np.array([g[0], g[1]]).T
    B = np.array(g[2])
    sol = np.linalg.solve(A, B)
    sol_int = np.array([round(n) for n in sol])
    if np.all(B == A@sol_int) and np.all(sol_int > 0):
        return sol_int
    else:
        return None


if __name__ == '__main__':
    main()