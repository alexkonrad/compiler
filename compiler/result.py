from dataclasses import dataclass
from typing import Optional

from compiler.kind import Kind


@dataclass
class Result:
  kind: Kind
  val: int = 0
  addr: int = 0
  r: int = 0


def ConstantResult():
  return Result(kind=Kind.CONSTANT)

def VariableResult():
  return Result(kind=Kind.VARIABLE)