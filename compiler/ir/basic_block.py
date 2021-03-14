from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from compiler.ir.assignment import Assignment
from compiler.ir.instruction import Instruction


@dataclass
class BasicBlock:
  children: List[BasicBlock] = field(default_factory=list)
  parents: List[BasicBlock] = field(default_factory=list)
  instructions: List[Instruction] = field(default_factory=list)
  assignments: List[Assignment] = field(default_factory=list)

  def add_parent(self, parent: BasicBlock):
    parent.children.append(self)
    self.parents.append(parent)

  def lookup(self, ident):
    for assignment in reversed(self.assignments):
      if assignment.label == ident:
        return assignment.index
    # for parent in self.parents:
    #   val = parent.get_assignment(ident)
    #   if val:
    #     return val
    return 0

  def add_assgn(self, ident, index):
    assgn = Assignment(ident, index)
    self.assignments.append(assgn)

  def add_instr(self, pc, op, a, b):
    instr = Instruction(pc, op, a, b)
    self.instructions.append(instr)
    return instr

  def fetch_instr(self, pc) -> Optional[Instruction]:
    for instr in self.instructions:
      if instr.pc == pc:
        return instr