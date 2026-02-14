from __future__ import annotations 
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from typing import Generic , TypeVar

if TYPE_CHECKING:
    from expr import Binary, Grouping, Literal, Unary

R = TypeVar('R')


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


class AstPrinter(Visitor[str]):
    def visitBinaryExpr(self,expr:Binary)->str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visitGroupingExpr(self,expr:Grouping)->str:
        return self.parenthesize("group", expr.expression)
    
    def visitLiteralExpr(self, expr:Literal)->str:
        if(expr.value is None):
            return "nil"
        return str(expr.value)
    
    def visitUnaryExpr(self, expr:Unary)->str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        result = f"({name}"
        for expr in exprs:
            result += f" {expr.accept(self)}"
        result += ")"
        return result
    
    def print(self, expr):
        print(expr.accept(self))