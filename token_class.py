from token_type import TokenType


# TODO: this is a good candidate for namedtuple
class Token:
    ttype: TokenType
    lexeme: str
    literal: object
    line: int = 0

    def __init__(self, t: TokenType, lexeme: str, literal: object, line: int):
        self.ttype = t
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"{self.ttype:<22}:\t{self.lexeme}\t{self.literal}\t{self.line}"
