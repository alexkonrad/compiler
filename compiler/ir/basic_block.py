from __future__ import annotations

from copy import copy
from dataclasses import dataclass, field
from typing import List, Optional

from compiler.ir.assignment import Assignment
from compiler.ir.instruction import Instruction
from compiler.opcode import SSAOpCode


@dataclass
class BasicBlock:
  idx: int
  children: List[BasicBlock] = field(default_factory=list)
  parents: List[BasicBlock] = field(default_factory=list)
  instructions: List[Instruction] = field(default_factory=list)
  assignments: List[Assignment] = field(default_factory=list)

  @property
  def entry_point(self):
    return self.instructions[0]

  @property
  def exit_point(self):
    return self.instructions[-1]

  def add_parent(self, parent: BasicBlock):
    parent.children.append(self)
    self.parents.append(parent)

  def local_lookup(self, ident):
    for assignment in self.assignments:
      if assignment.label == ident:
        return assignment.instr

  def lookup(self, ident):
    for assignment in self.assignments:
      if assignment.label == ident:
        return assignment.instr
    for parent in self.parents:
      val = parent.lookup(ident)
      if val != 0:
        return val
    return 0

  def add_assgn(self, ident, instr):
    assgn = Assignment(ident, instr)
    self.assignments = [a for a in self.assignments if a.label != assgn.label]
    self.assignments.append(assgn)
    if not instr.is_phi():
      return assgn
    self.push_forward_assgn(assgn)

    return assgn

  def push_forward_assgn(self, assgn: Assignment):
    for instr in self.instructions:
      if instr.is_phi():
        continue
      if isinstance(instr.x, Instruction):
        x_needs_replace = instr.x.label == assgn.label
        if x_needs_replace:
          instr.x = copy(assgn.instr)
      if isinstance(instr.y, Instruction):
        y_needs_replace = instr.y.label == assgn.label
        if y_needs_replace:
          instr.y = copy(assgn.instr)

  def add_instr(self, pc, op, a=None, b=None):
    if self.empty_instr():
      instr = self.instructions[0]
      instr.pc = pc
      instr.opcode = op
      instr.x = copy(a)
      instr.y = copy(b)
    else:
      instr = Instruction(pc, op, a, b)
      if instr.is_phi():
        self.instructions.insert(self.phi_index(), instr)
      else:
        self.instructions.append(instr)
    return instr

  def phi_index(self):
    idx = 0
    for i in range(len(self.instructions)):
      if self.instructions[i].opcode is not SSAOpCode.Phi:
        break
      idx += 1
    return idx

  def fetch_instr(self, pc) -> Optional[Instruction]:
    for instr in self.instructions:
      if instr.pc == pc:
        return instr

  def empty_instr(self) -> bool:
    if len(self.instructions) == 0:
      return False
    return self.instructions[-1].opcode is SSAOpCode.Empty

