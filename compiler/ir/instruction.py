from dataclasses import dataclass

from compiler.opcode import SSAOpCode


@dataclass
class Instruction:
  pc: int
  opcode: SSAOpCode
  x: int
  y: int
  label: str = None

  def __repr__(self):
    instr_str = f"{self.pc}: {self.opcode.name.lower()}"
    # if self.x:
    if type(self.x) is Instruction:
      instr_str += f" ({self.x.pc})"
    elif self.x is not None:
      instr_str += f" #{self.x}"
    # if self.y:
    if type(self.y) is Instruction:
      instr_str += f" ({self.y.pc})"
    elif self.y is not None:
      instr_str += f" #{self.y}"
    return instr_str

  def branches_to(self, dest):
    if self.opcode is SSAOpCode.Bra:
      return self.x is dest
    elif SSAOpCode.is_branch(self.opcode):
      return self.y is dest
    return False

  def is_phi(self):
    return self.opcode is SSAOpCode.Phi

  def is_const(self):
    return self.opcode is SSAOpCode.Const
