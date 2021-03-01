from compiler.kind import Kind
from compiler.opcode import OpCode
from compiler.register_allocation_table import RegisterAllocationTable as RegTable
from compiler.result import Result
from compiler.opcode_generator import OpCodeGenerator as OpCodeGen

class RegisterMachine:
  @staticmethod
  def compute(op: OpCode, x: Result, y: Result):
    if x.kind is Kind.CONSTANT and y.kind is Kind.CONSTANT:
      if op is OpCode.ADD:
        x.val += y.val
      elif op is OpCode.MUL:
        x.val *= y.val
    else:
      RegisterMachine.load(x)
      if y.kind is Kind.CONSTANT:
        OpCodeGen.put_f1(op.immediate, x.r, y.r, y.val)
      else:
        RegisterMachine.load(y)
      OpCodeGen.put_f1(op, x.r, x.r, y.r)
      RegTable.deallocate_register(y.r)

  @staticmethod
  def load(x: Result):
    if x.kind is Kind.CONSTANT:
      if x.val == 0:
        x.r = 0
      else:
        x.r = RegTable.allocate_register()
        OpCodeGen.put_f1(OpCode.ADDI, x.r, RegTable.R0, x.val)
      x.kind = Kind.REGISTER
    elif x.kind is Kind.VARIABLE:
      x.r = RegTable.allocate_register()
      OpCodeGen.put_f2(OpCode.LDW, x.r, RegTable.RBase, x.addr)
      x.kind = Kind.REGISTER





