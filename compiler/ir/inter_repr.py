from __future__ import annotations
from copy import copy

from compiler.ir.basic_block import BasicBlock
from compiler.ir.instruction import Instruction
from compiler.opcode import SSAOpCode


class InterRepr:
  active_block: BasicBlock = None
  root_block: BasicBlock = None
  num_blks: int = 1
  join_blks = []
  pc: int = 1

  @staticmethod
  def add_const(x: int):
    block = InterRepr.active_block
    pc = InterRepr.pc
    instr = block.add_instr(pc, SSAOpCode.Const, x)
    InterRepr.pc += 1
    return instr

  @staticmethod
  def add_instr(op: SSAOpCode, x: Instruction = None, y: Instruction = None):
    blk = InterRepr.active_block
    pc = InterRepr.pc
    instr = blk.add_instr(pc, op, x, y)
    InterRepr.pc += 1
    return instr

  @staticmethod
  def assign(ident, instr: int):
    block = InterRepr.active_block
    old_instr = InterRepr.lookup(ident)
    block.add_assgn(ident, instr)
    for join_blk in reversed(InterRepr.join_blks):
      phi_instr = join_blk.local_lookup(ident)
      if phi_instr:
        if phi_instr.x == old_instr:
          phi_instr.x = instr
        elif phi_instr.y == old_instr:
          phi_instr.y = instr
      else:
        pc = InterRepr.pc
        instr = join_blk.add_instr(pc, SSAOpCode.Phi, instr, old_instr)
        join_blk.add_assgn(ident, instr)
        InterRepr.pc += 1

  @staticmethod
  def lookup(x):
    block = InterRepr.active_block
    instr = block.lookup(x)
    if instr:
      instr = copy(instr)
      instr.label = x
    return instr

  @staticmethod
  def add_block(parents=None, children=None):
    if parents is None:
      parents = []
    if children is None:
      children = []

    blk = BasicBlock(InterRepr.num_blks)
    blk.add_instr(InterRepr.pc, SSAOpCode.Empty)
    InterRepr.pc += 1
    InterRepr.num_blks += 1

    for parent_blk in parents:
      blk.add_parent(parent_blk)
    for child_blk in children:
      child_blk.add_parent(blk)

    return blk


blk = InterRepr.add_block()
InterRepr.active_block = blk
InterRepr.root_block = blk