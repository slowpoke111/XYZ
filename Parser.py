from typing import *
from TokenType import TokenType
from TokenClass import Token
from Expr import Expr
import XYZ

class Parser:
    tokens:List[Token]
    current:int = 0
    
    class ParseError(RuntimeError):
        def __init__(self):
            super().__init__()

    def __init__(self, tokens:List[Token]):
        self.tokens = tokens
    
    def expression(self) -> Expr:
        return self.equality()
    
    def equality(self) -> Expr:
        expr:Expr = self.comparison()
        while self.match(TokenType.EXCLAMATION_EQUAL, TokenType.EQUAL_EQUAL):
            operator:Token = self.previous()
            right:Expr = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def match(self, *types:TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def check(self, type:TokenType) -> bool:
        if self.isAtEnd(): return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current+=1
        return self.previous()
    
    def isAtEnd(self) -> bool:
        return self.peek().type == TokenType.EOF
    def peek(self) -> Token:
        return self.tokens[self.current]
    def previous(self) -> Token:
        return self.tokens[self.current-1]
    
    def comparison(self) -> Expr:
        expr:Expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator:Token = self.previous()
            right:Expr = self.term()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def term(self) -> Expr:
        expr:Expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator:Token = self.previous()
            right:Expr = self.factor()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def factor(self) -> Expr:
        expr:Expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator:Token = self.previous()
            right:Expr = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def unary(self) -> Expr:
        if self.match(TokenType.EXCLAMATION, TokenType.MINUS):
            operator:Token = self.previous()
            right:Expr = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()
    
    def primary(self) -> Expr:
        if self.match(TokenType.FALSE): return Expr.Literal(False)
        if self.match(TokenType.TRUE): return Expr.Literal(True)
        if self.match(TokenType.NIL): return Expr.Literal(None)
        
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.previous().literal)
        
        if self.match(TokenType.LEFT_PAREN):
            expr:Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")
    
    def consume(self,type:TokenType, message:str) -> Token:
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)
    
    def error(self,token:Token,message:str) -> ParseError:
        XYZ.error(token, message)
        return ParseError()
    
    def synchronize(self) -> None:
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON: return
            if self.peek().type in [TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN]: return
            self.advance()
    
    def parse(self):
        try:
            return self.expression()
        except ParseError:
            return None