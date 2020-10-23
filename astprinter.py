from expr import Visitor


class ASTPrinter(Visitor):
    def pprint(self, expr):
        # ask the expr to call our appropriate method
        # (in many langauage I'd rather use a switch on type)
        return expr.accept(self)

    def visitBinaryExpr(self, expr):
        return f"({expr.operator.lexeme} {expr.left.accept(self)} {expr.right.accept(self)})"  # noqa: E501

    def visitGroupingExpr(self, expr):
        return f"(group {expr.expression.accept(self)})"

    def visitLiteralExpr(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr):
        return f"({expr.operator.lexeme} {expr.right.accept(self)})"


if __name__ == "__main__":

    from expr import Binary, Grouping, Literal, Unary
    from token_class import Token
    from token_type import TokenType

    expression = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )

    print(ASTPrinter().pprint(expression))
