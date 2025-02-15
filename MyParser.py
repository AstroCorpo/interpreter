from MyScanner import MyScanner
import AST
from sly import Parser
import TreePrinter

class MyParser(Parser):
    tokens = MyScanner.tokens
    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', IFX),
        ('nonassoc', ELSE),
        ('nonassoc', LTE, GTE, EQ, NEQ, LT, GT),
        ('left', ADD, SUB, DOTADD, DOTSUB),
        ('left', MUL, DIV, DOTMUL, DOTDIV),
        ('nonassoc', "'")
    )

    @_('statements stmt',
       'stmt')
    def statements(self, p):
        if len(p) == 1:
            return AST.StatementsNode([p[0]], lineno=p.lineno)

        statements = p[0].statements.copy()
        statements.append(p[1])

        return AST.StatementsNode(statements, lineno=p.lineno)

    @_(
        '";"',
        '"{" statements "}"',
        'if_stmt',
        'while_stmt',
        'for_stmt',
        'assign_expr',
        'print_stmt',
        'BREAK ";"',
        'CONTINUE ";"',
        'RETURN expr ";"'
    )
    def stmt(self, p):
        try:
            if (p.BREAK):
                return AST.BreakStatement(lineno=p.lineno)
        except:
            pass
        try:
            if (p.CONTINUE):
                return AST.ContinueStatement(lineno=p.lineno)
        except:
            pass
        try:
            if (p.RETURN):
                return AST.ReturnStatement(p[1], lineno=p.lineno)
        except:
            pass

        if p[0] == ";":
            return AST.BlankStatement(lineno=p.lineno)

        if len(p) == 1:
            return p[0]

        return p[1]

    @_(
        'IF "(" rel_expr ")" stmt ELSE stmt',
        'IF "(" rel_expr ")" stmt %prec IFX'
    )
    def if_stmt(self, p):
        condition = p[2]
        if_body = p[4]
        else_body = None


        try:
            if (p.ELSE):
                else_body = p[6]
        except:
            pass

        print(if_body, else_body)

        return AST.IfElseExpr(condition, if_body, else_body, lineno=p.lineno)

    @_(
        'FOR referance "=" value ":" value stmt'
    )
    def for_stmt(self, p):
        return AST.ForLoop(p[1], p[3], p[5], p[6], p.lineno)

    @_(
        'WHILE "(" rel_expr ")" stmt'
    )
    def while_stmt(self, p):
        return AST.WhileLoop(p[2], p[4], p.lineno)

    @_(
        'PRINT value'
    )
    def print_stmt(self, p):
        return AST.Print(p[1], lineno=p.lineno)

    @_(
        'INTNUM'
    )
    def IntNum(self, p):
        return AST.IntNum(p[0], p.lineno)

    @_(
        'FLOATNUM'
    )
    def FloatNum(self, p):
        return AST.FloatNum(p[0], p.lineno)

    @_(
        'STRING'
    )
    def String(self, p):
        return AST.String(p[0], p.lineno)

    @_(
        'IntNum',
        'FloatNum',
        'String',
        'referance'
    )
    def value(self, p):
        return AST.Value(p[0], p.lineno)

    @_(
        'ZEROS "(" value ")"',
        'ONES "(" value ")"',
        'EYE "(" value ")"'
    )
    def matrix_func(self, p):
        func_name = p[0]
        size = p[2]

        if func_name == 'zeros':
            return AST.ZerosFunc(size, lineno=p.lineno)
        elif func_name == 'ones':
            return AST.OnesFunc(size, lineno=p.lineno)
        elif func_name == 'eye':
            return AST.EyeFunc(size, lineno=p.lineno)

    @_(
        'value',
        'string_of_values "," value',
        'vector',
        'string_of_values "," vector'
    )
    def string_of_values(self, p):
        if len(p) == 1:
            values = [p[0]]
        else:
            values = p[0].values
            values.append(p[2])
        return AST.StringOfValues(values, p.lineno)

    @_(
        '"[" string_of_values "]"'
    )
    def vector(self, p):
        return AST.Vector(p[1], p.lineno)


    @_(
        'ID',
        'referance vector'
    )
    def referance(self, p):
        if len(p) == 1:
            return AST.IDRef(p[0], p.lineno)
        else:
            return AST.VectorCellRef(p[0], p[1], p.lineno)

    @_(
        'value',
        'rel_expr',
        'matrix_func',
       )
    def expr(self, p):
        return AST.Expr(p[0], p.lineno)

    @_(
        'SUB expr'
    )
    def expr(self, p):
        return AST.NegationRef(p[1], lineno=p.lineno)

    @_(
        'expr "\'"'
    )
    def expr(self, p):
        return AST.TransposeRef(p[0], lineno=p.lineno)

    # @_(
    #     'referance'
    # )
    # def expr(self, p):
    #     return AST.Expr(p[0], lineno=p.lineno)

    @_(
        'expr ADD expr',
        'expr SUB expr',
        'expr MUL expr',
        'expr DIV expr',
        'expr DOTADD expr',
        'expr DOTSUB expr',
        'expr DOTMUL expr',
        'expr DOTDIV expr',
        '"(" expr ")"'
    )
    def expr(self, p):
        return AST.BinExpr(p[0], p[1], p[2], p.lineno)

    @_(
        'expr LT expr',
        'expr GT expr',
        'expr LTE expr',
        'expr GTE expr',
        'expr EQ expr',
        'expr NEQ expr'
    )
    def rel_expr(self, p):
        return AST.RelExpr(p[0], p[1], p[2], p.lineno)

    @_(
        'referance "=" expr',
        'referance ADDASSIGN expr',
        'referance SUBASSIGN expr',
        'referance MULASSIGN expr',
        'referance DIVASSIGN expr'
    )
    def assign_expr(self, p):
        return AST.AssignExpr(p[0], p[1], p[2], p.lineno)



if __name__ == '__main__':
    lexer = MyScanner()
    parser = MyParser()

    # print("##### [TEST 1] #####")
    # with open("z2/ex1.txt") as file:
    #     data = file.read()
    #     ast = parser.parse(lexer.tokenize(data))
    #     ast.printTree()
    #
    # print("##### [TEST 2] #####")
    # with open("z2/ex2.txt") as file:
    #     data = file.read()
    #     ast = parser.parse(lexer.tokenize(data))
    #     ast.printTree()

    print("##### [TEST 3] #####")
    with open("z2/ex3.txt") as file:
        data = file.read()
        ast = parser.parse(lexer.tokenize(data))
        ast.printTree()