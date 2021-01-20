# Compiler

Optimizing compiler for a simple programming language `smpl` emitting machine code for DLX (MIPS) architecture.

## Grammar

EBNF grammar for the `smpl` language below:

```
letter =  "a" | "b" | ... | "z".
digit =  "0" | "1" | ... | "9".
relOp  =  "==" | "!=" | "<" | "<=" | ">" | "=".
ident  =  letter {letter | digit}.
number  =  digit {digit}.
designator  = ident{ "[" expression "]" }.
factor  =  designator |  number  |  "(" expression ")"  | funcCall1.
term  =  factor { ("*" | "/") factor}.
expression  =  term {("+" | "-") term}.
relation  =  expression relOp expression .
assignment  =  "let" designator "<-" expression.
funcCall  =  "call" ident [2"(" [expression { "," expression } ] ")" ].
ifStatement  =  "if" relation "then" statSequence [ "else" statSequence ] "fi".
whileStatement  =  "while" relation "do" StatSequence "od".
returnStatement  =  "return" [ expression ].
statement  =  assignment | funcCall3| ifStatement | whileStatement | returnStatement.
statSequence  =  statement { ";" statement }[ ";"]4.
typeDecl  =  "var" | "array" "[" number "]" { "[" number "]" }.
varDecl  =  typeDecl indent { "," ident } ";".
funcDecl  =  [ "void" ] "function" ident formalParam ";" funcBody ";".
formalParam  = "(" [ident { "," ident }] ")".
funcBody  =  { varDecl } "{" [ statSequence ] "}".
computation  =  "main" { varDecl } { funcDecl } "{" statSequence "}" "."
```

## TODO

- [ ] a compiler using the register set as a stack
- [ ] a sophisticated compiler propagating state up and down the parse tree
- [ ] static single assignment
- [ ] static single assignment while parsing
- [ ] common subexpression elimination
- [ ] aliasing with arrays
- [ ] register allocation
- [ ] instruction scheduling
- [ ] trace scheduling
- [ ] trace based just-in-time compilation
- [ ] object-oriented language features
- [ ] implementing functions
