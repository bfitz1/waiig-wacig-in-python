# Python doesn't like `builtins` as a module name, either
import evaluator
import mobject as obj

def builtin_len(*args):
    match args:
        case [obj.Array(elements)]:
            return obj.Integer(len(elements))
        case [obj.String(value)]:
            return obj.Integer(len(value))
        case [x]:
            return obj.Error(f"argument to `len` not supported, got {obj.typeof(x)}")
        case _:
            return obj.Error(f"wrong number of arguments; got {len(args)} but wanted 1")

def first(*args):
    if len(args) != 1:
        return obj.Error(f"wrong number of arguments; got {len(args)} but wanted 1")
    
    if not isinstance(args[0], obj.Array):
        return obj.Error(f"argument to `first` must be ARRAY, got {typeof(args[0])}")
    
    array = args[0].elements
    if len(array) == 0:
        return evaluator.NULL
    
    return array[0]

def last(*args):
    if len(args) != 1:
        return obj.Error(f"wrong number of arguments; got {len(args)} but wanted 1")
    
    if not isinstance(args[0], obj.Array):
        return obj.Error(f"argument to `first` must be ARRAY, got {typeof(args[0])}")
    
    array = args[0].elements
    if len(array) == 0:
        return evaluator.NULL
    
    return array[-1]

def rest(*args):
    if len(args) != 1:
        return obj.Error(f"wrong number of arguments; got {len(args)} but wanted 1")
    
    if not isinstance(args[0], obj.Array):
        return obj.Error(f"argument to `first` must be ARRAY, got {typeof(args[0])}")
    
    array = args[0].elements
    if len(array) == 0:
        return evaluator.NULL
    
    return obj.Array(array[1:])

def push(*args):
    if len(args) != 2:
        return obj.Error(f"wrong number of arguments; got {len(args)} but wanted 2")
    
    if not isinstance(args[0], obj.Array):
        return obj.Error(f"argument to `first` must be ARRAY, got {typeof(args[0])}")
    
    array = args[0].elements[:]
    array.append(args[1])
    
    return obj.Array(array)

builtinfns = {
    "len": obj.Builtin(builtin_len),
    "first": obj.Builtin(first),
    "last": obj.Builtin(last),
    "rest": obj.Builtin(rest),
    "push": obj.Builtin(push),
}