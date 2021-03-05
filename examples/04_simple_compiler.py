"""
Simple compiler.


Grammar:
E -> T { "+" T }
T -> F { "*" F }
F -> "(" E ")" | N
N -> D { D }
I -> A { A | D }
D -> "0" | "1" | ... | "9"
A -> "a" | "b" | ... | "z"

Glossary:
E means "expression"
T means "term"
F means "factor"
-> means produce
quotes are for literals
| means either or
[] means 0 or 1 time
{} means repeated 0 or more times

"""

class Parser():

    def e(self):
        pass

