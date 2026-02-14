from tokens import Token, TokenType


keywords = {
    "and":    TokenType.AND,
    "class":  TokenType.CLASS,
    "else":   TokenType.ELSE,
    "false":  TokenType.FALSE,
    "for":    TokenType.FOR,
    "fun":    TokenType.FUN,
    "if":     TokenType.IF,
    "nil":    TokenType.NIL,
    "or":     TokenType.OR,
    "print":  TokenType.PRINT,
    "return": TokenType.RETURN,
    "super":  TokenType.SUPER,
    "this":   TokenType.THIS,
    "true":   TokenType.TRUE,
    "var":    TokenType.VAR,
    "while":  TokenType.WHILE,
}


class Scanner:
    source:str
    tokens:list[Token]
    start:int =0
    current:int =0
    line:int =1

    def __init__(self,source:str):
        self.source = source
        self.tokens = []
    
    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def isAtEnd(self):
        return self.current >= len(self.source)
    
    def scanToken(self):
        c = self.advance()
        if c == '*':
            self.add_token(TokenType.STAR)
        elif c == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '/':
            if self.match('/'):
                while self.current < len(self.source) and self.source[self.current] != '\n':
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == ' ' or c == '\r' or c == '\t':
            pass
        elif c=='\n':
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if self.isDigit(c):
                self.number()
            elif c.isalpha():
                self.identifier()
            else:
                # 默认情况，可以报错或忽略
                
                print(f"line {self.line} Unexpected character: {c} {c.isalpha()}")

    def identifier(self):
        while self.peek().isalnum():
            self.advance()
        literal = self.source[self.start:self.current]
        token_type = keywords.get(literal, TokenType.IDENTIFIER)
        self.add_token(token_type, literal)

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()
        if(self.peek() == '.' and self.isDigit(self.peekNext())):
            self.advance()
            while self.isDigit(self.peek()):
                self.advance()
        literal = self.source[self.start:self.current]
        self.add_token(TokenType.NUMBER, literal)

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def isDigit(self, c):
        return c >= '0' and c <= '9'

    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.isAtEnd():
            print(f"line {self.line} Unterminated string.")
            return
        self.advance() # consume the closing quote
        literal = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, literal)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]
    
    def add_token(self, token_type: TokenType,literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
    
    def match(self, expected: str):
        if(self.isAtEnd()):
            return False
        if self.source[self.current] == expected:
            self.current += 1
            return True
        return False
    
    def peek(self):
        if(self.isAtEnd()):
            return '\0'
        return self.source[self.current]