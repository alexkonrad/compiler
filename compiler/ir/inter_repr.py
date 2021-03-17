from __future__ import annotations

from compiler.ir.basic_block import BasicBlock
from compiler.ir.instruction import Instruction
from compiler.opcode import SSAOpCode


class InterRepr:
  blks = []
  join_blks = []
  pc: int = 1

  @staticmethod
  def add_const(x: int):
    block = InterRepr.blks[-1]
    pc = InterRepr.pc
    instr = block.add_instr(pc, SSAOpCode.Const, x)
    InterRepr.pc += 1
    return instr

  @staticmethod
  def add_instr(op: SSAOpCode, x: Instruction = None, y: Instruction = None):
    blk = InterRepr.blks[-1]
    if blk.empty_instr():
      instr = blk.instructions[0]
      instr.opcode = op
      instr.x = x
      instr.y = y
    else:
      pc = InterRepr.pc
      instr = blk.add_instr(pc, op, x, y)
      InterRepr.pc += 1
    return instr

  @staticmethod
  def assign(ident, instr: int):
    block = InterRepr.blks[-1]
    phi_instr = InterRepr.lookup(ident)
    block.add_assgn(ident, instr)
    for join_blk in reversed(InterRepr.join_blks):
      for join_instr in join_blk.instructions:
        is_empty = join_instr.opcode is SSAOpCode.Empty
        is_phi = join_instr.opcode is SSAOpCode.Phi
        should_edit_phi = is_phi and (phi_instr is join_instr.x or phi_instr is join_instr.y)
        if is_empty or should_edit_phi:
          join_instr.opcode = SSAOpCode.Phi
          join_instr.x = instr
          join_instr.y = phi_instr
          break
      else:
        pc = InterRepr.pc
        instr = join_blk.add_instr(pc, SSAOpCode.Phi, instr, phi_instr)
        InterRepr.pc += 1

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
  def add_block(parents=None, children=None, join_block=False):
    if parents is None:
      parents = []
    if children is None:
      children = []

    blk = BasicBlock(len(InterRepr.blks)+1)
    blk.add_instr(InterRepr.pc, SSAOpCode.Empty)
    InterRepr.pc += 1

    if not join_block:
      InterRepr.blks.append(blk)
    else:
      InterRepr.join_blks.append(blk)

    for parent_blk in parents:
      blk.add_parent(parent_blk)
    for child_blk in children:
      child_blk.add_parent(blk)

    return blk

  @staticmethod
  def add_join_block(parents=None, children=None):
    return InterRepr.add_block(parents, children, join_block=True)

  @staticmethod
  def attach_join_block(blk: BasicBlock):
    InterRepr.join_blks.pop()
    blk.idx = len(InterRepr.blks) + 1
    InterRepr.blks.append(blk)


blk = InterRepr.add_block()