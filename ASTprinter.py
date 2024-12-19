from typing import Any, override
from Expr import Expr
import TokenClass
from TokenType import TokenType

class ASTprinter:
    def print(self, expr:Expr) -> str:
        return expr.accept(self)

    @override
    def visitBinaryExpr(self, expr:Expr.Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    @override
    def visitGroupingExpr(self, expr:Expr.Grouping) -> str:
        return self.parenthesize("group", expr.expression)
    @override
    def visitLiteralExpr(self, expr:Expr.Literal) -> str:
        return str(expr.value)
    @override
    def visitUnaryExpr(self, expr:Expr.Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def parenthesize(self, name:str, *exprs:Expr) -> str:
        builder:str = "("
        builder += name
        for expr in exprs:
            builder += " "
            builder += expr.accept(self)
        builder += ")"
        return builder
    
    def main() -> None: 
        expression:Expr = Expr.Binary(
            Expr.Unary(
                TokenClass.Token(TokenType.MINUS, "-", None, 1), 
                Expr.Literal(123)  # Changed from Literal to Expr.Literal
            ),
            TokenClass.Token(TokenType.STAR, "*", None, 1),
            Expr.Grouping(Expr.Literal(45.67))  # Changed from Literal to Expr.Literal
        )
        print(ASTprinter().print(expression))

if __name__ == "__main__":
    ASTprinter.main()