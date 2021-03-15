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

class SSAOpCode(Enum):
  Add = auto()
  Sub = auto()
  Mul = auto()
  Div = auto()
  Const = auto()
  Cmp = auto()

  # Empty
  Empty = auto()

  # Control instructions
  Bra = auto()
  Beq = auto()
  Bne = auto()
  Blt = auto()
  Bge = auto()
  Ble = auto()
  Bgt = auto()

  # IO instructions
  Read = auto()
  Write = auto()
  WriteNL = auto()

  @staticmethod
  def from_relop(sym):
    return {
      "==": SSAOpCode.Bne,
      "!=": SSAOpCode.Beq,
      "<": SSAOpCode.Bge,
      "<=": SSAOpCode.Bgt,
      ">": SSAOpCode.Ble,
      ">=": SSAOpCode.Blt
    }[sym]



class OpCode(Enum):
  ADD = 0
  SUB = 1
  MUL = 2
  DIV = 3
  CONST = 99

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