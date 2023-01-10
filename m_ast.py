from typing import Any, NamedTuple

from tok import Tag

class Expression:
    pass

class PrefixExpression(NamedTuple):
    tag: Tag
    operator: str
    right: Expression

class InfixExpression(NamedTuple):
    tag: Tag
    left: Expression
    operator: str
    right: Expression

class BlockStatement(NamedTuple):
    tag: Tag
    statements: Any

class IfExpression(NamedTuple):
    tag: Tag
    condition: Expression
    consequence: BlockStatement
    alternative: BlockStatement

class Identifier(NamedTuple):
    tag: Tag
    value: str

class IntegerLiteral(NamedTuple):
    tag: Tag
    value: int

class FunctionLiteral(NamedTuple):
    tag: Tag
    parameters: list[Identifier]
    body: BlockStatement

class CallExpression(NamedTuple):
    tag: Tag
    function: Identifier | FunctionLiteral
    arguments: list[Expression]

class Boolean(NamedTuple):
    tag: Tag
    value: bool

class LetStatement(NamedTuple):
    tag: Tag
    identifier: str
    expr: Expression

class ReturnStatement(NamedTuple):
    tag: Tag
    expr: Expression

class ExpressionStatement(NamedTuple):
    tag: Tag
    expr: Any

class Program(NamedTuple):
    statements: list

    def __iter__(self):
        yield from self.statements