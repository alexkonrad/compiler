

buf = []
pc = 0

def put_f1(op, a, b, c):
    """
    Arguments:
        op: 6-bit opcode
        a: 5-bit argument (takes register number)
        b: 5-bit argument (takes register number)
        c: 5-bit argument (takes register number)

    """
    buf.append(op << 26 | a << 21 | b << 16 | c)

def put_f2(op, a, b, c):
    """
    Arguments:
        op: 6-bit opcode
        a: 5-bit argument (takes register number)
        b: 5-bit argument (takes register number)
        c: 5-bit argument (takes register number)
    """
    buf.append(op << 26 | a << 21 | b << 16 | c)

def put_f3(op, c):
    """
    Arguments:
        op: 6-bit opcode
        c:  26-bit argument
    """
    buf.append(op << 26 | a )
