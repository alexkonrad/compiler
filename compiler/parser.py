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
            xi = InterRepr.add_const(number)
        elif Parser.isletter():
            ident = Parser.designator()
            xi = InterRepr.lookup(ident)
        else:
            Parser.error()
        return xi

    @staticmethod
    def term() -> int:
        xi = Parser.factor()
        Parser.indent()
        while Parser.sym in ("*", "/"):
            op = OpCode.from_symbol(Parser.sym)
            Parser.next()
            Parser.indent()
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
        yi = Parser.expression()
        branch_opcode = SSAOpCode.from_relop(relop)
        return xi, branch_opcode, yi

    @staticmethod
    def assignment():
        Parser.consume("let")
        ident = Parser.designator()
        Parser.consume("<-")
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
            # arg_instr = InterRepr.lookup(args[0])
            instr = InterRepr.add_instr(SSAOpCode.Write, args[0])
        else:
            instr = None
            # Add func_calls here
        return instr

    @staticmethod
    def if_statement():
        Parser.consume("if")
        ancst_blk = InterRepr.active_block
        join_blk = InterRepr.add_block()
        InterRepr.join_blks.append(join_blk)
        xi, relop, yi = Parser.relation()
        rel_instr = InterRepr.add_instr(SSAOpCode.Cmp, xi, yi)
        InterRepr.add_instr(relop, rel_instr, join_blk.entry_point)
        if_blk = InterRepr.add_block(parents=[ancst_blk], children=[join_blk])
        InterRepr.active_block = if_blk
        Parser.consume("then")
        Parser.stat_sequence()

        # Parse else block if there is one
        if Parser.sym == "e":

            InterRepr.add_instr(SSAOpCode.Bra, join_blk.entry_point)
            else_blk = InterRepr.add_block(parents=[ancst_blk], children=[join_blk])
            InterRepr.active_block = else_blk
            ancst_blk.exit_point.y = else_blk.entry_point

            Parser.consume("else")
            Parser.stat_sequence()

        # If there is no else block, attach join block to ancestor block
        else:
            join_blk.add_parent(ancst_blk)
        Parser.consume("fi")
        InterRepr.join_blks.pop()
        InterRepr.active_block = join_blk


    @staticmethod
    def while_statement():
        Parser.consume("while")
        ancst_blk = InterRepr.active_block
        cond_blk = InterRepr.add_block(parents=[ancst_blk])
        loop_blk = InterRepr.add_block(parents=[cond_blk])
        cont_blk = InterRepr.add_block(parents=[cond_blk])
        InterRepr.active_block = cond_blk
        xi, rel_op, yi = Parser.relation()
        rel_instr = InterRepr.add_instr(SSAOpCode.Cmp, xi, yi)
        InterRepr.add_instr(rel_op, rel_instr, cont_blk.entry_point)
        InterRepr.active_block = loop_blk
        InterRepr.join_blks.append(cond_blk)
        Parser.consume("do")
        Parser.stat_sequence()
        Parser.consume("od")
        InterRepr.join_blks.pop()
        InterRepr.add_instr(SSAOpCode.Bra, cond_blk.entry_point)
        InterRepr.active_blk = cont_blk

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