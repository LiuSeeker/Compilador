import sys
import re
from collections import defaultdict

class Token:
    def __init__(self, t, value):
        self.type = t
        self.value = value

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None
        self.line_n = 0
        self.selectNext()

    def selectNext(self):
        if self.position < len(self.origin):
            while self.origin[self.position] == " " or self.origin[self.position] is "\n":
                if self.origin[self.position] is "\n":
                    self.line_n += 1
                self.position += 1
                if self.position >= len(self.origin):
                    self.actual = Token("EOF", "")
                    return

            if self.origin[self.position].isdigit():
                i = self.position
                self.position += 1
                if self.position < len(self.origin): # N eficiente
                    while self.origin[self.position].isdigit():
                        self.position += 1
                        if self.position >= len(self.origin):
                            break
                self.actual = Token("INT", int(self.origin[i:self.position]))
                return
            elif self.origin[self.position] == "+":
                self.actual = Token("PLUS", "+")
                self.position += 1
                return
            elif self.origin[self.position] == "-":
                self.actual = Token("MINUS", "-")
                self.position += 1
                return
            elif self.origin[self.position] == "*":
                self.actual = Token("MULT", "*")
                self.position += 1
                return
            elif self.origin[self.position] == "/":
                self.actual = Token("DIV", "/")
                self.position += 1
                return
            elif self.origin[self.position] == "(":
                self.actual = Token("OPAR", "(")
                self.position += 1
                return
            elif self.origin[self.position] == ")":
                self.actual = Token("CPAR", ")")
                self.position += 1
                return
            elif self.origin[self.position] == "{":
                self.actual = Token("OCHA", "{")
                self.position += 1
                return
            elif self.origin[self.position] == "}":
                self.actual = Token("CCHA", "}")
                self.position += 1
                return
            elif self.origin[self.position] == ";":
                self.actual = Token("PVIR", ";")
                self.position += 1
                return
            elif self.origin[self.position] == "=":
                self.actual = Token("IGUA", "=")
                self.position += 1
                if self.origin[self.position] == "=":
                    self.actual = Token("IGUAR", "==")
                    self.position += 1
                return
            elif self.origin[self.position] == ">":
                self.actual = Token("MAIO", ">")
                self.position += 1
                return
            elif self.origin[self.position] == "<":
                self.actual = Token("MENO", "<")
                self.position += 1
                return
            elif self.origin[self.position] == "!":
                self.actual = Token("NOT", "!")
                self.position += 1
                return
            elif self.origin[self.position] == "$":
                i = self.position
                self.position += 1
                if self.origin[self.position].isalpha():
                    self.position += 1
                    if self.position < len(self.origin): # N eficiente
                        while self.origin[self.position].isdigit() or self.origin[self.position].isalpha() or self.origin[self.position] == "_":
                            self.position += 1
                            if self.position >= len(self.origin):
                                break
                self.actual = Token("IDEN", self.origin[i:self.position])
                return
            elif self.origin[self.position].isalpha():
                i = self.position
                self.position += 1
                if self.position < len(self.origin): # N eficiente
                    while self.origin[self.position].isalpha():
                        self.position += 1
                        if self.position >= len(self.origin):
                            break
                if self.origin[i:self.position].lower() == "echo":
                    self.actual = Token("ECHO", self.origin[i:self.position])
                    return
                elif self.origin[i:self.position].lower() == "or":
                    self.actual = Token("OR", self.origin[i:self.position])
                    return
                elif self.origin[i:self.position].lower() == "and":
                    self.actual = Token("AND", self.origin[i:self.position])
                    return
                elif self.origin[i:self.position].lower() == "while":
                    self.actual = Token("WHIL", self.origin[i:self.position])
                    return
                elif self.origin[i:self.position].lower() == "if":
                    self.actual = Token("IF", self.origin[i:self.position])
                    return
                elif self.origin[i:self.position].lower() == "else":
                    self.actual = Token("ELSE", self.origin[i:self.position])
                    return
                elif self.origin[i:self.position].lower() == "readline":
                    self.actual = Token("READ", self.origin[i:self.position])
                    return
                else:
                    raise SyntaxError("Keyword desconhecida {}".format(self.origin[i:self.position]))
            
            else:
                raise SyntaxError("Caractere nao permitido {}".format(self.origin[self.position]))
            
        else:
            self.actual = Token("EOF", "")


class Parser:
    tokens = None

    @staticmethod
    def parseBlock():
        if Parser.tokens.actual.type == "OCHA":
            ret = Comm()
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type != "CCHA":
                #print("NOVA LINHA")
                if Parser.tokens.actual.type == "EOF":
                    raise SyntaxError("Line {}: Fechamento de chaves esperado".format(Parser.tokens.line_n))
                ret_t = Parser.parseCommand()
                if ret_t is not None:
                    ret.children.append(ret_t)
            Parser.tokens.selectNext()
        else:
            raise SyntaxError("Line {}: Abertura de chaves esperado".format(Parser.tokens.line_n))
        
        return ret
    
    @staticmethod
    def parseCommand():
        #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
        if Parser.tokens.actual.type == "PVIR":
            ret = None
        elif Parser.tokens.actual.type == "OCHA":
            ret = Parser.parseBlock()
        elif Parser.tokens.actual.type == "IDEN":
            ret = Iden(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            if Parser.tokens.actual.type == "IGUA":
                ret = Assign(ret)
                Parser.tokens.selectNext()
                ret.children.append(Parser.parseRelationExpression())
                if Parser.tokens.actual.type == "PVIR":
                    #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
                    Parser.tokens.selectNext()
                else:
                    raise SyntaxError("Line {}: Ponto e virgula esperado".format(Parser.tokens.line_n))
            else:
                raise SyntaxError("Line {}: Assignment ('=') esperado".format(Parser.tokens.line_n))
            
        elif Parser.tokens.actual.type == "ECHO":
            ret = Echo()
            Parser.tokens.selectNext()
            ret.children.append(Parser.parseRelationExpression())
            if Parser.tokens.actual.type == "PVIR":
                #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
                Parser.tokens.selectNext()
            else:
                raise SyntaxError("Line {}: Ponto e virgula esperado".format(Parser.tokens.line_n))
        elif Parser.tokens.actual.type == "WHIL":
            ret = While()
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "OPAR":
                Parser.tokens.selectNext()
                ret.children.append(Parser.parseRelationExpression())
                if Parser.tokens.actual.type == "CPAR":
                    Parser.tokens.selectNext()
                    ret.children.append(Parser.parseCommand())
                else:
                    raise SyntaxError("Line {}: Fechamento de parenteses esperado".format(Parser.tokens.line_n))
            else:
                raise SyntaxError("Line {}: Abertura de parenteses esperado".format(Parser.tokens.line_n))
        elif Parser.tokens.actual.type == "IF":
            ret = If()
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "OPAR":
                Parser.tokens.selectNext()
                ret.children.append(Parser.parseRelationExpression())
                if Parser.tokens.actual.type == "CPAR":
                    Parser.tokens.selectNext()
                    ret.children.append(Parser.parseCommand())
                    if Parser.tokens.actual.type == "ELSE":
                        Parser.tokens.selectNext()
                        ret.children.append(Parser.parseCommand())
                else:
                    raise SyntaxError("Line {}: Fechamento de parenteses esperado".format(Parser.tokens.line_n))
            else:
                raise SyntaxError("Line {}: Abertura de parenteses esperado".format(Parser.tokens.line_n))
        else:
            raise SyntaxError("Line {}: Identifier, Echo ou Block esperado".format(Parser.tokens.line_n))

        return ret

    @staticmethod
    def parseRelationExpression():
        ret = Parser.parseExpression()
        while Parser.tokens.actual.type == "IGUAR" or Parser.tokens.actual.type == "MAIO" or Parser.tokens.actual.type == "MENO":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            ret = BinOp(Parser.tokens.actual.value, ret)
            Parser.tokens.selectNext()
            ret.children.append(Parser.parseExpression())
        
        return ret

    @staticmethod
    def parseExpression():
        ret = Parser.parseTerm()
        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "OR":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            ret = BinOp(Parser.tokens.actual.value, ret)
            Parser.tokens.selectNext()
            ret.children.append(Parser.parseTerm())
        
        return ret
    
    @staticmethod
    def parseTerm():        
        ret = Parser.parseFactor()
        while Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "AND":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            tmp_ret = BinOp(Parser.tokens.actual.value, ret)
            Parser.tokens.selectNext()
            tmp_ret.children.append(Parser.parseFactor())
            ret = tmp_ret
        
        return ret

    @staticmethod
    def parseFactor():
        if Parser.tokens.actual.type == "INT":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            ret = IntVal(int(Parser.tokens.actual.value))
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "NOT":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            ret = UnOp(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            ret.children.append(Parser.parseFactor())
        elif Parser.tokens.actual.type == "OPAR":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            ret = Parser.parseRelationExpression()
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            if Parser.tokens.actual.type != "CPAR":
                if Parser.tokens.actual.type == "INT":
                    raise SyntaxError("Line {}: Dois numeros seguidos".format(Parser.tokens.line_n))
                else:
                    raise SyntaxError("Line {}: Fechamento de parenteses esperado".format(Parser.tokens.line_n))
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == "IDEN":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            ret = Iden(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == "READ":
            ret_t = Readline()
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "OPAR":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "CPAR":
                    Parser.tokens.selectNext()
                    ret = ret_t
                else:
                    raise SyntaxError("Line {}: Fechamento de parenteses esperado apos readline".format(Parser.tokens.line_n))
            else:
                raise SyntaxError("Line {}: Parenteses esperado apos readline".format(Parser.tokens.line_n))
        
        
        elif Parser.tokens.actual.type == "EOF":
            raise SyntaxError("Line {}: Ultimo caractere operador".format(Parser.tokens.line_n))
        elif Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
            raise SyntaxError("Line {}: Dois operadores de multiplicacao e/ou divisiao seguidos".format(Parser.tokens.line_n))

        elif Parser.tokens.actual.type == "CPAR":
            raise SyntaxError("Fechamento de parentes desnecessario")
        else:
            print("WUT")
            print(Parser.tokens.actual.type)
            raise SyntaxError()
        
        return ret


    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        if Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
            raise SyntaxError("Line {}: Primeiro caractere operador nao permitido".format(Parser.tokens.line_n))
        ast = Parser.parseBlock()
        if Parser.tokens.actual.type != "EOF":
            if Parser.tokens.actual.type == "CPAR":
                raise SyntaxError("Line {}: Fechamento de parentes desnecessario".format(Parser.tokens.line_n))
            elif Parser.tokens.actual.type == "INT":
                raise SyntaxError("Line {}: Dois numeros seguidos".format(Parser.tokens.line_n))
        return ast

class PrePro:
    @staticmethod
    def filter(string):
        ## https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
        string = re.sub(re.compile("/\*.*?\*/",re.DOTALL) ,"" ,string) # remove all occurrences streamed comments (/*COMMENT */) from string
        #string = re.sub(re.compile("\\n",re.DOTALL), " ", string)
        return string

class Node:
    def __init__(self):
        self.value = None
        self.children = []
    
    def evaluate(self, st):
        raise NotImplementedError('subclasses must override evaluate()!')

class BinOp(Node):
    def __init__(self, value, c1):
        self.value = value
        self.children = [c1]

    def evaluate(self, st):
        if self.value == "+":
            return self.children[0].evaluate(st) + self.children[1].evaluate(st)
        elif self.value == "-":
            return self.children[0].evaluate(st) - self.children[1].evaluate(st)
        elif self.value == "*":
            return self.children[0].evaluate(st) * self.children[1].evaluate(st)
        elif self.value == "/":
            return self.children[0].evaluate(st) / self.children[1].evaluate(st)
        elif self.value == "==":
            return self.children[0].evaluate(st) is self.children[1].evaluate(st)
        elif self.value == ">":
            return self.children[0].evaluate(st) > self.children[1].evaluate(st)
        elif self.value == "<":
            return self.children[0].evaluate(st) < self.children[1].evaluate(st)
        elif self.value == "and":
            return self.children[0].evaluate(st) and self.children[1].evaluate(st)
        elif self.value == "or":
            return self.children[0].evaluate(st) or self.children[1].evaluate(st)
        else:
            print("BinOp Fail")

class UnOp(Node):
    def __init__(self, value):
        self.value = value
        self.children = []

    def evaluate(self, st):
        if self.value == "+":
            return self.children[0].evaluate(st)
        elif self.value == "-":
            return -self.children[0].evaluate(st)
        elif self.value == "!":
            return not self.children[0].evaluate(st)
        else:
            print("UnOp Fail")

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        return self.value

class NoOp(Node):
    def evaluate(self, st):
        pass

class Comm(Node):
    def evaluate(self, st):
        for c in self.children:
            c.evaluate(st)

class Assign(Node):
    def __init__(self, c1):
        self.children = [c1]

    def evaluate(self, st):
        st.setSymbol(self.children[0].value, self.children[1].evaluate(st))

class Iden(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        return st.getSymbol(self.value)

class Echo(Node):
    def evaluate(self, st):
        print(int(self.children[0].evaluate(st)))

class Readline(Node):
    def evaluate(self, st):
        return input()

class While(Node):    
    def evaluate(self, st):
        while self.children[0].evaluate(st):
            self.children[1].evaluate(st)

class If(Node):    
    def evaluate(self, st):
        if self.children[0].evaluate(st):
            self.children[1].evaluate(st)
        else:
            if len(self.children) > 2:
                self.children[2].evaluate(st)

class SymbolTable():
    def __init__(self):
        self.symbols = defaultdict(int)
    
    def setSymbol(self, symbol, value):
        self.symbols[symbol] = value
    
    def getSymbol(self, symbol):
        if symbol not in self.symbols.keys():
            raise NameError("{} nao definido".format(symbol))
        return int(self.symbols[symbol])


def main():
    if len(sys.argv) <= 1:
        raise SyntaxError("Sem argumentos")
    
    if sys.argv[1][-4:] != ".php":
        raise TypeError("Arquivo tem que ser .php")

    with open(sys.argv[1]) as f:
        code = f.read()

    code = PrePro.filter(code)

    ast = Parser.run(code)

    st = SymbolTable()

    ast.evaluate(st)

if __name__ == "__main__":
    main()