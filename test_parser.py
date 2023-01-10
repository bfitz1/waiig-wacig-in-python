import unittest

from lexer import Lexer
from m_ast import Program, LetStatement, Expression
from parser import Parser

class Test_Parser(unittest.TestCase):
    def test_let_statement(self):
        sample = """
let x = 5;
let y = 10;
let foobar = 838383;
"""

        l = Lexer(sample)
        p = Parser(l)

        program = p.parse_program()
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 3)

        expected = [
            LetStatement(Tag.LET, 'x', Expression()),
            LetStatement(Tag.LET, 'y', Expression()),
            LetStatement(Tag.LET, 'foobar', Expression())
        ]

        for i, (e, ps) in enumerate(zip(expected, program)):
            self.assertEqual(e, ps, f"For program.statement[{i}], expected {e} but got {ps}")
    
    def test_return_statement(self):
        sample = """
return 5;
return 10;
return 993322;
"""

        l = Lexer(sample)
        p = Parser(l)

        program = p.parse_program()
        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 3)

        expected = [
            ReturnStatement(Tag.RETURN, Expression()),
            ReturnStatement(Tag.RETURN, Expression()),
            ReturnStatement(Tag.RETURN, Expression())
        ]

        for i, (e, ps) in enumerate(zip(expected, program)):
            self.assertEqual(e, ps, f"For program.statement[{i}], expected {e} but got {ps}")

if __name__ == '__main__':
    unittest.main()