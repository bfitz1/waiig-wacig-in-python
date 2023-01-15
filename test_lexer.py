import unittest

from tok import TokenType, Token
from lexer import Lexer

class Test_Lexer(unittest.TestCase):
    def test_tokens(self):
        sample = "=+(){},;"

        expected = [
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
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
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "five"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "5"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "ten"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "10"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "add"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.FUNCTION, "fn"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.IDENT, "x"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.IDENT, "y"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "result"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.IDENT, "add"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "five"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.IDENT, "ten"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.BANG, "!"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.SLASH, "/"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.INT, "5"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.INT, "5"),
            Token(TokenType.LT, "<"),
            Token(TokenType.INT, "10"),
            Token(TokenType.GT, ">"),
            Token(TokenType.INT, "5"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
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
            Token(TokenType.IF, "if"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.INT, "5"),
            Token(TokenType.LT, "<"),
            Token(TokenType.INT, "10"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RETURN, "return"),
            Token(TokenType.TRUE, "true"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.ELSE, "else"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RETURN, "return"),
            Token(TokenType.FALSE, "false"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.EOF, ""),
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
            Token(TokenType.INT, "10"),
            Token(TokenType.EQ, "=="),
            Token(TokenType.INT, "10"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.INT, "10"),
            Token(TokenType.NOT_EQ, "!="),
            Token(TokenType.INT, "9"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
        ]

        lexer = Lexer(sample)
        for i, (t, l) in enumerate(zip(expected, lexer)):
            et, el = t
            lt, ll = l

            self.assertEqual(lt, et, f"tests[{i}] - tag wrong. expected={et}, got={lt}")
            self.assertEqual(ll, el, f"tests[{i}] - literal wrong. expected={el}, got={ll}")

    def test_strings(self):
        sample = """
"foobar"
"foo bar"
"""
        expected = [
            Token(TokenType.STRING, "foobar"),
            Token(TokenType.STRING, "foo bar"),
            Token(TokenType.EOF, ""),
        ]

        lexer = Lexer(sample)
        for i, (t, l) in enumerate(zip(expected, lexer)):
            et, el = t
            lt, ll = l

            self.assertEqual(lt, et, f"tests[{i}] - tag wrong. expected={et}, got={lt}")
            self.assertEqual(ll, el, f"tests[{i}] - literal wrong. expected={el}, got={ll}")


if __name__ == '__main__':
    unittest.main()