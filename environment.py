from __future__ import annotations
from dataclasses import dataclass

import mobject as obj

@dataclass
class Environment:
    store: dict[str, obj.Object]
    outer: Environment

    def __init__(self, store=None, outer=None):
        self.store = store or dict()
        self.outer = outer

    def get(self, key):
        value = self.store.get(key)
        if not value and self.outer:
            value = self.outer.get(key)
        
        return value
    
    def put(self, key, value):
        self.store[key] = value
        return value