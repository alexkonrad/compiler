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

- [x] letter =  "a" | "b" | ... | "z".
- [x] digit =  "0" | "1" | ... | "9".
- [x] relOp  =  "==" | "!=" | "<" | "<=" | ">" | "=".
- [x] ident  =  letter {letter | digit}.
- [x] number  =  digit {digit}.
- [x] designator  = ident{ "[" expression "]" }.
- [x] factor  =  designator |  number  |  "(" expression ")"  | funcCall1.
- [x] term  =  factor { ("*" | "/") factor}.
- [x] expression  =  term {("+" | "-") term}.
- [x] relation  =  expression relOp expression .
- [x] assignment  =  "let" designator "<-" expression.
- [x] funcCall  =  "call" ident [2"(" [expression { "," expression } ] ")" ].
- [x] ifStatement  =  "if" relation "then" statSequence [ "else" statSequence ] "fi".
- [x] whileStatement  =  "while" relation "do" StatSequence "od".
- [x] returnStatement  =  "return" [ expression ].
- [x] statement  =  assignment | funcCall3| ifStatement | whileStatement | returnStatement.
- [x] statSequence  =  statement { ";" statement }[ ";"]4.
- [x] typeDecl  =  "var" | "array" "[" number "]" { "[" number "]" }.
- [x] varDecl  =  typeDecl indent { "," ident } ";".
- [x] funcDecl  =  [ "void" ] "function" ident formalParam ";" funcBody ";".
- [x] formalParam  = "(" [ident { "," ident }] ")".
- [x] funcBody  =  { varDecl } "{" [ statSequence ] "}".
- [ ] computation  =  "main" { varDecl } { funcDecl } "{" statSequence "}" "."


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
