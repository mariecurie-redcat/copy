from expr import Binary, Grouping, Literal, Unary
from tokens import Token
from visitor import AstPrinter


a = Binary(Unary(Token("minus", "-", None, 1),Literal(123)),Token("plus", "+", None, 1),
           Grouping(Literal(456)))

AstPrinter().print()