import unittest

import mast as ast
import mobject as obj
from lexer import lex
from evaluator import Eval
from parser import parse
from environment import Environment

class Test_Eval(unittest.TestCase):
    def test_eval_integer_expression(self):
        tests = [
            ("5", obj.Integer(5)),
            ("10", obj.Integer(10)),
            ("-5", obj.Integer(-5)),
            ("-10", obj.Integer(-10)),
            ("5 + 5 + 5 + 5 - 10", obj.Integer(10)),
            ("2 * 2 * 2 * 2 * 2", obj.Integer(32)),
            ("-50 + 100 + -50", obj.Integer(0)),
            ("5 * 2 + 10", obj.Integer(20)),
            ("5 + 2 * 10", obj.Integer(25)),
            ("20 + 2 * -10", obj.Integer(0)),
            ("50 / 2 * 2 + 10", obj.Integer(60)),
            ("2 * (5 + 10)", obj.Integer(30)),
            ("3 * 3 * 3 + 10", obj.Integer(37)),
            ("3 * (3 * 3) + 10", obj.Integer(37)),
            ("(5 + 10 * 2 + 15 / 3) * 2 + -10", obj.Integer(50)),
        ]

        for i, (sample, expected) in enumerate(tests):
            returned = Eval(Environment(), parse(sample))
            self.assertEqual(returned, expected, f"tests[{i}]: expected {expected}, got {returned}")
    
    def test_eval_boolean_expression(self):
        tests = [
            ("true", obj.Boolean(True)),
            ("false", obj.Boolean(False)),
            ("1 < 2", obj.Boolean(True)),
            ("1 > 2", obj.Boolean(False)),
            ("1 < 1", obj.Boolean(False)),
            ("1 > 1", obj.Boolean(False)),
            ("1 == 1", obj.Boolean(True)),
            ("1 != 1", obj.Boolean(False)),
            ("1 == 2", obj.Boolean(False)),
            ("1 != 2", obj.Boolean(True)),
            ("true == true", obj.Boolean(True)),
            ("false == false", obj.Boolean(True)),
            ("true == false", obj.Boolean(False)),
            ("true != false", obj.Boolean(True)),
            ("false != true", obj.Boolean(True)),
            ("(1 < 2) == true", obj.Boolean(True)),
            ("(1 < 2) == false", obj.Boolean(False)),
            ("(1 > 2) == true", obj.Boolean(False)),
            ("(1 > 2) == false", obj.Boolean(True)),
        ]

        for i, (sample, expected) in enumerate(tests):
            returned = Eval(Environment(), parse(sample))
            self.assertEqual(returned, expected, f"tests[{i}]: expected {expected}, got {returned}")
    
    def test_bang_operator(self):
        tests = [
            ("!true", obj.Boolean(False)),
            ("!false", obj.Boolean(True)),
            ("!5", obj.Boolean(False)),
            ("!!true", obj.Boolean(True)),
            ("!!false", obj.Boolean(False)),
            ("!!5", obj.Boolean(True)),
        ]

        for sample, expected in tests:
            returned = Eval(Environment(), parse(sample))
            self.assertEqual(returned, expected, f"Expected {expected}, got {returned}")
    
    def test_if_else_expression(self):
        tests = [
            ("if (true) { 10 }", obj.Integer(10)),
            ("if (false) { 10 }", obj.Null()),
            ("if (1) { 10 }", obj.Integer(10)),
            ("if (1 < 2) { 10 }", obj.Integer(10)),
            ("if (1 > 2) { 10 }", obj.Null()),
            ("if (1 > 2) { 10 } else { 20 }", obj.Integer(20)),
            ("if (1 < 2) { 10 } else { 20 }", obj.Integer(10)),
        ]

        for i, (sample, expected) in enumerate(tests):
            returned = Eval(Environment(), parse(sample))
            self.assertEqual(returned, expected, f"tests[{i}]: expected {expected}, go {returned}")
    
    def test_return_statements(self):
        tests = [
            ("return 10;", obj.Integer(10)),
            ("return 10; 9;", obj.Integer(10)),
            ("return 2 * 5; 9;", obj.Integer(10)),
            ("9; return 2 * 5; 9;", obj.Integer(10)),
            ("if (10 > 1) { if (10 > 1) { return 10; } return 1; }", obj.Integer(10))
        ]

        for i, (sample, expected) in enumerate(tests):
            returned = Eval(Environment(), parse(sample))
            self.assertEqual(returned, expected, f"tests[{i}]: expected {expected}, got {returned}")

    def test_error_handling(self):
        tests = [
            ("5 + true;", obj.Error("type mismatch: INTEGER + BOOLEAN")),
            ("5 + true; 5;", obj.Error("type mismatch: INTEGER + BOOLEAN")),
            ("-true", obj.Error("unknown operator: -BOOLEAN")),
            ("true + false;", obj.Error("unknown operator: BOOLEAN + BOOLEAN")),
            ("5; true + false; 5", obj.Error("unknown operator: BOOLEAN + BOOLEAN")),
            ("if (10 > 1) { true + false }", obj.Error("unknown operator: BOOLEAN + BOOLEAN")),
            ("if (10 > 1) { if (10 > 1) { return true + false; } return 1; }", obj.Error("unknown operator: BOOLEAN + BOOLEAN")),
            ("foobar", obj.Error("identifier not found: foobar")),
            ('"Hello" - "World"', obj.Error("unknown operator: STRING - STRING")),
            ('{"name": "Monkey"}[fn(x) { x }];', obj.Error("unusable as hash key: FUNCTION")),
        ]

        for i, (sample, expected) in enumerate(tests):
            returned = Eval(Environment(), parse(sample))
            self.assertEqual(returned, expected, f"tests[{i}]: expected {expected}, got {returned}")

    def test_let_statements(self):
        tests = [
            ("let a = 5; a;", obj.Integer(5)),
            ("let a = 5 * 5; a;", obj.Integer(25)),
            ("let a = 5; let b = a; b;", obj.Integer(5)),
            ("let a = 5; let b = a; let c = a + b + 5; c;", obj.Integer(15)),
        ]

        for i, (sample, expected) in enumerate(tests):
            returned = Eval(Environment(), parse(sample))
            self.assertEqual(returned, expected, f"tests[{i}]: expected {expected}, got {returned}")

    def test_function_object(self):
        sample = "fn(x) { x + 2; };"
        env = Environment()
        expected = obj.Function(
            [ast.Identifier("x")],
            ast.BlockStatement([
                ast.ExpressionStatement(ast.InfixExpression(ast.Identifier("x"), "+", ast.IntegerLiteral(2)))
            ]),
            env)
        
        returned = Eval(env, parse(sample))
        self.assertEqual(returned, expected, f"Expected {expected}, got {returned}")

    def test_function_application(self):
        tests = [
            ("let identity = fn(x) { x; }; identity(5);", obj.Integer(5)),
            ("let identity = fn(x) { return x; }; identity(5);", obj.Integer(5)),
            ("let double = fn(x) { x * 2; }; double(5);", obj.Integer(10)),
            ("let add = fn(x, y) { x + y; }; add(5, 5);", obj.Integer(10)),
            ("let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", obj.Integer(20)),
            ("fn(x) { x; }(5)", obj.Integer(5))
        ]

        for i, (sample, expected) in enumerate(tests):
            returned = Eval(Environment(), parse(sample))
            self.assertEqual(returned, expected, f"tests[{i}]: expected {expected}, got {returned}")

    def test_closures(self):
        sample = """
let newAdder = fn(x) {
    fn(y) { x + y };
};

let addTwo = newAdder(2);
addTwo(2);
"""
        expected = obj.Integer(4)
        returned = Eval(Environment(), parse(sample))
        self.assertEqual(returned, expected, f"Expected {expected}, got {returned}")

    def test_string_literal(self):
        sample = '"Hello World!"'
        expected = obj.String("Hello World!")
        returned = Eval(Environment(), parse(sample))
        self.assertEqual(returned, expected, f"Expected {expected}, got {returned}")
    
    def test_string_concatenation(self):
        sample = '"Hello" + " " + "World!"'
        expected = obj.String("Hello World!")
        returned = Eval(Environment(), parse(sample))
        self.assertEqual(returned, expected, f"Expected {expected}, got {returned}")

    def test_builtin_functions(self):
        tests = [
            ('len("")', obj.Integer(0)),
            ('len("four")', obj.Integer(4)),
            ('len("hello world")', obj.Integer(11)),
            ('len(1)', obj.Error("argument to `len` not supported, got INTEGER")),
            ('len("one", "two")', obj.Error("wrong number of arguments; got 2 but wanted 1")),
        ]

        for i, (sample, expected) in enumerate(tests):
            returned = Eval(Environment(), parse(sample))
            self.assertEqual(returned, expected, f"tests[{i}]: expected {expected}, got {returned}")

    def test_array_literals(self):
        sample = "[1, 2 * 2, 3 + 3]"
        expected = obj.Array([obj.Integer(1), obj.Integer(4), obj.Integer(6)])
        returned = Eval(Environment(), parse(sample))
        self.assertEqual(returned, expected, f"Expected {expected}, got {returned}")
    
    def test_array_index_expression(self):
        tests = [
            ("[1, 2, 3][0]", obj.Integer(1)),
            ("[1, 2, 3][1]", obj.Integer(2)),
            ("[1, 3, 3][2]", obj.Integer(3)),
            ("let i = 0; [1][i];", obj.Integer(1)),
            ("[1, 2, 3][1 + 1];", obj.Integer(3)),
            ("let myArray = [1, 2, 3]; myArray[2];", obj.Integer(3)),
            ("let myArray = [1, 2, 3]; myArray[0] + myArray[1] + myArray[2];", obj.Integer(6)),
            ("let myArray = [1, 2, 3]; let i = myArray[0]; myArray[i]", obj.Integer(2)),
            ("[1, 2, 3][3]", obj.Null()),
            ("[1, 2, 3][-1]", obj.Null()),
        ]

        for i, (sample, expected) in enumerate(tests):
            returned = Eval(Environment(), parse(sample))
            self.assertEqual(returned, expected, f"tests[{i}]: expected {expected}, got {returned}")

    def test_string_hash_key(self):
        hello1 = obj.String("Hello World")
        hello2 = obj.String("Hello World")
        diff1 = obj.String("My name is johnny")
        diff2 = obj.String("My name is johnny")

        self.assertEqual(obj.hash_key(hello1), obj.hash_key(hello2))
        self.assertEqual(obj.hash_key(diff1), obj.hash_key(diff2))
        self.assertNotEqual(obj.hash_key(hello1), obj.hash_key(diff1))

    def test_hash_literals(self):
        sample = """
let two = "two";
{
    "one": 10 - 9,
    two: 1 + 1,
    "thr" + "ee": 6 / 2,
    4: 4,
    true: 5,
    false: 6
}
"""
        expected = obj.Hash({
            obj.hash_key(obj.String("one")): obj.HashPair(obj.String("one"), obj.Integer(1)),
            obj.hash_key(obj.String("two")): obj.HashPair(obj.String("two"), obj.Integer(2)),
            obj.hash_key(obj.String("three")): obj.HashPair(obj.String("three"), obj.Integer(3)),
            obj.hash_key(obj.Integer(4)): obj.HashPair(obj.Integer(4), obj.Integer(4)),
            obj.hash_key(obj.Boolean(True)): obj.HashPair(obj.Boolean(True), obj.Integer(5)),
            obj.hash_key(obj.Boolean(False)): obj.HashPair(obj.Boolean(False), obj.Integer(6)),
        })
        returned = Eval(Environment(), parse(sample))

        for i, (r, e) in enumerate(zip(returned.pairs.items(), expected.pairs.items())):
            self.assertEqual(r, e)

    def test_hash_index_expression(self):
        tests = [
            ('{"foo": 5}["foo"]', obj.Integer(5)),
            ('{"foo": 5}["bar"]', obj.Null()),
            ('let key = "foo"; {"foo": 5}[key]', obj.Integer(5)),
            ('{}["foo"]', obj.Null()),
            ('{5: 5}[5]', obj.Integer(5)),
            ('{true: 5}[true]', obj.Integer(5)),
            ('{false: 5}[false]', obj.Integer(5)),
        ]
         
        for i, (sample, expected) in enumerate(tests):
            returned = Eval(Environment(), parse(sample))
            self.assertEqual(returned, expected, f"tests[{i}]: expected {expected}, got {returned}")

if __name__ == '__main__':
    unittest.main()