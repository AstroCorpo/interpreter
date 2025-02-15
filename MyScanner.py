from sly import Lexer


class MyScanner(Lexer):
    def __init__(self):
        self.nesting_level = 0

    tokens = {
        ID,
        IF,
        ELSE,
        WHILE,
        FOR,
        BREAK,
        CONTINUE,
        RETURN,
        EYE,
        ZEROS,
        ONES,
        PRINT,
        INTNUM,
        FLOATNUM,

        MULASSIGN,
        SUBASSIGN,
        ADDASSIGN,
        DIVASSIGN,

        DOTADD,
        DOTSUB,
        DOTMUL,
        DOTDIV,

        ADD,
        SUB,
        MUL,
        DIV,

        LT,
        GT,
        LTE,
        GTE,
        EQ,
        NEQ,

        STRING
    }

    ignore = " \t"
    ignore_comment = "#.*"

    LTE = r"<="
    GTE = r">="
    LT = r"<"
    GT = r">"
    EQ = r"=="
    NEQ = r"!="

    MULASSIGN = r"\*="
    SUBASSIGN = r"-="
    ADDASSIGN = r"\+="
    DIVASSIGN = r"/="

    DOTADD = r"\.\+"
    DOTSUB = r"\.-"
    DOTMUL = r"\.\*"
    DOTDIV = r"\./"

    ADD = r"\+"
    SUB = r"-"
    MUL = r"\*"
    DIV = r"/"

    literals = {'(', ')', '{', '}', '[', ']', ',', ';', ':', '\'', '='}

    STRING = r"\".*\""

    ID = r"[a-zA-Z_][\w_]*"
    ID["if"] = IF
    ID["else"] = ELSE
    ID["while"] = WHILE
    ID["for"] = FOR
    ID["break"] = BREAK
    ID["continue"] = CONTINUE
    ID["return"] = RETURN
    ID["eye"] = EYE
    ID["zeros"] = ZEROS
    ID["ones"] = ONES
    ID["print"] = PRINT

    @_(r'[\{\[\(]')
    def lbrace(self, t):
        t.type = t.value
        self.nesting_level += 1
        return t

    @_(r'[\}\]\)]')
    def rbrace(self, t):
        t.type = t.value
        self.nesting_level -= 1
        return t

    @_(r"[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?|\d+\.")
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    @_(r"\d+")
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

    @_(r'[\d\.\?]+[a-zA-Z]*')
    def bad_token(self, t):
        print(f"ERROR: Unknown token at line {self.lineno}: {t.value}")

if __name__ == "__main__":
    with open("z2/ex3.txt") as f:
        data = f.read()

        lexer = MyScanner()
        tokens = lexer.tokenize(data)

        for tok in tokens:
            print(f"({tok.lineno}): {tok.type}({tok.value})")

        if (lexer.nesting_level != 0):
            print("Error: braces are not nested correctly")
