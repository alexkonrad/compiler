from collections import defaultdict

class SymbolTable:
  # symbol_table = {}
  symbol_table = defaultdict(int)
  @staticmethod
  def lookup(addr):
    return SymbolTable.symbol_table[addr]