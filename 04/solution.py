def main():
    sboard = get_input()
    ans1 = match_xmas(sboard)
    print('Ans1:', ans1)
    ans2 = match_x_mas(sboard)
    print('Ans2:', ans2)


def get_input(infile='input.txt'):
    with open(infile) as f:
        return [row for row in f.read().splitlines()]


def match_xmas(sboard):
    w = len(sboard[0])
    l = len(sboard)
    matches = []
    for i, row in enumerate(sboard):
        for j, c in enumerate(row):
            if c == 'X':
                # horizontal search
                if j <= w - 4 and row[j+1:j+4] == 'MAS':
                    matches.append([(i, k) for k in range(j, j+4)])
                if j >= 3 and row[j-3:j] == 'SAM':
                    matches.append([(i, k) for k in range(j, j-4, -1)])
                # vertical search
                if i <= l - 4 and sboard[i+1][j] == 'M' and sboard[i+2][j] == 'A' and sboard[i+3][j] == 'S':
                    matches.append([(k, j) for k in range(i, i+4)])
                if i >= 3 and sboard[i-1][j] == 'M' and sboard[i-2][j] == 'A' and sboard[i-3][j] == 'S':
                    matches.append([(k, j) for k in range(i, i-4, -1)])
                # lr diagonal search
                if j <= w - 4 and i <= l - 4 and sboard[i+1][j+1] == 'M' and sboard[i+2][j+2] == 'A' and sboard[i+3][j+3] == 'S':
                    matches.append([(i+k, j+k) for k in range(4)])
                if j >= 3 and i >= 3 and sboard[i-1][j-1] == 'M' and sboard[i-2][j-2] == 'A' and sboard[i-3][j-3] == 'S':
                    matches.append([(i-k, j-k) for k in range(4)])
                # rl diagonal search
                if j >= 3 and i <= l - 4 and sboard[i+1][j-1] == 'M' and sboard[i+2][j-2] == 'A' and sboard[i+3][j-3] == 'S':
                    matches.append([(i+k, j-k) for k in range(4)])
                if j <= w - 4 and i >= 3 and sboard[i-1][j+1] == 'M' and sboard[i-2][j+2] == 'A' and sboard[i-3][j+3] == 'S':
                    matches.append([(i-k, j+k) for k in range(4)])
    return len(matches)


def match_x_mas(sboard):
    nmatches = 0
    for i, row in enumerate(sboard[:-2]):
        for j, _ in enumerate(row[:-2]):
            if sboard[i+1][j+1] == 'A':
                if sboard[i][j] != sboard[i+2][j+2] and sboard[i][j+2] != sboard[i+2][j]:
                    if all(sboard[m][n] in {'M', 'S'} for (m, n) in ((i,j), (i+2, j), (i, j+2), (i+2, j+2))):
                        nmatches += 1
    return nmatches


if __name__ == '__main__':
    main()
