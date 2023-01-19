from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import typing

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
class Builtin:
    fn: typing.Any

@dataclass
class Array:
    elements: list[Object]

@dataclass(eq=True, frozen=True)
class HashKey:
    type: str
    value: int

@dataclass
class HashPair:
    key: Object
    value: Object

    def __iter__(self):
        yield self.key, self.value

@dataclass
class Hash:
    pairs: dict[HashKey, HashPair]

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
        case Builtin(_):
            return "builtin function"
        case Array(elements):
            ele = ", ".join(str(e) for e in elements)
            return f"[{ele}]"
        case Hash(pairs):
            p = ", ".join(f"{inspect(x.key)!r}:{inspect(x.value)!r}" for x in pairs.values())
            return f"{{ {p} }}"
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
        case Builtin(_):
            return "BUILTIN"
        case Array(_):
            return "ARRAY"
        case Hash(_):
            return "HASH"
        case Null():
            return "NULL"
        case ReturnValue(_):
            return "RETURN_VALUE"
        case Error(_):
            return "ERROR"

def hash_key(obj):
    match obj:
        case Boolean(_) | Integer(_) | String(_):
            return HashKey(typeof(obj), hash(obj.value))
        case _:
            return None