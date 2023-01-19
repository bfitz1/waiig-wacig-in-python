import mast as ast
import mobject as obj
from mobject import inspect, typeof
from environment import Environment
from mbuiltins import builtinfns

NULL = obj.Null()
TRUE = obj.Boolean(True)
FALSE = obj.Boolean(False)

def Eval(env, node):
    match node:
        case ast.Program(statements):
            return eval_program(env, statements)

        case ast.ReturnStatement(expr):
            eval_expr = Eval(env, expr)
            if is_error(eval_expr):
                return eval_expr

            return obj.ReturnValue(eval_expr)

        case ast.ExpressionStatement(expr):
            return Eval(env, expr)

        case ast.IntegerLiteral(value):
            return obj.Integer(value)

        case ast.StringLiteral(value):
            return obj.String(value)

        case ast.Boolean(value):
            return native_boolean_to_object(value)

        case ast.FunctionLiteral(parameters, body):
            return obj.Function(parameters, body, env)

        case ast.ArrayLiteral(elements):
            ele = eval_expressions(env, elements)

            if len(ele) == 1 and is_error(elements[0]):
                return elements[0]
            
            return obj.Array(ele)
        
        case ast.HashLiteral(_):
            return eval_hash_literal(env, node)
        
        case ast.IndexExpression(left, index):
            eval_left = Eval(env, left)
            if is_error(eval_left):
                return eval_left
            
            eval_index = Eval(env, index)
            if is_error(eval_index):
                return eval_index
            
            return eval_index_expression(eval_left, eval_index)
        
        case ast.CallExpression(function, arguments):
            fn = Eval(env, function)
            if is_error(fn):
                return fn
            
            args = eval_expressions(env, arguments)
            if len(args) == 1 and is_error(args[0]):
                return args[0]

            return apply_function(fn, args)

        case ast.PrefixExpression(operator, right):
            eval_right = Eval(env, right)
            if is_error(eval_right):
                return eval_right

            return eval_prefix_expression(operator, eval_right)

        case ast.InfixExpression(left, operator, right):
            eval_left = Eval(env, left)
            if is_error(eval_left):
                return eval_left

            eval_right = Eval(env, right)
            if is_error(eval_right):
                return eval_right

            return eval_infix_expression(operator, eval_left, eval_right)

        case ast.BlockStatement(statements):
            return eval_block_statement(env, statements)

        case ast.IfExpression(condition, consequence, alternative):
            return eval_if_expression(env, condition, consequence, alternative)

        case ast.LetStatement(identifier, expr):
            eval_expr = Eval(env, expr)
            if is_error(eval_expr):
                    return eval_expr

            env.put(identifier.value, eval_expr)
        
        case ast.Identifier(value):
            return eval_identifier(env, value)
    
    return None

def eval_program(env, statements):
    for s in statements:
        result = Eval(env, s)
        match result:
            case obj.ReturnValue(value):
                return value
            case obj.Error(_):
                return result     

    return result

def eval_block_statement(env, statements):
    for s in statements:
        result = Eval(env, s)
        if result and type(result) in { obj.ReturnValue, obj.Error }:
            return result

    return result

def eval_expressions(env, exprs):
    result = []
    for e in exprs:
        evaluated = Eval(env, e)
        if is_error(evaluated):
            return [evaluated]
        result.append(evaluated)
    
    return result

def apply_function(function, arguments):
    match function:
        case obj.Function(_, body, _):
            extended_env = extend_function_env(function, arguments)
            evaluated = Eval(extended_env, body)
            return unwrap_return_value(evaluated)
        case obj.Builtin(fn):
            return fn(*arguments)
        case _:
            return obj.Error(f"not a function: {typeof(function)}")

def extend_function_env(fn, args):
    env = Environment(outer=fn.env)
    for i, param in enumerate(fn.parameters):
        env.put(param.value, args[i])
    
    return env

def unwrap_return_value(ret):
    match ret:
        case obj.ReturnValue(x):
            return x
        case _:
            return ret
    
def eval_identifier(env, key):
    value = env.get(key)
    if value:
        return value
    
    builtin = builtinfns.get(key)
    if builtin:
        return builtin

    return obj.Error(f"identifier not found: {key}")

def eval_prefix_expression(operator, right):
    match operator:
        case "!":
            return eval_bang_operator_expression(right)
        case "-":
            return eval_minus_prefix_operator_expression(right)
        case _:
            return obj.Error(f"unknown operator: {operator}{right}")

def eval_infix_expression(operator, left, right):
    match (operator, left, right):
        case (_, obj.Integer(_), obj.Integer(_)):
            return eval_integer_infix_expression(operator, left, right)
        case (_, obj.String(_), obj.String(_)):
            return eval_string_infix_expression(operator, left, right)
        case (_, left, right) if typeof(left) != typeof(right):
            return obj.Error(f"type mismatch: {typeof(left)} {operator} {typeof(right)}")
        case ("==", _, _):
            return native_boolean_to_object(left == right)
        case ("!=", _, _):
            return native_boolean_to_object(left != right)
        case _:
            return obj.Error(f"unknown operator: {typeof(left)} {operator} {typeof(right)}")

def eval_bang_operator_expression(right):
    # Pattern matching doesn't work here ¯\_(ツ)_/¯
    if right == TRUE:
        return FALSE
    elif right == FALSE:
        return TRUE
    elif right == NULL:
        return TRUE
    else:
        return FALSE

def eval_minus_prefix_operator_expression(right):
    match right:
        case obj.Integer(value):
            return obj.Integer(-value)
        case _:
            return obj.Error(f"unknown operator: -{typeof(right)}")

def eval_integer_infix_expression(operator, left, right):
    leftval, rightval = left.value, right.value
    match operator:
        case "+":
            return obj.Integer(leftval + rightval)
        case "-":
            return obj.Integer(leftval - rightval)
        case "*":
            return obj.Integer(leftval * rightval)
        case "/":
            return obj.Integer(leftval // rightval)
        case "<":
            return native_boolean_to_object(leftval < rightval)
        case ">":
            return native_boolean_to_object(leftval > rightval)
        case "==":
            return native_boolean_to_object(leftval == rightval)
        case "!=":
            return native_boolean_to_object(leftval != rightval)
        case _:
            return obj.Error(f"unknown operator: {typeof(left)} {operator} {typeof(right)}")

def eval_string_infix_expression(operator, left, right):
    if operator != "+":
        return obj.Error(f"unknown operator: {typeof(left)} {operator} {typeof(right)}")
    
    leftval = left.value
    rightval = right.value
    return obj.String(leftval + rightval)

def eval_if_expression(env, condition, consequence, alternative):
    cond = Eval(env, condition)
    if is_error(cond):
        return cond

    if is_truthy(cond):
        return Eval(env, consequence)
    elif alternative:
        return Eval(env, alternative)
    else:
        return NULL

def eval_index_expression(left, index):
    match (left, index):
        case (obj.Array(_), obj.Integer(_)):
            return eval_array_index_expression(left, index)
        case (obj.Hash(_), _):
            return eval_hash_index_expression(left, index)
        case _:
            return obj.Error(f"index operator not supported: {typeof(left)}")

def eval_array_index_expression(left, index):
    maxindex = len(left.elements)
    if index.value < 0 or index.value >= maxindex:
        return NULL
    
    return left.elements[index.value]

def eval_hash_index_expression(left, index):
    key = obj.hash_key(index)
    if not key:
        return obj.Error(f"unusable as hash key: {typeof(index)}")
    
    pair = left.pairs.get(key, NULL)
    if pair == NULL:
        return NULL
        
    return pair.value

def eval_hash_literal(env, node):
    pairs = dict()
    for keynode, valuenode in node.pairs.items():
        key = Eval(env, keynode)
        if is_error(key):
            return key
        
        hashkey = obj.hash_key(key)
        if not hashkey:
            return obj.Error(f"unusable as a hash key: {typeof(key)}")
        
        value = Eval(env, valuenode)
        if is_error(value):
            return value
        
        pairs[hashkey] = obj.HashPair(key, value)
    
    return obj.Hash(pairs)


def native_boolean_to_object(boolean):
    return TRUE if boolean else FALSE

def is_truthy(x):
    if x == NULL or x == FALSE:
        return False
    else:
        return True

def is_error(x):
    if x:
        return type(x) == obj.Error
    else:
        return False