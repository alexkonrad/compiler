from __future__ import annotations
from typing import List
from dataclasses import dataclass, field

from compiler.opcode import OpCode

class IntrRepr:
  blks = []

  @staticmethod
  def compute(op: OpCode, x: Result, y: Result):
    if len(IntrRepr.blks) == 0:
      IntrRepr.blks
    # Create an instruction
    instr = Instruction(op, x, y)

    # Create an assignment
    assgn = Assignment()

@dataclass
class Instruction:
  opcode: OpCode
  x: Result
  y: Result

@dataclass
class Assignment:
  label: str
  index: int

@dataclass
class BasicBlock:
  pc: int
  child: BasicBlock = None
  parents: List[BasicBlock] = field(default_factory=list)
  instructions: List[Instruction] = field(default_factory=list)
  assignments: List[Assignment] = field(default_factory=list)