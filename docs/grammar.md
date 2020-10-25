http://craftinginterpreters.com/functions.html#return-statements
statement      → exprStmt
               | forStmt
               | ifStmt
               | printStmt
               | returnStmt
               | whileStmt
               | block ;

returnStmt     → "return" expression? ";" ;

http://craftinginterpreters.com/functions.html#function-declarations
declaration    → funDecl
               | varDecl
               | statement ;

funDecl        → "fun" function ;
function       → IDENTIFIER "(" parameters? ")" block ;

parameters     → IDENTIFIER ( "," IDENTIFIER )* ;

http://craftinginterpreters.com/functions.html
unary          → ( "!" | "-" ) unary | call ;
call           → primary ( "(" arguments? ")" )* ;

arguments      → expression ( "," expression )* ;

http://craftinginterpreters.com/control-flow.html#for-loops
statement      → exprStmt
               | forStmt
               | ifStmt
               | printStmt
               | whileStmt
               | block ;

forStmt        → "for" "(" ( varDecl | exprStmt | ";" )
                 expression? ";"
                 expression? ")" statement ;

http://craftinginterpreters.com/control-flow.html#while-loops
statement      → exprStmt
               | ifStmt
               | printStmt
               | whileStmt
               | block ;

whileStmt      → "while" "(" expression ")" statement ;

http://craftinginterpreters.com/control-flow.html#logical-operators
expression     → assignment ;
assignment     → identifier "=" assignment
               | logic_or ;
logic_or       → logic_and ( "or" logic_and )* ;
logic_and      → equality ( "and" equality )* ;

http://craftinginterpreters.com/control-flow.html#conditional-execution
statement      → exprStmt
               | ifStmt
               | printStmt
               | block ;

ifStmt         → "if" "(" expression ")" statement
               ( "else" statement )? ;

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

