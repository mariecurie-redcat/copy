
from tokens import Token, TokenType
from visitor import AstPrinter, Interpreter
from parser import LxoParser
from scanner import Scanner


with open("bash.txt", "r") as f:
    content = f.read()

scanner = Scanner(content)
tokens = scanner.scanTokens()

for token in tokens:
    print(token)
print(Interpreter().interpret(LxoParser(tokens).parse()))
# AstPrinter().print(LxoParser(tokens).equality())


def error(token:Token,messege:str):
    if token.type == TokenType.EOF:
        print(f"line {token.line} at end {messege}")
    else:
        print(f"line {token.line} error: {messege}")

class ParseError(RuntimeError):
    pass