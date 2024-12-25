OP = {
    'AND': lambda t1, t2: t1 & t2,
    'OR': lambda t1, t2: t1 | t2,
    'XOR': lambda t1, t2: t1 ^ t2
}


def main():
    wires = get_input()
    print('Ans1:', get_num(wires, 'z'))
    # answer was computed manually using the input-fixed.txt (copy input.txt first into it) and fixing it one gate pair at a time
    # see the comments in fix_wrong_gates()
    print('Ans2:', ','.join(sorted(get_switched_gates())))


def get_input(infile='input.txt'):
    with open(infile) as f:
        c = f.read()
        p1, p2 = c.split('\n\n')
        wires = {}
        for line in p1.strip().splitlines():
            w, v = line.split(': ')
            wires[w] = int(v)

        wires_todo = {}
        for line in p2.strip().splitlines():
            t1, op, t2, _, r = line.strip().split()
            if t1 not in wires or t2 not in wires:
                wires_todo[r] = t1, op, t2
            else:
                wires[r] = OP[op](wires[t1], wires[t2])
        mapping = {}
        while wires_todo:
            temp = {}
            for r, (t1, op, t2) in wires_todo.items():
                if t1 not in wires or t2 not in wires:
                    temp[r] = t1, op, t2
                else:
                    wires[r] = OP[op](wires[t1], wires[t2])
            wires_todo = temp
    return wires


def get_num(wires, prefix):
    result = 0
    for key, value in sorted(
        [
            (k, v)
            for k, v in wires.items()
            if k.startswith(prefix)
        ],
        reverse=True
    ):
        result = (result << 1) + value
    return result


def get_gates(infile='input-fixed.txt'):
    with open(infile) as f:
        c = f.read()
        p1, p2 = c.split('\n\n')
        gates = {}
        total_digits = 0
        for line in p2.strip().splitlines():
            t1, op, t2, _, r = line.strip().split()
            if r.startswith('z'):
                total_digits += 1
            gates[K(t1, t2, op)] = r
        return gates, total_digits - 1  # input digits is one less the output digits


def get_switched_gates(infile1='input.txt', infile2='input-fixed.txt'):
    with open(infile1) as f:
        c = f.read()
        _, orig = c.split('\n\n')

    with open(infile2) as f:
        c = f.read()
        _, fixed = c.split('\n\n')

    swapped_gates = set()

    for oline, fline in zip(orig.strip().splitlines(), fixed.strip().splitlines()):
        if oline != fline:
            o1, _, o2, _, ro = oline.strip().split()
            f1, _, f2, _, rf = fline.strip().split()
            if o1 != f1:
                swapped_gates.add(o1)
                swapped_gates.add(f1)
            if o2 != f2:
                swapped_gates.add(o2)
                swapped_gates.add(f2)
            if ro != rf:
                swapped_gates.add(ro)
                swapped_gates.add(rf)
    return swapped_gates


def K(*args):
    return frozenset(args)


def find_wrong_gates():
    # find c00 and s00 first
    g, n = get_gates('input-fixed.txt')

    carries = []
    digits = []

    carries.append(g[K('x00', 'y00', 'AND')])
    digits.append(g[K('x00', 'y00', 'XOR')])

    # whenever we encounter a wrong gate this will raise an exception
    # we start from LSB 1 and progress to the end fixing gates one pair at a time
    # we assume xnn ^ ynn and xnn & ynn are correct (as well as all previous gates, c(n-1) including)
    # then using the schematic from https://content.instructables.com/F3D/2GZ2/KNVR5S0C/F3D2GZ2KNVR5S0C.png?auto=webp&frame=1&width=601&height=1024&fit=bounds&md=MjAyMS0wNC0yNCAxNjo1Nzo1Mi4w
    # we obtain:
    #   hnn = xnn ^ ynn
    #   znn = hnn ^ c(n-1) (result bit)
    #   ann = xnn & ynn
    #   tnn = hnn & c(n-1)
    #   cnn = ann | tnn (carry bit)
    # whenever we can't find a gate in try/except block -> we have a swap
    # we find the swapped gate by checking hnn, znn, ann, tnn and carries
    for i in range(1, n):
        r = f'{i:02d}'
        print(r)
        h = c = a = t = None
        try:
            h = g[K(f'x{r}', f'y{r}', 'XOR')]
            c = carries[-1]
            digit = g[K(h, c, 'XOR')]
            assert digit.startswith('z'), digit
            digits.append(digit)
            a = g[K(f'x{r}', f'y{r}', 'AND')]
            t = g[K(h, c, 'AND')]
            carries.append(g[K(a, t, 'OR')])
        except:
            print('-' * 20)
            print(f'{h=}, {c=}, {a=}, {t=}')
            print(f'{digits=}')
            print(f'{carries=}')
            raise


if __name__ == '__main__':
    main()
