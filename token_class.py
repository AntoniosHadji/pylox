from dataclasses import dataclass

from token_type import TokenType


@dataclass(frozen=True)
class Token:
    ttype: TokenType
    lexeme: str
    literal: object
    line: int = 0

    def __repr__(self):
        return f"{self.ttype:<22}:\t{self.lexeme}\t{self.literal}\t{self.line}"
