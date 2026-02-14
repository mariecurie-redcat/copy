from tokens import Token
from abc import ABC,abstractmethod
from typing import Generic , TypeVar
from visitor import R, Visitor


class Expr:
    @abstractmethod
    def accept(self,visitor:Visitor[R])->R:
        pass

class Binary(Expr):
    left:Expr
    operator:Token
    right:Expr
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)

class Grouping(Expr):
    expression:Expr
    def __init__(self, expression):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)

class Literal(Expr):
    value:object
    def __init__(self, value):
        self.value =value

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)
    
class Unary(Expr):
    operator:Token
    right:Expr
    
    def __init__(self,operator,right):
        self.operator =operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)
    