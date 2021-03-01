from dataclasses import dataclass
from enum import Enum, auto

# class Fmt(Enum):
#   F1 = "f1"
#   F2 = "f2"
#   F3 = "f3"
#
# @dataclass
# class OpCode2:
#   fmt: Fmt
#   opcode: int
#
# Add = OpCode2(Fmt.F2, 0)
# Mul = OpCode2(Fmt.F2, 2)
#
# AddI = OpCode2(Fmt.F1, 16)

class OpCode(Enum):
  ADD = 0
  MUL = 2
  ADDI = 16
  MULI = 18
  LDW = 32

  @property
  def immediate(self):
    return OpCode(self.value + 16)