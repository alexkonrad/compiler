from compiler.errors import ParseError
from compiler.result import Result, ConstantResult, VariableResult
from compiler.symbol_table import SymbolTable
from compiler.register_machine import RegisterMachine
from compiler.opcode import OpCode

class Parser:
    sym = str()
    txt = str()
    pc = int()

    @staticmethod
    def compile(program):
        Parser.txt = program
        Parser.next()
        Parser.expression()

    @staticmethod
    def next():
        try:
            Parser.sym = Parser.txt[Parser.pc]
            Parser.pc += 1
        except IndexError:
            print("Done.")

    @staticmethod
    def peek():
        try:
            return Parser.txt[Parser.pc]
        except IndexError:
            return ""

    @staticmethod
    def error():
        raise ParseError

    @staticmethod
    def end_of_line():
        while Parser.sym.isspace():
            Parser.next()
        return Parser.sym == '\n'

    @staticmethod
    def consume(chars):
        for char in chars:
            if Parser.sym != char:
                Parser.error()
            Parser.next()

    @staticmethod
    def isletter():
        return Parser.sym.isalpha()

    @staticmethod
    def isdigit():
        return Parser.sym.isdigit()

    @staticmethod
    def relop():
        chars = Parser.sym + Parser.peek()
        if chars in ("==", "!=", "<=", ">="):
            Parser.next()
            Parser.next()
        elif Parser.sym in ("<", ">"):
            Parser.next()

    @staticmethod
    def ident():
        if not Parser.isletter():
            Parser.error()
        id = Parser.sym
        Parser.next()
        while Parser.isletter() or Parser.isdigit():
            id += Parser.sym
            Parser.next()
        return id

    @staticmethod
    def number():
        if not Parser.isdigit():
            Parser.error()
        v = int(Parser.sym)
        Parser.next()
        while Parser.isdigit():
            v = 10 * v + int(Parser.sym)
            Parser.next()
        return v

    @staticmethod
    def designator():
        id = Parser.ident()
        while Parser.sym == '[':
            Parser.next()
            Parser.expression()
            Parser.consume(']')
            # do something
        return id

    @staticmethod
    def factor() -> Result:
        if Parser.sym == '(':
            Parser.next()
            x = Parser.expression()
            Parser.consume(')')
        elif Parser.isdigit():
            number = Parser.number()
            x = ConstantResult()
            x.val = number
        elif Parser.isletter():
            id = Parser.designator()
            addr = SymbolTable.lookup(id)
            x = VariableResult()
            x.addr = addr
        else:
            Parser.error()
        return x

    @staticmethod
    def term() -> Result:
        x = Parser.factor()
        while Parser.sym in ("*", "/"):
            Parser.next()
            y = Parser.factor()
            RegisterMachine.compute(OpCode.MUL, x, y)
        return x


    @staticmethod
    def expression() -> Result:
        x = Parser.term()
        while Parser.sym in ("+", "-"):
            Parser.next()
            y = Parser.term()
            RegisterMachine.compute(OpCode.ADD, x, y)
        return x

    @staticmethod
    def relation():
        Parser.expression()
        Parser.relop()
        Parser.expression()

    @staticmethod
    def assignment():
        Parser.consume("let")
        Parser.designator()
        Parser.consume("<-")
        Parser.expression()

    @staticmethod
    def func_call():
        Parser.consume("call")
        Parser.ident()
        if Parser.sym == "(":
            Parser.next()
            if Parser.sym == ")":
                Parser.next()
            else:
                Parser.expression()
                while Parser.sym == ",":
                    Parser.consume(",")
                    Parser.expression()

    @staticmethod
    def if_statement():
        Parser.consume("if")
        Parser.relop()
        Parser.consume("then")
        Parser.stat_sequence()
        if Parser.sym == "e":
            Parser.consume("else")
            Parser.stat_sequence()
        Parser.consume("fi")

    @staticmethod
    def while_statement():
        Parser.consume("while")
        Parser.relop()
        Parser.consume("do")
        Parser.stat_sequence()
        Parser.consume("od")

    @staticmethod
    def return_statement():
        Parser.consume("return")
        if not Parser.end_of_line():
            Parser.expression()

    @staticmethod
    def statement():
        if Parser.sym == "l":
            Parser.assignment()
        elif Parser.sym == "c":
            Parser.func_call()
        elif Parser.sym == "i":
            Parser.if_statement()
        elif Parser.sym == "w":
            Parser.while_statement()
        elif Parser.sym == "r":
            Parser.return_statement()
        else:
            Parser.error()

    @staticmethod
    def stat_sequence():
        Parser.statement()
        while Parser.sym == ";":
            Parser.consume(";")
            Parser.statement()

    @staticmethod
    def type_decl():
        if Parser.sym == "v":
            Parser.consume("var")
        elif Parser.sym == "a":
            Parser.consume("array")
            Parser.consume("[")
            Parser.number()
            Parser.consume("]")
            while Parser.sym == "[":
                Parser.consume("[")
                Parser.number()
                Parser.consume("]")
        else:
            Parser.error()

    @staticmethod
    def var_decl():
        Parser.type_decl()
        Parser.ident()
        while Parser.sym == ",":
            Parser.consume(",")
            Parser.ident()
        Parser.consume(";")

    @staticmethod
    def func_decl():
        if Parser.sym == "v":
            Parser.consume("void")
        Parser.consume("function")
        Parser.ident()
        Parser.formal_param()
        Parser.consume(";")
        Parser.func_body()
        Parser.consume(";")

    @staticmethod
    def formal_param():
        Parser.consume("(")
        Parser.ident()
        while Parser.sym == ",":
            Parser.consume(",")
            Parser.ident()
        Parser.consume(")")

    @staticmethod
    def func_body():
        while Parser.sym != "{":
            Parser.var_decl()
        Parser.consume("{")
        if Parser.sym != "}":
            Parser.stat_sequence()
        Parser.consume("}")

    @staticmethod
    def computation():
        Parser.consume("main")
        chars = Parser.sym + Parser.peek()
        while chars not in ('vo', 'fu'):
            Parser.var_decl()
        while Parser.sym != "{":
            Parser.func_decl()
        Parser.consume("{")
        Parser.stat_sequence()
        Parser.consume("}")