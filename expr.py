from tokens import Token
from abc import ABC,abstractmethod
from typing import Generic , TypeVar

R = TypeVar('R')

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

class Grouping(Expr):
    expression:Expr
    def __init__(self, expression):
        self.expression = expression

class Literal(Expr):
    value:object
    def __init__(self, value):
        self.value =value
    
class Unary(Expr):
    operator:Token
    right:Expr
    def __init__(self,operator,right):
        self.operator =operator
        self.right = right


class Visitor(ABC,Generic[R]):
    @abstractmethod
    def visitBinaryExpr(self,expr:Binary)->R:
        pass
    
    @abstractmethod
    def visitUnaryExpr(self,expr:Unary)->R:
        pass

    @abstractmethod
    def visitGroupingExpr(self,expr:Grouping)->R:
        pass

    @abstractmethod
    def visitLiteralExpr(self,expr:Literal)->R:
        pass