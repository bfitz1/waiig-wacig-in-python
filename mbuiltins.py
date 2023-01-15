# Python doesn't like `builtins` as a module name, either
import evaluator
import mobject as obj

def builtin_len(*args):
    match args:
        case [obj.String(value)]:
            return obj.Integer(len(value))
        case [x]:
            return obj.Error(f"argument to `len` not supported, got {obj.typeof(x)}")
        case _:
            return obj.Error(f"wrong number of arguments; got {len(args)} but wanted 1")

builtinfns = {
    "len": obj.Builtin(builtin_len)
}