from dataclasses import dataclass

from compiler.opcode import SSAOpCode


@dataclass
class Instruction:
  pc: int
  opcode: SSAOpCode
  x: int
  y: int