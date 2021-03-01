from enum import Enum


class Kind(Enum):
  CONSTANT = "constant"
  VARIABLE = "variable"
  REGISTER = "register"