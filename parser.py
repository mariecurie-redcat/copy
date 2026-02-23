from expr import Binary, Grouping, Literal, Unary
from stmt import Expression, Expression, Print
from tokens import Token, TokenType

# expression     → equality ;
# equality       → comparison ( ( "!=" | "==" ) comparison )* ;
# comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
# term           → factor ( ( "-" | "+" ) factor )* ;
# factor         → unary ( ( "/" | "*" ) unary )* ;
# unary          → ( "!" | "-" ) unary
#                | primary ;
# primary        → NUMBER | STRING | "true" | "false" | "nil"
#                | "(" expression ")" ;

class LxoParser:
    tokens:list[Token]
    current:int 
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr
    
    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
    
    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    
    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr
    
    def unary(self):
        print(repr(self.peek()))
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()
    
    def primary(self):
        if self.match(TokenType.FALSE, TokenType.TRUE, TokenType.NIL):
            return Literal(self.previous().literal)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.equality()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        raise self.error(self.peek(), "Expect expression.")
        
    def error(self, token:Token, message:str):
        print(f"[line {token.line}] Error: {message}")
        return None
    
    def consume(self, token_type: TokenType, message: str):
        if self.check(token_type):
            self.advance()
            return
        raise self.error(self.peek(), message)
    
    def match(self, *token_types: TokenType):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def check(self, token_type: TokenType):
        if self.isAtEnd():
            return False
        return self.peek().type == token_type
    
    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()
    
    def isAtEnd(self):
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]

    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return
            type = self.peek().type
            if type in (TokenType.CLASS, TokenType.FUN, TokenType.VAR, 
                        TokenType.FOR, TokenType.IF, 
                        TokenType.WHILE, TokenType.PRINT, TokenType.RETURN):
                return
            self.advance()

    def parse(self):
        statements = []
        while not self.isAtEnd():
            statements.append(self.statement())
        return statements
    
    def statement(self):
        if self.match(TokenType.PRINT):
            return self.printStatement()
        return self.expressionStatement()
    
    def printStatement(self):
        value = self.equality()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)
    
    def expressionStatement(self):
        expr = self.equality()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)