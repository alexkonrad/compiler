from compiler.opcode import OpCode

class OpCodeGenerator:
    buf = []
    pc = 0
    debug = True

    @staticmethod
    def put_f1(op: OpCode, a, b, c):
        """
        Arguments:
            op: 6-bit opcode
            a: 5-bit argument (takes register number)
            b: 5-bit argument (takes register number)
            c: 5-bit argument (takes register number)

        """
        if OpCodeGenerator.debug:
            print(f"{op.name} | F1 | {a} | {b} | {c}")
        OpCodeGenerator.buf.append(op.value << 26 | a << 21 | b << 16 | c)

    @staticmethod
    def put_f2(op: OpCode, a, b, c):
        """
        Arguments:
            op: 6-bit opcode
            a: 5-bit argument (takes register number)
            b: 5-bit argument (takes register number)
            c: 5-bit argument (takes register number)
        """
        if OpCodeGenerator.debug:
            print(f"{op.name} | F2 | {a} | {b} | {c}")
        OpCodeGenerator.buf.append(op.value << 26 | a << 21 | b << 16 | c)

    @staticmethod
    def put_f3(op: OpCode, c):
        """
        Arguments:
            op: 6-bit opcode
            c:  26-bit argument
        """
        if OpCodeGenerator.debug:
            print(f"{op.name} | F3 | {c}")
        OpCodeGenerator.buf.append(op.value << 26 | c)
