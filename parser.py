from enum import Enum

from tok import Tag, Token
from lexer import Lexer
from m_ast import * 

LOWEST = 1
EQUALS = 2
LESSGREATER = 3
SUM = 4
PRODUCT = 5
PREFIX = 6
CALL = 7

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.errors = []
        self.current = self.lexer.next_token()
        self.peek = self.lexer.next_token()
        self.prefix_parse_fns = {}
        self.infix_parse_fns = {}

        self.register_prefix(Tag.IDENT, self.parse_identifier)
        self.register_prefix(Tag.INT, self.parse_integer_literal)
        self.register_prefix(Tag.BANG, self.parse_prefix_expression)
        self.register_prefix(Tag.MINUS, self.parse_prefix_expression)
        self.register_prefix(Tag.TRUE, self.parse_boolean)
        self.register_prefix(Tag.FALSE, self.parse_boolean)
        self.register_prefix(Tag.LPAREN, self.parse_grouped_expression)
        self.register_prefix(Tag.IF, self.parse_if_expression)
        self.register_prefix(Tag.FUNCTION, self.parse_function_literal)

        self.register_infix(Tag.PLUS, self.parse_infix_expression)
        self.register_infix(Tag.MINUS, self.parse_infix_expression)
        self.register_infix(Tag.SLASH, self.parse_infix_expression)
        self.register_infix(Tag.ASTERISK, self.parse_infix_expression)
        self.register_infix(Tag.EQ, self.parse_infix_expression)
        self.register_infix(Tag.NOT_EQ, self.parse_infix_expression)
        self.register_infix(Tag.LT, self.parse_infix_expression)
        self.register_infix(Tag.GT, self.parse_infix_expression)
        self.register_infix(Tag.LPAREN, self.parse_call_expression)

    def register_prefix(self, tag, fn):
        self.prefix_parse_fns[tag] = fn

    def register_infix(self, tag, fn):
        self.infix_parse_fns[tag] = fn

    def next_token(self):
        self.current = self.peek
        self.peek = self.lexer.next_token()

    def parse_program(self):
        statements = []
        while self.current.tag != Tag.EOF:
            s = self.parse_statement()
            if s is not None:
                statements.append(s)
            self.next_token()
        return Program(statements)
    
    def parse_statement(self):
        match self.current.tag:
            case Tag.LET:
                return self.parse_let_statement()
            case Tag.RETURN:
                return self.parse_return_statement()
            case _:
                return self.parse_expression_statement()

    def parse_let_statement(self):
        if not self.expect_peek(Tag.IDENT):
            return None
        
        identifier = self.current.literal

        if not self.expect_peek(Tag.ASSIGN):
            return None

        expr = self.parse_expression(LOWEST)
        
        if self.peek_token_is(Tag.SEMICOLON):
            self.next_token()

        return LetStatement(Tag.LET, identifier, expr)
    
    def parse_return_statement(self):
        self.next_token()

        expr = self.parse_expression(LOWEST)

        if self.peek_token_is(Tag.SEMICOLON):
            self.next_token()
        
        return ReturnStatement(Tag.RETURN, expr)
    
    def parse_expression_statement(self):
        tag = self.current.tag
        expr = self.parse_expression(LOWEST)

        if self.peek_token_is(Tag.SEMICOLON):
            self.next_token()

        return ExpressionStatement(tag, expr)
    
    def parse_block_statement(self):
        tag = self.current.tag
        statements = []

        self.next_token()

        while not self.current_token_is(Tag.RBRACE) and not self.current_token_is(Tag.EOF):
            st = self.parse_statement()
            if st:
                statements.append(st)
            self.next_token()
        
        return BlockStatement(tag, statements)

    def parse_expression(self, precedence):
        prefix = self.prefix_parse_fns.get(self.current.tag, None)
        if prefix is None:
            self.errors.append(f'No prefix parse function for {self.current.tag} found')
            return None
        left_expr = prefix()

        while not self.peek_token_is(Tag.SEMICOLON) and precedence < self.peek_precedence():
            infix = self.infix_parse_fns.get(self.peek.tag, None)
            if infix is None:
                return left_expr
            
            self.next_token()
            left_expr = infix(left_expr)
        
        return left_expr
    
    def parse_identifier(self):
        return Identifier(self.current.tag, self.current.literal)
    
    def parse_integer_literal(self):
        try:
            value = int(self.current.literal)
        except ValueError:
            self.errors.append(f'Could not parse {self.current.literal!r} as integer')
            return None
        else:
            return IntegerLiteral(Tag.INT, value)
    
    def parse_function_literal(self):
        tag = self.current.tag

        if not self.expect_peek(Tag.LPAREN):
            return None
        
        parameters = self.parse_function_parameters()

        if not self.expect_peek(Tag.LBRACE):
            return None
        
        body = self.parse_block_statement()

        return FunctionLiteral(tag, parameters, body)
    
    def parse_function_parameters(self):
        identifiers = []

        if self.peek_token_is(Tag.RPAREN):
            self.next_token()
            return identifiers
        
        self.next_token()

        ident = Identifier(self.current.tag, self.current.literal)
        identifiers.append(ident)

        while self.peek_token_is(Tag.COMMA):
            self.next_token()
            self.next_token()
            ident = Identifier(self.current.tag, self.current.literal)
            identifiers.append(ident)
        
        if not self.expect_peek(Tag.RPAREN):
            return None
        
        return identifiers
    
    def parse_call_expression(self, function):
        tag = self.current.tag
        arguments = self.parse_call_arguments()
        return CallExpression(tag, function, arguments)
    
    def parse_call_arguments(self):
        args = []

        if self.peek_token_is(Tag.RPAREN):
            self.next_token()
            return args
        
        self.next_token()
        args.append(self.parse_expression(LOWEST))
        while self.peek_token_is(Tag.COMMA):
            self.next_token()
            self.next_token()
            args.append(self.parse_expression(LOWEST))
        
        if not self.expect_peek(Tag.RPAREN):
            return None

        return args

    def parse_prefix_expression(self):
        tag = self.current.tag
        operator = self.current.literal
        self.next_token()
        right = self.parse_expression(PREFIX)
        return PrefixExpression(tag, operator, right)
    
    def parse_boolean(self):
        return Boolean(self.current.tag, self.current_token_is(Tag.TRUE))
    
    def parse_grouped_expression(self):
        self.next_token()
        expr = self.parse_expression(LOWEST)
        if not self.expect_peek(Tag.RPAREN):
            return None
        return expr
    
    def parse_if_expression(self):
        tag = self.current.tag

        if not self.expect_peek(Tag.LPAREN):
            return None
        
        self.next_token()
        condition = self.parse_expression(LOWEST)

        if not self.expect_peek(Tag.RPAREN):
            return None
        
        if not self.expect_peek(Tag.LBRACE):
            return None
        
        consequence = self.parse_block_statement()

        if self.peek_token_is(Tag.ELSE):
            self.next_token()
            
            if not self.expect_peek(Tag.LBRACE):
                return None
            
            alternative = self.parse_block_statement()

        return IfExpression(tag, condition, consequence, alternative)

    def parse_infix_expression(self, left):
        tag = self.current.tag
        operator = self.current.literal
        prece = self.current_precedence()
        self.next_token()
        right = self.parse_expression(prece)
        return InfixExpression(tag, left, operator, right)
    
    def current_token_is(self, tag):
        return self.current.tag == tag

    def peek_token_is(self, tag):
        return self.peek.tag == tag
    
    def expect_peek(self, tag):
        if self.peek_token_is(tag):
            self.next_token()
            return True
        else:
            self.peek_error(tag)
            return False
    
    def peek_precedence(self):
        return precedences.get(self.peek.tag, LOWEST)
    
    def current_precedence(self):
        return precedences.get(self.current.tag, LOWEST)

    def peek_error(self, tag):
        self.errors.append(f'expected next token to be {self.peek.tag}, got {tag} instead')

precedences = dict([
    (Tag.EQ, EQUALS),
    (Tag.NOT_EQ, EQUALS),
    (Tag.LT, LESSGREATER),
    (Tag.GT, LESSGREATER),
    (Tag.PLUS, SUM),
    (Tag.MINUS, SUM),
    (Tag.SLASH, PRODUCT),
    (Tag.ASTERISK, PRODUCT),
    (Tag.LPAREN, CALL),
])