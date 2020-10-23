http://craftinginterpreters.com/statements-and-state.html#block-syntax-and-semantics
statement      → exprStmt
               | printStmt
               | block ;

block          → "{" declaration* "}" ;


http://craftinginterpreters.com/statements-and-state.html#assignment-syntax
expression     → assignment ;
assignment     → IDENTIFIER "=" assignment
               | equality ;

http://craftinginterpreters.com/statements-and-state.html#variable-syntax
program        → declaration* EOF ;

declaration    → varDecl
               | statement ;

statement      → exprStmt
               | printStmt ;

varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;

primary        → "true" | "false" | "nil"
               | NUMBER | STRING
               | "(" expression ")"
               | IDENTIFIER ;

http://craftinginterpreters.com/statements-and-state.html#statements
program        → statement* EOF ;

statement      → exprStmt
               | printStmt ;

exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;

http://craftinginterpreters.com/representing-code.html#a-grammar-for-lox-expressions
expression     → literal
               | unary
               | binary
               | grouping ;

literal        → NUMBER | STRING | "true" | "false" | "nil" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
               | "+"  | "-"  | "*" | "/" ;

