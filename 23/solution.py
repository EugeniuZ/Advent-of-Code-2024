from collections import defaultdict


def main():
    net = get_input()
    tnet = {k: v for k, v in net.items() if k.startswith('t')}
    
    triplets = set()
    for tk, tk2s in tnet.items():
        for tk2 in tk2s:
            for tk3 in net[tk2]:
                if tk in net[tk3]:
                    triplets.add(tuple(sorted([tk, tk2, tk3])))
    print('Ans1:', len(triplets))

    groups = {frozenset([k]) for k in net.keys()}
    while True:
        new_groups = set()
        for group in groups:
            possible_nodes = set.intersection(*[net[node] for node in group])
            for pn in possible_nodes:
                if group <= net[pn]:  # subset check
                    new_groups.add(group | {pn})
        if not new_groups:
            break
        groups = new_groups
       
    for clique in groups:
        print('Ans2:', ','.join(sorted(clique)))
    
    
def get_input(infile='input.txt'):
    res = defaultdict(set)
    with open(infile) as f:
        for line in f.readlines():
            line = line.strip()
            c1, c2 = line.split('-')
            res[c1].add(c2)
            res[c2].add(c1)
    return res


if __name__ == '__main__':
    main()