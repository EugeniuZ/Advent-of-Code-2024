import re


S_MUL = 'mul\(\d{1,3},\d{1,3}\)'
S_DO = 'do\(\)'
S_DONT = 'don\'t\(\)'

RE_MUL = re.compile(S_MUL)
RE_M = re.compile(f'{S_MUL}|{S_DO}|{S_DONT}')


def main():
    program = get_input()
    s = 0
    for m in RE_MUL.findall(program):
        t1, t2 = m[4:-1].split(',')
        s += int(t1) * int(t2)
    print('Ans1:', s)

    s = 0
    enabled = True
    for m in RE_M.findall(program):
        if m.startswith('mul'):
            if enabled:
                t1, t2 = m[4:-1].split(',')
                s += int(t1) * int(t2)
        else:
            enabled = m == 'do()'
    print('Ans2:', s)


def get_input():
    infile = 'input.txt'
    with open(infile) as f:
        return f.read()


if __name__ == '__main__':
    main()
