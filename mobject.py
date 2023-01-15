from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

import mast as ast
import environment as env

@dataclass
class Integer:
    value: int

@dataclass
class String:
    value: str

@dataclass
class Boolean:
    value: bool

@dataclass
class Function:
    parameters: list[ast.Identifier]
    body: ast.BlockStatement
    env: env.Environment

@dataclass
class Null:
    def __repr__(self):
        return "Null"

@dataclass
class ReturnValue:
    value: Object

@dataclass
class Error:
    message: str

Object = Integer | Boolean | Function | Null

def inspect(obj):
    match obj:
        case Integer(x):
            return f"{x}"
        case String(x):
            return x
        case Boolean(x):
            return f"{x}".lower()
        case Function(parameters, body, env):
            params = [x.value for x in parameters]
            # Oh no, this is gonna look so bad
            return f"fn({','.join(params)}) {{\n{body}\n}}"
        case Null():
            return "null"
        case ReturnValue(x):
            return inspect(x)
        case Error(x):
            return f"ERROR: {x}"

def typeof(obj):
    match obj:
        case Integer(_):
            return "INTEGER"
        case String(_):
            return "STRING"
        case Boolean(_):
            return "BOOLEAN"
        case Function(_, _, _):
            return "FUNCTION"
        case Null():
            return "NULL"
        case ReturnValue(_):
            return "RETURN_VALUE"
        case Error(_):
            return "ERROR"