from compiler.parser import Parser
from compiler.symbol_table import SymbolTable
from compiler.opcode_generator import OpCodeGenerator
from dlx import DLX
if __name__ == '__main__':
    # Parser.compile("1+2*(3+4)")
    SymbolTable.symbol_table["a"] = 3
    SymbolTable.symbol_table["b"] = 4
    Parser.compile("a+b*(3+4)")
    buf = OpCodeGenerator.buf
    DLX.load(buf)
    DLX.execute()

