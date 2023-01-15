from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    # Meta
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers and literals
    IDENT = "IDENT"
    INT = "INT"
    STRING = "STRING"

    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"
    LT = "<"
    GT = ">"
    EQ = "=="
    NOT_EQ = "!="
    
    # Delimiters
    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Keywords
    FUNCTION = "FUNCTION"
    LET = "LET"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"

@dataclass
class Token:
    type: TokenType
    text: str

    # For tuple unpacking
    def __iter__(self):
        yield self.type
        yield self.text

    def __repr__(self):
        return f"Token(tag={self.type.name}, text={self.text!r})"