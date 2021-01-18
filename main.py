class P:
    sym = str()
    txt = str()
    pc = int()

    @staticmethod
    def compile(program):
        P.txt = program
        P.next()
        P.e()

    @staticmethod
    def next():
        try:
            P.sym = P.txt[P.pc]
            P.pc += 1
        except IndexError:
            print("Done.")

    @staticmethod
    def peek():
        try:
            return P.txt[P.pc]
        except IndexError:
            return ""

    @staticmethod
    def error():
        print("Error")

    @staticmethod
    def e():
        P.t()
        while P.sym == '+':
            P.next()
            P.t()

    @staticmethod
    def t():
        P.f()
        while P.sym == '*':
            P.next()
            P.f()

    @staticmethod
    def f():
        if P.sym == '(':
            P.next()
            P.e()
            if P.sym == ')':
                P.next()
        elif P.sym.isdigit():
            P.next()
            while P.sym.isdigit():
                P.next()
        else:
            P.error()


if __name__ == '__main__':
    P.compile("1+2*(3+4)")