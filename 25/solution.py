FILL = '#'
EMPTY = '.'


def main():
    keys, locks, h = get_input()
    ans1 = sum(
    all(
        l + k <= h
        for l, k in zip(lock, key)
    )
    for lock in locks
    for key in keys)
    print('Ans1:', ans1)
    print('Ans2: *')  # second star was a gift :)


def get_input(infile='input.txt'):
    keys = []
    locks = []
    with open(infile) as f:
        blocks = f.read().split('\n\n')
        blocks = [b.splitlines() for b in blocks]
        spec = blocks[0]
        h, w = len(spec) - 2, len(spec[0])  # top and bottom row are not part of the lock/key
        for b in blocks:
            el_spec = [-1] * w
            container = keys if b[0][0] == EMPTY else locks
            for line in b:
                for i, c in enumerate(line.strip()):
                    if c == FILL:
                        el_spec[i] += 1
            container.append(el_spec)
    return keys, locks, h


if __name__ == '__main__':
    main()
