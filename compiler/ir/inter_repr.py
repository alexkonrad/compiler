from __future__ import annotations

from compiler.ir.basic_block import BasicBlock
from compiler.ir.instruction import Instruction
from compiler.opcode import SSAOpCode


class InterRepr:
  blks = []
  pc: int = 1

  @staticmethod
  def add_const(x: int, y: int):
    block = InterRepr.blks[-1]
    pc = InterRepr.pc
    instr = block.add_instr(pc, SSAOpCode.Const, x, y)
    InterRepr.pc += 1
    return instr

  @staticmethod
  def add_instr(op: SSAOpCode, x: Instruction = None, y: Instruction = None):
    block = InterRepr.blks[-1]
    if block.empty_instr():
      block.instructions.pop()
      InterRepr.pc -= 1
    pc = InterRepr.pc
    instr = block.add_instr(pc, op, x, y)
    InterRepr.pc += 1
    return instr

  @staticmethod
  def assign(ident, instr: int):
    block = InterRepr.blks[-1]
    block.add_assgn(ident, instr)

  @staticmethod
  def lookup(x):
    block = InterRepr.blks[-1]
    instr = block.lookup(x)
    return instr

  @staticmethod
  def fetch_instr(pc):
    for block in reversed(InterRepr.blks):
      instr = block.fetch_instr(pc)
      if instr:
        return instr

  @staticmethod
  def add_block():
    block = BasicBlock(len(InterRepr.blks)+1)
    InterRepr.blks.append(block)
    InterRepr.add_instr(SSAOpCode.Empty)
    return block

  @staticmethod
  def cfgraph():
    return f"""
      digraph G {{
        
      }}
    """

InterRepr.add_block()