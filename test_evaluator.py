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


if __name__ == '__main__':
    unittest.main()