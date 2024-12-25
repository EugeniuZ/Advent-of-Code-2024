def main():
    eqs = get_input()

    ans1 = 0
    for tv, ns in eqs:
        res = check_eq(ns[1:], tv, ns[0], f'{ns[0]}')
        if res:
            ans1 += tv
    print('Ans1:', ans1)

    ans2 = 0
    for tv, ns in eqs:
        res = check_eq_ext(ns[1:], tv, ns[0], f'{ns[0]}')
        if res:
            ans2 += tv
    print('Ans2:', ans2)


def get_input(infile='input.txt'):
    eqs = []
    with open(infile) as f:
        for line in f.readlines():
            tv, ns = line.strip().split(':')
            tv = int(tv)
            ns = [int(i) for i in ns.strip().split(' ')]
            eqs.append((tv, ns))
    return eqs


def check_eq(ns, tv, cv, ops):
    if cv == tv:
        return ops
    if cv > tv:
        return
    if not ns:
        return
    op = ns[0]
    return check_eq(ns[1:], tv, cv * op, ops + f'*{op}' ) or check_eq(ns[1:], tv, cv + op, ops + f'+{op}')


def check_eq_ext(ns, tv, cv, ops):
    if cv == tv:
        return ops
    if cv > tv:
        return
    if not ns:
        return
    op = ns[0]
    return (
        check_eq_ext(ns[1:], tv, int(f'{cv}{op}'), ops + f'||{op}')
        or check_eq_ext(ns[1:], tv, cv * op, ops + f'*{op}' )
        or check_eq_ext(ns[1:], tv, cv + op, ops + f'+{op}')
    )


if __name__ == '__main__':
    main()
