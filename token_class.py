from dataclasses import dataclass

from token_type import TokenType


@dataclass(frozen=True)
class Token:
    ttype: TokenType
    lexeme: str
    literal: object
    line: int = 0

    def __repr__(self):
        return f"Token[{self.ttype}〔{self.lexeme}〕Lit:〔{self.literal}〕@{self.line}]"  # noqa: E501
