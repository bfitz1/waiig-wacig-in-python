import unittest

from tok import Token, Tag
from lexer import Lexer

class Test_Lexer(unittest.TestCase):
    def test_tokens(self):
        sample = "=+(){},;"

        expected = [
            (Tag.ASSIGN, "="),
            (Tag.PLUS, "+"),
            (Tag.LPAREN, "("),
            (Tag.RPAREN, ")"),
            (Tag.LBRACE, "{"),
            (Tag.RBRACE, "}"),
            (Tag.COMMA, ","),
            (Tag.SEMICOLON, ";"),
            (Tag.EOF, ""),
        ]

        lexer = Lexer(sample)
        for i, (t, l) in enumerate(zip(expected, lexer)):
            et, el = t
            lt, ll = l

            self.assertEqual(lt, et, f"tests[{i}] - tag wrong. expected={et}, got={lt}")
            self.assertEqual(ll, el, f"tests[{i}] - literal wrong. expected={el}, got={ll}")
        
        # Check that iterator is exhausted
        with self.assertRaises(StopIteration):
            next(lexer)
    
    def test_monkey_code(self):
        sample = """
let five = 5;
let ten = 10;

let add = fn(x, y) {
    x + y;
};

let result = add(five, ten);
!-/*5;
5 < 10 > 5;
"""

        expected = [
            (Tag.LET, "let"),
            (Tag.IDENT, "five"),
            (Tag.ASSIGN, "="),
            (Tag.INT, "5"),
            (Tag.SEMICOLON, ";"),
            (Tag.LET, "let"),
            (Tag.IDENT, "ten"),
            (Tag.ASSIGN, "="),
            (Tag.INT, "10"),
            (Tag.SEMICOLON, ";"),
            (Tag.LET, "let"),
            (Tag.IDENT, "add"),
            (Tag.ASSIGN, "="),
            (Tag.FUNCTION, "fn"),
            (Tag.LPAREN, "("),
            (Tag.IDENT, "x"),
            (Tag.COMMA, ","),
            (Tag.IDENT, "y"),
            (Tag.RPAREN, ")"),
            (Tag.LBRACE, "{"),
            (Tag.IDENT, "x"),
            (Tag.PLUS, "+"),
            (Tag.IDENT, "y"),
            (Tag.SEMICOLON, ";"),
            (Tag.RBRACE, "}"),
            (Tag.SEMICOLON, ";"),
            (Tag.LET, "let"),
            (Tag.IDENT, "result"),
            (Tag.ASSIGN, "="),
            (Tag.IDENT, "add"),
            (Tag.LPAREN, "("),
            (Tag.IDENT, "five"),
            (Tag.COMMA, ","),
            (Tag.IDENT, "ten"),
            (Tag.RPAREN, ")"),
            (Tag.SEMICOLON, ";"),
            (Tag.BANG, "!"),
            (Tag.MINUS, "-"),
            (Tag.SLASH, "/"),
            (Tag.ASTERISK, "*"),
            (Tag.INT, "5"),
            (Tag.SEMICOLON, ";"),
            (Tag.INT, "5"),
            (Tag.LT, "<"),
            (Tag.INT, "10"),
            (Tag.GT, ">"),
            (Tag.INT, "5"),
            (Tag.SEMICOLON, ";"),
            (Tag.EOF, ""),
        ]

        lexer = Lexer(sample)
        for i, (t, l) in enumerate(zip(expected, lexer)):
            et, el = t
            lt, ll = l

            self.assertEqual(lt, et, f"tests[{i}] - tag wrong. expected={et}, got={lt}")
            self.assertEqual(ll, el, f"tests[{i}] - literal wrong. expected={el}, got={ll}")
        
        with self.assertRaises(StopIteration):
            next(lexer)

    def test_if_else(self):
        sample = """
if (5 < 10) {
    return true;
} else {
    return false;
}
"""
        expected = [
            (Tag.IF, "if"),
            (Tag.LPAREN, "("),
            (Tag.INT, "5"),
            (Tag.LT, "<"),
            (Tag.INT, "10"),
            (Tag.RPAREN, ")"),
            (Tag.LBRACE, "{"),
            (Tag.RETURN, "return"),
            (Tag.TRUE, "true"),
            (Tag.SEMICOLON, ";"),
            (Tag.RBRACE, "}"),
            (Tag.ELSE, "else"),
            (Tag.LBRACE, "{"),
            (Tag.RETURN, "return"),
            (Tag.FALSE, "false"),
            (Tag.SEMICOLON, ";"),
            (Tag.RBRACE, "}"),
            (Tag.EOF, ""),
        ]

        lexer = Lexer(sample)
        for i, (t, l) in enumerate(zip(expected, lexer)):
            et, el = t
            lt, ll = l

            self.assertEqual(lt, et, f"tests[{i}] - tag wrong. expected={et}, got={lt}")
            self.assertEqual(ll, el, f"tests[{i}] - literal wrong. expected={el}, got={ll}")
        
        # Check that iterator is exhausted
        with self.assertRaises(StopIteration):
            next(lexer)
    
    def test_double_symbol(self):
        sample = """
10 == 10;
10 != 9;
"""
        expected = [
            (Tag.INT, "10"),
            (Tag.EQ, "=="),
            (Tag.INT, "10"),
            (Tag.SEMICOLON, ";"),
            (Tag.INT, "10"),
            (Tag.NOT_EQ, "!="),
            (Tag.INT, "9"),
            (Tag.SEMICOLON, ";"),
            (Tag.EOF, ""),
        ]

if __name__ == '__main__':
    unittest.main()