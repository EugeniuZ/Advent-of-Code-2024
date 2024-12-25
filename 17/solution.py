def main():
    A, B, C, program = get_input()
    output = CPU(A, B, C).execute(program)
    print('Ans1:', output)

    # the trick is to start with the end of the program
    # where the output depends on the most significant 3 bits of regA
    # and then generate the output backwards adding 3 more bits to regA
    a_list = [0]
    last = len(program)
    k = last - 1
    while k >= 0:
        t = []
        for reg_a in a_list:
            for aa in range(8):
                aa = reg_a * 8 + aa
                cpu = CPU(aa, B, C)
                out = cpu.execute(program)
                if out.startswith(','.join(str(s) for s in program[k:last])):
                    # print(f'A={aa},', out)
                    t.append(aa)
        a_list = t
        k-=1
    ans2 = min(a_list)
    print('Ans2:', ans2)
    print('Program:\n', ','.join(str(s) for s in program))
    print('Output:\n', CPU(ans2, B, C).execute(program))


def get_input(infile='input.txt'):
    with open(infile) as f:
        a = int(f.readline().strip().split()[-1])
        b = int(f.readline().strip().split()[-1])
        c = int(f.readline().strip().split()[-1])
        f.readline()
        program = [int(c) for c in f.readline().split(':')[1].strip().split(',')]
        return a, b, c, program


class CPU:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.ip = None
        self.out = None
        self.instruction = {
            0: self.op_adv,
            1: self.op_bxl,
            2: self.op_bst,
            3: self.op_jnz,
            4: self.op_bxc,
            5: self.op_out,
            6: self.op_bdv,
            7: self.op_cdv,
        }

    def execute(self, program, ip=None):
        self.ip = ip or 0
        self.out = []
        while True:
            try:
                opcode, operand = program[self.ip: self.ip+2]
                self.instruction[opcode](operand)
                self.ip += 2
                # print(f'>{opcode=}, A={self.a:b}, B={self.b:b}, C={self.c:b}, out={self.out}, IP={self.ip}')
            except (IndexError, ValueError):
                break
        return ','.join([str(c) for c in self.out])

    def op_adv(self, op):
        self.a = int(self.a / 2**(self.combo(op)))

    def op_bxl(self, op):
        self.b = self.b ^ op

    def op_bst(self, op):
        self.b = self.combo(op) % 8

    def op_jnz(self, op):
        if self.a != 0:
            self.ip = op - 2  # it will be increased by 2 in the main loop

    def op_bxc(self, _op):
        self.b = self.b ^ self.c

    def op_out(self, op):
        self.out.append(self.combo(op) % 8)

    def op_bdv(self, op):
        self.b = int(self.a / 2**(self.combo(op)))

    def op_cdv(self, op):
        self.c = int(self.a / 2**(self.combo(op)))

    def combo(self, op):
        if 0 <= op <= 3:
            return op
        if op == 4:
            return self.a
        if op == 5:
            return self.b
        if op == 6:
            return self.c
        else:
            raise ValueError(f'Invalid operand: {op}')


if __name__ == '__main__':
    main()
