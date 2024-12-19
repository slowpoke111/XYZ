from typing import Any, Optional, Generic, TypeVar

R = TypeVar('R')

class Expr:
    """Forward declaration for Expr"""
    pass

class Expr:
    """Base class for Abstract Syntax Tree nodes"""
    class Visitor(Generic[R]):
        def visitBinaryExpr(self, expr: 'Expr.Binary') -> R:
            pass

        def visitGroupingExpr(self, expr: 'Expr.Grouping') -> R:
            pass

        def visitLiteralExpr(self, expr: 'Expr.Literal') -> R:
            pass

        def visitUnaryExpr(self, expr: 'Expr.Unary') -> R:
            pass

    def accept(self, visitor: 'Visitor[R]') -> R:
        raise NotImplementedError('Subclasses must implement accept')

    class Binary(Expr):
        def __init__(self, left: 'Expr', operator: 'Token', right: 'Expr'):
            self.left = left
            self.operator = operator
            self.right = right

        left: 'Expr'
        operator: 'Token'
        right: 'Expr'

        def accept(self, visitor: 'Expr.Visitor[R]') -> R:
            return visitor.visitBinaryExpr(self)
            
    class Grouping(Expr):
        def __init__(self, expression: 'Expr'):
            self.expression = expression

        expression: 'Expr'

        def accept(self, visitor: 'Expr.Visitor[R]') -> R:
            return visitor.visitGroupingExpr(self)
            
    class Literal(Expr):
        def __init__(self, value: Any):
            self.value = value

        value: Any

        def accept(self, visitor: 'Expr.Visitor[R]') -> R:
            return visitor.visitLiteralExpr(self)
            
    class Unary(Expr):
        def __init__(self, operator: 'Token', right: 'Expr'):
            self.operator = operator
            self.right = right

        operator: 'Token'
        right: 'Expr'

        def accept(self, visitor: 'Expr.Visitor[R]') -> R:
            return visitor.visitUnaryExpr(self)
