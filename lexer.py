from tok import Tag, Token

class Lexer:
    def __init__(self, buffer):
        self.buffer = buffer
        self.read_position = 0
        self.finished = False
        self.read_char()

    def __iter__(self):
        self.read_position = 0
        self.finished = False
        self.read_char()
        return self
    
    def __next__(self):
        if self.finished:
            raise StopIteration

        token = self.next_token()
        if token.tag == Tag.EOF:
            self.finished = True

        return token

    def peek_char(self):
        if self.read_position >= len(self.buffer):
            return ""
        else:
            return self.buffer[self.read_position]

    def read_char(self):
        if self.read_position >= len(self.buffer):
            self.ch = ""
        else:
            self.ch = self.buffer[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def skip_whitespace(self):
        while self.ch.isspace():
            self.read_char()

    def read_identifier(self):
        start = self.position
        while isletter(self.ch):
            self.read_char()
        return self.buffer[start : self.position]

    def read_number(self):
        start = self.position
        while self.ch.isnumeric():
            self.read_char()
        return self.buffer[start : self.position]

    def next_token(self):
        self.skip_whitespace()

        match self.ch:
            case "":
                token = Token(Tag.EOF, self.ch)
            case "=" if self.peek_char() == "=":
                token = Token(Tag.EQ, "==")
                self.read_char()
                self.read_char()
            case "!" if self.peek_char() == "=":
                token = Token(Tag.NOT_EQ, "!=")
                self.read_char()
                self.read_char()
            case ch if ch in symbols.keys():
                token = Token(lookup_symbol(self.ch), self.ch)
                self.read_char()
            case ch if isletter(ch):
                literal = self.read_identifier()
                token = Token(lookup_ident(literal), literal)
            case ch if ch.isnumeric():
                literal = self.read_number()
                token = Token(Tag.INT, literal)
            case _:
                token = Token(Tag.ILLEGAL, self.ch)
                self.read_char()
        
        return token

keywords = { 
    "fn": Tag.FUNCTION,
    "let": Tag.LET,
    "true": Tag.TRUE,
    "false": Tag.FALSE,
    "if": Tag.IF,
    "else": Tag.ELSE,
    "return": Tag.RETURN
}

symbols = {
    "=": Tag.ASSIGN,
    ";": Tag.SEMICOLON,
    "(": Tag.LPAREN,
    ")": Tag.RPAREN,
    ",": Tag.COMMA,
    "+": Tag.PLUS,
    "{": Tag.LBRACE,
    "}": Tag.RBRACE,
    "-": Tag.MINUS,
    "!": Tag.BANG,
    "*": Tag.ASTERISK,
    "/": Tag.SLASH,
    "<": Tag.LT,
    ">": Tag.GT,
}

def isletter(ch):
    return ch.isalpha() or ch == '_'

def lookup_ident(key):
    return keywords.get(key, Tag.IDENT)

def lookup_symbol(key):
    return symbols.get(key, Tag.ILLEGAL)