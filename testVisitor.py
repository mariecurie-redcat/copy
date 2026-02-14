from expr import Binary, Grouping, Literal, Unary
from tokens import Token
from visitor import AstPrinter


a = Binary(Unary(Token("MINUS", "-", None, 1),Literal(123)),Token("PLUS", "+", None, 1),
           Grouping(Literal(456)))

AstPrinter().print(a)