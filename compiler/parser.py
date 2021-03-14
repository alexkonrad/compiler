from compiler.errors import ParseError
from compiler.result import Result, ConstantResult, VariableResult
from compiler.symbol_table import SymbolTable
from compiler.register_machine import RegisterMachine
from compiler.opcode import OpCode, SSAOpCode
from compiler.ir.inter_repr import InterRepr

class Parser:
    sym = str()
    txt = str()
    pc = int()

    @staticmethod
    def compile(program):
        Parser.txt = program
        Parser.next()
        # Parser.stat_sequence()
        # Parser.expression()
        Parser.computation()

    @staticmethod
    def next():
        try:
            Parser.sym = Parser.txt[Parser.pc]
            Parser.pc += 1
        except IndexError:
            print("Done.")
        print(Parser.sym,end="")
        if Parser.sym == "\n":
            Parser.next()


    @staticmethod
    def indent():
        while Parser.sym == " ":
            Parser.next()

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
        Parser.indent()
        for char in chars:
            if Parser.sym != char:
                Parser.error()
            Parser.next()
        Parser.indent()

    @staticmethod
    def space():
        while Parser.sym.isspace():
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
            chars = Parser.sym
            Parser.next()
        else:
            Parser.error()
        return chars

    @staticmethod
    def ident():
        # Parser.indent()
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
        Parser.indent()
        try:
            lookahead = Parser.sym + Parser.txt[Parser.pc:Parser.pc+3]
            if lookahead == "call":
                xi = Parser.func_call()
                return xi
        except IndexError:
            pass
        if Parser.sym == '(':
            Parser.next()
            xi = Parser.expression()
            Parser.consume(')')
        elif Parser.isdigit():
            number = Parser.number()
            xi = InterRepr.add_const(number, 0)
        elif Parser.isletter():
            ident = Parser.designator()
            xi = InterRepr.lookup(ident)
        else:
            Parser.error()
        return xi

    @staticmethod
    def term() -> int:
        xi = Parser.factor()
        while Parser.sym in ("*", "/"):
            op = OpCode.from_symbol(Parser.sym)
            Parser.next()
            yi = Parser.factor()
            xi = InterRepr.add_instr(op, xi, yi)
        return xi


    @staticmethod
    def expression() -> int:
        xi = Parser.term()
        Parser.indent()
        while Parser.sym in ("+", "-"):
            op = OpCode.from_symbol(Parser.sym)
            Parser.next()
            Parser.indent()
            yi = Parser.term()
            xi = InterRepr.add_instr(op, xi, yi)
        return xi

    @staticmethod
    def relation():
        xi = Parser.expression()
        relop = Parser.relop()
        branch_opcode = SSAOpCode.from_relop(relop)
        yi = Parser.expression()
        instr = InterRepr.add_instr(SSAOpCode.Cmp, xi, yi)
        return instr, branch_opcode

    @staticmethod
    def assignment():
        Parser.consume("let")
        ident = Parser.designator()
        Parser.indent()
        Parser.consume("<-")
        Parser.indent()
        expr_instr = Parser.expression()
        InterRepr.assign(ident, expr_instr)

    @staticmethod
    def func_call():
        Parser.consume("call")
        ident = Parser.ident()
        Parser.consume("(")
        args = []
        if Parser.sym == ")":
            Parser.next()
        else:
            args.append(Parser.expression())
            while Parser.sym == ",":
                Parser.consume(",")
                args.append(Parser.expression())
            Parser.consume(")")
        if ident == "inputNum" and len(args) == 0:
            instr = InterRepr.add_instr(SSAOpCode.Read)
        elif ident == "outputNum" and len(args) == 1:
            arg_instr = InterRepr.lookup(args[0])
            instr = InterRepr.add_instr(SSAOpCode.Write, arg_instr)
        else:
            instr = None
            # Add func_calls here
        return instr

    @staticmethod
    def if_statement():
        Parser.consume("if")
        # Parser.indent()
        rel_instr, branch_opcode = Parser.relation()
        branch_instr = InterRepr.add_instr(branch_opcode, rel_instr, 0)
        Parser.consume("then")
        parent_block = InterRepr.blks[-1]
        if_block = InterRepr.add_block()
        if_block.add_parent(parent_block)
        Parser.stat_sequence()
        has_else_block = False
        if Parser.sym == "e":
            has_else_block = True
            Parser.consume("else")
            branch_back_instr = InterRepr.add_instr(SSAOpCode.Bra, 0)
            else_block = InterRepr.add_block()
            else_block.add_parent(parent_block)
            branch_instr.y = InterRepr.pc + 1
            Parser.stat_sequence()
        Parser.consume("fi")
        after_block = InterRepr.add_block()
        after_block.add_parent(if_block)
        if has_else_block:
            after_block.add_parent(else_block)
            branch_back_instr.y = InterRepr.pc + 1
        else:
            after_block.add_parent(parent_block)
            branch_instr.y = InterRepr.pc + 1


    @staticmethod
    def while_statement():
        Parser.consume("while")
        relop = Parser.relation()
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
        # Parser.indent()
        Parser.ident()
        while Parser.sym == ",":
            Parser.consume(",")
            # Parser.indent()
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
        while Parser.sym != "{" and chars not in ('vo', 'fu'):
            Parser.var_decl()
        while Parser.sym != "{":
            Parser.func_decl()
        Parser.consume("{")
        Parser.stat_sequence()
        Parser.consume("}")