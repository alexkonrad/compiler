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
  SUB = 1
  MUL = 2
  DIV = 3
  ADDI = 16
  SUBI = 17
  MULI = 18
  DIVI = 19
  LDW = 32

  @property
  def immediate(self):
    return OpCode(self.value + 16)

  @staticmethod
  def from_symbol(sym):
    return {
      "+": OpCode.ADD,
      "-": OpCode.SUB,
      "*": OpCode.MUL,
      "/": OpCode.DIV
    }[sym]