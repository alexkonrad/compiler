"""
Parser for math expressions.
From CS241 Lecture 1 with Michael Franz.
1 + 2 * (3 + 4)
-> means produce
quotes are for literals
| means either or
[] means 0 or 1 time
{} means repeated 0 or more times
E -> T { "+" T }
T -> F { "*" F }
F -> "(" E ")" | N
N -> D { D }
D -> "0" | "1" | ... | "9"
E means "expression"
T means "term"
F means "factor"
"""

from collections import deque
class Parser():
    def __init__(self, parse):
        self.parse_iter = iter(parse)
        self.next()
        self.e()

    def next(self):
        try:
            self.sym = next(self.parse_iter)
        except StopIteration:
            print("Done.")

    def error(self):
        print("Error.")

    def e(self):
        self.t()
        while self.sym == "+":
            self.next()
            self.t()

    def t(self):
        self.f()
        while self.sym == "*":
            self.next()
            self.f()

    def f(self):
        if self.sym == "(":
            self.next()
            self.e()
            if self.sym == ")":
                self.next()
        elif self.sym.isdigit():
            self.next()
            while self.sym == "1":
                self.next()
        else:
            self.error()

if __name__ == "__main__":
    Parser("1+2*(3+4)")
