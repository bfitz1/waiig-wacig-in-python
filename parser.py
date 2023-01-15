from enum import Enum

from tok import TokenType, Token
from lexer import Lexer
from mast import * 

LOWEST = 1
EQUALS = 2
LESSGREATER = 3
SUM = 4
PRODUCT = 5
PREFIX = 6
CALL = 7

# Note to self: Not happy with this, for a variety of reasons:
# - It just feels like it could be organized and/or expressed better.
# - I don't know what `return None` is doing in most cases. They show up when
#   asserts fail, and a failed assert is (IME) a hard crash.
# - Come to think of it, the errors list goes mostly unused anyway.
# - Not stopping when asserts fail leads to some other weirdness
#   when parsing.
# - It's probably too general for this project, but maybe consider accepting
#   configuration parameters for the parser.

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.errors = []
        self.current = self.lexer.next_token()
        self.peek = self.lexer.next_token()
        self.prefix_parse_fns = {}
        self.infix_parse_fns = {}

        self.register_prefix(TokenType.IDENT, self.parse_identifier)
        self.register_prefix(TokenType.INT, self.parse_integer_literal)
        self.register_prefix(TokenType.BANG, self.parse_prefix_expression)
        self.register_prefix(TokenType.MINUS, self.parse_prefix_expression)
        self.register_prefix(TokenType.TRUE, self.parse_boolean)
        self.register_prefix(TokenType.FALSE, self.parse_boolean)
        self.register_prefix(TokenType.LPAREN, self.parse_grouped_expression)
        self.register_prefix(TokenType.IF, self.parse_if_expression)
        self.register_prefix(TokenType.FUNCTION, self.parse_function_literal)

        self.register_infix(TokenType.PLUS, self.parse_infix_expression)
        self.register_infix(TokenType.MINUS, self.parse_infix_expression)
        self.register_infix(TokenType.SLASH, self.parse_infix_expression)
        self.register_infix(TokenType.ASTERISK, self.parse_infix_expression)
        self.register_infix(TokenType.EQ, self.parse_infix_expression)
        self.register_infix(TokenType.NOT_EQ, self.parse_infix_expression)
        self.register_infix(TokenType.LT, self.parse_infix_expression)
        self.register_infix(TokenType.GT, self.parse_infix_expression)
        self.register_infix(TokenType.LPAREN, self.parse_call_expression)

    def __iter__(self):
        yield from self.parse_program()

    def register_prefix(self, tokentype, fn):
        self.prefix_parse_fns[tokentype] = fn

    def register_infix(self, tokentype, fn):
        self.infix_parse_fns[tokentype] = fn

    def next_token(self):
        self.current = self.peek
        self.peek = self.lexer.next_token()

    def parse_program(self):
        statements = []
        while self.current.type != TokenType.EOF:
            s = self.parse_statement()
            if s is not None:
                statements.append(s)
            self.next_token()
        return Program(statements)
    
    def parse_statement(self):
        match self.current.type:
            case TokenType.LET:
                return self.parse_let_statement()
            case TokenType.RETURN:
                return self.parse_return_statement()
            case _:
                return self.parse_expression_statement()

    def parse_let_statement(self):
        if not self.expect_peek(TokenType.IDENT):
            return None
        
        identifier = self.parse_identifier()

        if not self.expect_peek(TokenType.ASSIGN):
            return None

        self.next_token()
        expr = self.parse_expression(LOWEST)
        
        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return LetStatement(identifier, expr)
    
    def parse_return_statement(self):
        self.next_token()

        expr = self.parse_expression(LOWEST)

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()
        
        return ReturnStatement(expr)
    
    def parse_expression_statement(self):
        expr = self.parse_expression(LOWEST)

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return ExpressionStatement(expr)
    
    def parse_block_statement(self):
        statements = []

        self.next_token()

        while not (self.current_token_is(TokenType.RBRACE) or self.current_token_is(TokenType.EOF)):
            st = self.parse_statement()
            if st:
                statements.append(st)
            self.next_token()
        
        return BlockStatement(statements)

    def parse_expression(self, precedence):
        prefix = self.prefix_parse_fns.get(self.current.type, None)
        if prefix is None:
            self.errors.append(f'No prefix parse function for {self.current.type} found')
            return None
        left_expr = prefix()

        while not self.peek_token_is(TokenType.SEMICOLON) and precedence < self.peek_precedence():
            infix = self.infix_parse_fns.get(self.peek.type, None)
            if infix is None:
                return left_expr
            
            self.next_token()
            left_expr = infix(left_expr)
        
        return left_expr
    
    def parse_identifier(self):
        return Identifier(self.current.text)
    
    def parse_integer_literal(self):
        try:
            value = int(self.current.text)
        except ValueError:
            self.errors.append(f'Could not parse {self.current.text!r} as integer')
            return None
        else:
            return IntegerLiteral(value)
    
    def parse_function_literal(self):
        if not self.expect_peek(TokenType.LPAREN):
            return None
        
        parameters = self.parse_function_parameters()

        if not self.expect_peek(TokenType.LBRACE):
            return None
        
        body = self.parse_block_statement()

        return FunctionLiteral(parameters, body)
    
    def parse_function_parameters(self):
        identifiers = []

        if self.peek_token_is(TokenType.RPAREN):
            self.next_token()
            return identifiers
        
        self.next_token()

        ident = Identifier(self.current.text)
        identifiers.append(ident)

        while self.peek_token_is(TokenType.COMMA):
            self.next_token()
            self.next_token()
            ident = Identifier(self.current.text)
            identifiers.append(ident)
        
        if not self.expect_peek(TokenType.RPAREN):
            return None
        
        return identifiers
    
    def parse_call_expression(self, function):
        arguments = self.parse_call_arguments()
        return CallExpression(function, arguments)
    
    def parse_call_arguments(self):
        args = []

        if self.peek_token_is(TokenType.RPAREN):
            self.next_token()
            return args
        
        self.next_token()
        args.append(self.parse_expression(LOWEST))
        while self.peek_token_is(TokenType.COMMA):
            self.next_token()
            self.next_token()
            args.append(self.parse_expression(LOWEST))
        
        if not self.expect_peek(TokenType.RPAREN):
            return None

        return args

    def parse_prefix_expression(self):
        operator = self.current.text
        self.next_token()
        right = self.parse_expression(PREFIX)
        return PrefixExpression(operator, right)
    
    def parse_boolean(self):
        return Boolean(self.current_token_is(TokenType.TRUE))
    
    def parse_grouped_expression(self):
        self.next_token()
        expr = self.parse_expression(LOWEST)
        if not self.expect_peek(TokenType.RPAREN):
            return None
        return expr
    
    def parse_if_expression(self):
        if not self.expect_peek(TokenType.LPAREN):
            return None
        
        self.next_token()
        condition = self.parse_expression(LOWEST)

        if not self.expect_peek(TokenType.RPAREN):
            return None
        
        if not self.expect_peek(TokenType.LBRACE):
            return None
        
        consequence = self.parse_block_statement()

        alternative = None
        if self.peek_token_is(TokenType.ELSE):
            self.next_token()
            
            if not self.expect_peek(TokenType.LBRACE):
                return None
            
            alternative = self.parse_block_statement()

        return IfExpression(condition, consequence, alternative)

    def parse_infix_expression(self, left):
        operator = self.current.text
        prece = self.current_precedence()
        self.next_token()
        right = self.parse_expression(prece)
        return InfixExpression(left, operator, right)
    
    def current_token_is(self, tokentype):
        return self.current.type == tokentype

    def peek_token_is(self, tokentype):
        return self.peek.type == tokentype
    
    def expect_peek(self, tokentype):
        if self.peek_token_is(tokentype):
            self.next_token()
            return True
        else:
            self.peek_error(tokentype)
            return False
    
    def peek_precedence(self):
        return precedences.get(self.peek.type, LOWEST)
    
    def current_precedence(self):
        return precedences.get(self.current.type, LOWEST)

    def peek_error(self, tokentype):
        self.errors.append(f'expected next token to be {self.peek.type}, got {tokentype} instead')

def parse(text):
    return Parser(Lexer(text)).parse_program()

precedences = dict([
    (TokenType.EQ, EQUALS),
    (TokenType.NOT_EQ, EQUALS),
    (TokenType.LT, LESSGREATER),
    (TokenType.GT, LESSGREATER),
    (TokenType.PLUS, SUM),
    (TokenType.MINUS, SUM),
    (TokenType.SLASH, PRODUCT),
    (TokenType.ASTERISK, PRODUCT),
    (TokenType.LPAREN, CALL),
])