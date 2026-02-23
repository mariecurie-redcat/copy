from __future__ import annotations 
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from typing import Generic , TypeVar

from stmt import Expression, Print, Stmt, StmtVisitor
from tokens import Token, TokenType

if TYPE_CHECKING:
    from expr import Binary, Grouping, Literal, Unary,Expr

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


class Interpreter(Visitor[object],StmtVisitor):
    def visitBinaryExpr(self, expr):
        # 算术运算符
        if expr.operator.type in (TokenType.MINUS, TokenType.PLUS, TokenType.SLASH, TokenType.STAR):
            print(f"--------expr.operator {expr.right is None}")
            print(f"--------{repr(expr)}")
            left = float(self.visit(expr.left))
            right = float(self.visit(expr.right)) 
            self.checkNumberOperand(expr.operator, left, right)
            if(expr.operator.type == TokenType.MINUS):
                return left - right
            if(expr.operator.type == TokenType.PLUS):
                return left + right
            if(expr.operator.type == TokenType.SLASH):
                return left / right
            if(expr.operator.type == TokenType.STAR):
                return left * right
        # 比较运算符
        if expr.operator.type in (TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            left =float( self.visit(expr.left))
            right = float(self.visit(expr.right)) 
            self.checkNumberOperand(expr.operator, left, right)
            if(expr.operator.type == TokenType.GREATER):
                return left > right
            if(expr.operator.type == TokenType.GREATER_EQUAL):
                return left >= right
            if(expr.operator.type == TokenType.LESS):
                return left < right
            if(expr.operator.type == TokenType.LESS_EQUAL):
                return left <= right
        # 相等运算符
        if expr.operator.type in (TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            left =float( self.visit(expr.left))
            right =float( self.visit(expr.right) )
        
            if(expr.operator.type == TokenType.EQUAL_EQUAL):
                return left == right
            if(expr.operator.type == TokenType.BANG_EQUAL):
                return left != right
        raise RuntimeError("Unknown operator")

    def visitLiteralExpr(self, expr):
        print(f"--------expr.value: {expr.value}")
        return expr.value

    def visitUnaryExpr(self, expr):
        if expr.operator.type == TokenType.MINUS:
            print(f"--------expr.right.value: {expr.right is None}")
            right = self.visit(expr.right) 
            self.checkNumberOperand(expr.operator, right)
            return -right
        if expr.operator.type == TokenType.BANG:
            return not self.visit(expr.right)
        raise RuntimeError("Unknown unary operator")

    def visitGroupingExpr(self, expr):
        return self.visit(expr.expression)
    
    def visit(self, expr:Expr):
        return expr.accept(self)
    
    def checkNumberOperand(self, operator:Token, operand:object,right:object =None):
        if isinstance(operand, (int, float)) and (isinstance(right, (int, float)) or right is None):
            return
        raise RuntimeError(f"Operand must be a number.")
    
    def visitExpressionStmt(self, stmt:Expression):
        value = self.visit(stmt.expression)
        # print(value)
    
    def visitPrintStmt(self, stmt:Print):
        value = self.visit(stmt.expression)
        print(value)

    def interpret(self, statements:list[Stmt]):
        for statement in statements:
            self.execute(statement)

    def execute(self, stmt:Stmt):
        stmt.accept(self)
