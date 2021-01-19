from contextlib import contextmanager

class PErr(Exception):
    pass

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
    @contextmanager
    def zero_or_one():
        pc = P.pc
        try:
            yield
        except PErr:
            P.pc = pc
            P.sym = P.txt[pc]

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
        raise PErr



    @staticmethod
    def consume(chars):
        for char in chars:
            if P.sym != char:
                P.error()
            P.next()

    @staticmethod
    def isletter():
        return P.sym.isalpha()

    @staticmethod
    def isdigit():
        return P.sym.isdigit()

    @staticmethod
    def relop():
        chars = P.sym + P.peek()
        if chars in ("==", "!=", "<=", ">="):
            P.next()
            P.next()
        elif P.sym in ("<", ">"):
            P.next()

    @staticmethod
    def ident():
        if not P.isletter():
            P.error()
        id = P.sym
        P.next()
        while P.isletter() or P.isdigit():
            id += P.sym
            P.next()
        return id

    @staticmethod
    def number():
        if not P.isdigit():
            P.error()
        v = int(P.sym)
        P.next()
        while P.isdigit():
            v = 10 * v + int(P.sym)
            P.next()
        return v

    @staticmethod
    def designator():
        id = P.ident()
        while P.sym == '[':
            P.next()
            P.expression()
            P.consume(']')
            # do something
        return id

    @staticmethod
    def factor():
        if P.sym == '(':
            P.next()
            P.expression()
            P.consume(')')
        elif P.isdigit():
            v = P.number()
        elif P.isletter():
            id = P.designator()
        else:
            P.error()

    @staticmethod
    def term():
        P.factor()
        while P.sym in ("*", "/"):
            P.next()
            P.factor()


    @staticmethod
    def expression():
        P.term()
        while P.sym in ("+", "-"):
            P.next()
            P.term()

    @staticmethod
    def relation():
        P.expression()
        P.relop()
        P.expression()

    @staticmethod
    def assignment():
        P.consume("let")
        P.designator()
        P.consume("<-")
        P.expression()

    @staticmethod
    def func_call():
        P.consume("call")
        P.ident()
        if P.sym == "(":
            P.next()
            with P.zero_or_one():
                P.expression()
                while P.sym == ",":
                    P.consume(",")
                    P.expression()
            P.consume(")")

    @staticmethod
    def if_statement():
        P.consume("if")
        P.relop()
        P.consume("then")
        P.stat_sequence()
        with P.zero_or_one():
            P.consume("else")
            P.stat_sequence()
        P.consume("fi")

    @staticmethod
    def while_statement():
        P.consume("while")
        P.relop()
        P.consume("do")
        P.stat_sequence()
        P.consume("od")

    @staticmethod
    def return_statement():
        P.consume("return")
        with P.zero_or_one():
            P.expression()

    @staticmethod
    def statement():
        # Maybe instead just do P.sym == "l" "c" "i" "w" "r"
        with P.zero_or_one():
            P.assignment()
            return
        with P.zero_or_one():
            P.func_call()
            return
        with P.zero_or_one():
            P.if_statement()
            return
        with P.zero_or_one():
            P.while_statement()
            return
        with P.zero_or_one():
            P.return_statement()
            return

    @staticmethod
    def stat_sequence():
        P.statement()
        while P.sym == ";":
            P.consume(";")
            P.statement()

    @staticmethod
    def type_decl():
        pass

    @staticmethod
    def var_decl():
        pass

    @staticmethod
    def func_decl():
        pass

    @staticmethod
    def formal_param():
        pass

    @staticmethod
    def func_body():
        pass

    @staticmethod
    def computation():
        pass

    # @staticmethod
    # def e():
    #     P.t()
    #     while P.sym == '+':
    #         P.next()
    #         P.t()
    #
    # @staticmethod
    # def t():
    #     P.f()
    #     while P.sym == '*':
    #         P.next()
    #         P.f()
    #
    # @staticmethod
    # def f():
    #     if P.sym == '(':
    #         P.next()
    #         P.e()
    #         if P.sym == ')':
    #             P.next()
    #     elif P.sym.isdigit():
    #         P.next()
    #         while P.sym.isdigit():
    #             P.next()
    #     else:
    #         P.error()


if __name__ == '__main__':
    P.compile("1+2*(3+4)")