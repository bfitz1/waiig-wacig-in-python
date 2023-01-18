from __future__ import annotations
from dataclasses import dataclass
from typing import Any

# Remark: This implementation bothers me, but I'm not sure how to fix it.
# - Plain classes mean a lot of boilerplate. I'd like to avoid that if possible.
# - Dataclasses are more compact, but writing type hints doesn't feel great.
# - Why not just stick to values (list, tuples and dicts)? I dunno, in too deep I guess.

@dataclass
class PrefixExpression:
    operator: str
    right: Any

@dataclass
class InfixExpression:
    left: Any
    operator: str
    right: Any

@dataclass
class BlockStatement:
    statements: Any

@dataclass
class IfExpression:
    condition: Any
    consequence: BlockStatement
    alternative: BlockStatement

@dataclass
class Identifier:
    value: str

@dataclass
class IntegerLiteral:
    value: int

@dataclass
class StringLiteral:
    value: str

@dataclass
class Boolean:
    value: bool

@dataclass
class FunctionLiteral:
    parameters: list[Identifier]
    body: BlockStatement

@dataclass
class ArrayLiteral:
    elements: list[Any]

    def __repr__(self):
        s = ", ".join(str(x) for x in self.elements)
        return f"[{s}]"

@dataclass
class IndexExpression:
    left: Any
    index: Any

    def __repr__(self):
        return f"({self.left}[{self.index}])"

@dataclass
class CallExpression:
    function: Identifier | FunctionLiteral
    arguments: list[Any]

@dataclass
class LetStatement:
    identifier: str
    expr: Any

@dataclass
class ReturnStatement:
    expr: Any

@dataclass
class ExpressionStatement:
    expr: Any

@dataclass
class Program:
    statements: list[Any]

    def __iter__(self):
        yield from self.statements
    
    def __repr__(self):
        return f"Program({self.statements})"