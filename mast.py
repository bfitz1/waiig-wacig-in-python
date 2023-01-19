from __future__ import annotations
from dataclasses import dataclass
from typing import Any

# Remark: This implementation bothers me, but I'm not sure how to fix it.
# - Plain classes mean a lot of boilerplate. I'd like to avoid that if possible.
# - Dataclasses are more compact, but writing type hints doesn't feel great.
# - Why not just stick to values (list, tuples and dicts)? I dunno, in too deep I guess.

@dataclass(eq=True, frozen=True)
class PrefixExpression:
    operator: str
    right: Any

    def __repr__(self):
        return f"({str(self.operator)}{str(self.right)})"

@dataclass(eq=True, frozen=True)
class InfixExpression:
    left: Any
    operator: str
    right: Any

    def __repr__(self):
        return f"({str(self.left)}{str(self.operator)}{str(self.right)})"

@dataclass(eq=True, frozen=True)
class BlockStatement:
    statements: Any

    def __repr__(self):
        s = "\n".join(str(x) for x in self.statements)
        return f"{{ {s} }}"

@dataclass(eq=True, frozen=True)
class IfExpression:
    condition: Any
    consequence: BlockStatement
    alternative: BlockStatement

    def __repr__(self):
        return f"if ({str(self.condition)}) {str(self.consequence)} else {str(self.alternative)}"

@dataclass(eq=True, frozen=True)
class Identifier:
    value: str

    def __repr__(self):
        return f"{self.value}"

@dataclass(eq=True, frozen=True)
class IntegerLiteral:
    value: int

    def __repr__(self):
        return f"{self.value}"

@dataclass(eq=True, frozen=True)
class StringLiteral:
    value: str

    def __repr__(self):
        return f"{self.value!r}"

@dataclass(eq=True, frozen=True)
class Boolean:
    value: bool

    def __repr__(self):
        return f"{str(self.value)}".lower()

@dataclass(eq=True, frozen=True)
class FunctionLiteral:
    parameters: list[Identifier]
    body: BlockStatement

    def __repr__(self):
        p = ", ".join(str(x) for x in parameters)
        return f"fn ({p}) {{ {str(self.body)} }}"

@dataclass(eq=True, frozen=True)
class ArrayLiteral:
    elements: list[Any]

    def __repr__(self):
        s = ", ".join(str(x) for x in self.elements)
        return f"[{s}]"

@dataclass(eq=True, frozen=True)
class HashLiteral:
    pairs: dict[Any, Any]
    
    def __repr__(self):
        s = ", ".join(f"{str(k)}:{str(v)}" for k, v in self.pairs.items())
        return f"{{{s}}}"

@dataclass(eq=True, frozen=True)
class IndexExpression:
    left: Any
    index: Any

    def __repr__(self):
        return f"({self.left}[{self.index}])"

@dataclass(eq=True, frozen=True)
class CallExpression:
    function: Identifier | FunctionLiteral
    arguments: list[Any]

    def __repr__(self):
        a = ", ".join(str(x) for x in arguments)
        return f"({str(self.function)})({a})"

@dataclass(eq=True, frozen=True)
class LetStatement:
    identifier: str
    expr: Any

    def __repr__(self):
        return f"let {str(self.identifier)} = {str(self.expr)};"

@dataclass(eq=True, frozen=True)
class ReturnStatement:
    expr: Any

    def __repr__(self):
        return f"return {str(self.expr)}"

@dataclass(eq=True, frozen=True)
class ExpressionStatement:
    expr: Any

    def __repr__(self):
        return f"{str(self.expr)};"

@dataclass(eq=True, frozen=True)
class Program:
    statements: list[Any]

    def __iter__(self):
        yield from self.statements
    
    def __repr__(self):
        return f"Program({self.statements})"