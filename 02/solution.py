def main():
    reports = get_reports()
    c_s = 0
    for report in reports:
        c_s += is_safe(report)
    print('Ans1:', c_s)

    c_s = 0
    for report in reports:
        c_s += any(is_safe(r) for r in sublists(report))
    print('Ans2:', c_s)


def get_reports():
    infile = 'input.txt'
    reports = []
    with open(infile) as f:
        for line in f:
            report = [int(t) for t in line.split()]
            reports.append(report)
    return reports


def is_safe(report):
    s = report[0] - report[1]
    for l, r in zip(report[:-1], report[1:]):
        d = l - r
        if d * s < 0 or not (1 <= abs(d) <= 3):
            return False
    return True


def sublists(report):
    return [report[:i] + report[i+1:] for i in range(len(report))]


if __name__ == '__main__':
    main()
