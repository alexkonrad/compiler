from compiler.settings import REGISTER_ALLOCATION_TABLE_SIZE
from compiler.errors import RegisterAllocationError

class RegisterAllocationTable:
  table = range(32)
  idx = 1
  R0 = 0
  FP = 28
  SP = 29
  RBase = 30
  RReturn = 31

  @staticmethod
  def allocate_register() -> int:
    if RegisterAllocationTable.idx > REGISTER_ALLOCATION_TABLE_SIZE:
      raise RegisterAllocationError
    register = RegisterAllocationTable.idx
    RegisterAllocationTable.idx += 1
    while RegisterAllocationTable.idx in (
      RegisterAllocationTable.RBase,
      RegisterAllocationTable.SP,
      RegisterAllocationTable.FP,
      RegisterAllocationTable.RReturn
    ):
      RegisterAllocationTable.idx += 1
    return register

  @staticmethod
  def deallocate_register(reg: int):
    pass