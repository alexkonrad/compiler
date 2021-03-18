from dataclasses import dataclass

from compiler.ir.instruction import Instruction


@dataclass
class Assignment:
  label: str
  instr: Instruction