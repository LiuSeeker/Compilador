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
            elif self.origin[self.position] == ",":
                self.actual = Token("VIRG", ",")
                self.position += 1
                return
            elif self.origin[self.position] == ".":
                self.actual = Token("PONT", ".")
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
                i = self.position
                self.position += 1
                if self.position < len(self.origin):
                    if self.origin[self.position] == "?":
                        while self.origin[self.position] != " " and self.origin[self.position] is not "\n":
                            self.position += 1
                            if self.position >= len(self.origin):
                                break
                        if self.origin[i:self.position] == "<?php":
                            self.actual = Token("OPRO", self.origin[i:self.position])
                        else:
                            raise SyntaxError("Keyword desconhecida {}".format(self.origin[i:self.position]))
                    else:
                        self.actual = Token("MENO", "<")
                        
                return
            elif self.origin[self.position] == "!":
                self.actual = Token("NOT", "!")
                self.position += 1
                return
            elif self.origin[self.position] == "?":
                i = self.position
                self.position += 1
                if self.position < len(self.origin):
                    if self.origin[self.position] == ">":
                        self.actual = Token("CPRO", self.origin[i:self.position])
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
                    self.actual = Token("ECHO", self.origin[i:self.position].lower())
                    return
                elif self.origin[i:self.position].lower() == "or":
                    self.actual = Token("OR", self.origin[i:self.position].lower())
                    return
                elif self.origin[i:self.position].lower() == "and":
                    self.actual = Token("AND", self.origin[i:self.position].lower())
                    return
                elif self.origin[i:self.position].lower() == "while":
                    self.actual = Token("WHIL", self.origin[i:self.position].lower())
                    return
                elif self.origin[i:self.position].lower() == "if":
                    self.actual = Token("IF", self.origin[i:self.position].lower())
                    return
                elif self.origin[i:self.position].lower() == "else":
                    self.actual = Token("ELSE", self.origin[i:self.position].lower())
                    return
                # elif self.origin[i:self.position].lower() == "readline":
                #     self.actual = Token("READ", self.origin[i:self.position].lower())
                #     return
                elif self.origin[i:self.position].lower() == "true":
                    self.actual = Token("TRUE", True)
                    return
                elif self.origin[i:self.position].lower() == "false":
                    self.actual = Token("FALSE", False)
                    return
                # elif self.origin[i:self.position].lower() == "function":
                #     self.actual = Token("FUND", "function")
                #     return
                # elif self.origin[i:self.position].lower() == "return":
                #     self.actual = Token("RET", "return")
                #     return
                else:
                    # while self.origin[self.position].isdigit() or self.origin[self.position].isalpha() or self.origin[self.position] == "_":
                    #     self.position += 1
                    #     if self.position >= len(self.origin):
                    #         break
                    # if self.origin[self.position] == "(":
                    #     self.actual = Token("IDEF", self.origin[i:self.position].lower())
                    # else:
                    #     raise SyntaxError("Keyword desconhecida {}".format(self.origin[i:self.position]))
                    raise SyntaxError("Keyword desconhecida {}".format(self.origin[i:self.position]))
            # elif self.origin[self.position] == '"':
            #     i = self.position
            #     self.position += 1
            #     if self.position < len(self.origin):
            #         while self.origin[self.position] != '"':
            #             self.position += 1
            #             if self.position >= len(self.origin):
            #                 break
            #         self.actual = Token("STRG", self.origin[i+1:self.position])
            #         self.position += 1
            #     return
            
            else:
                raise SyntaxError("Caractere nao permitido {}".format(self.origin[self.position]))
            
        else:
            self.actual = Token("EOF", "")


class Parser:
    tokens = None
    id_n = 0

    @staticmethod
    def parseProgram():
        if Parser.tokens.actual.type == "OPRO":
            ret = Comm()
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type != "CPRO":
                #print("NOVA LINHA")
                if Parser.tokens.actual.type == "EOF":
                    raise SyntaxError("Line {}: Fechamento ?> esperado".format(Parser.tokens.line_n))
                ret_t = Parser.parseCommand()
                if ret_t is not None:
                    ret.children.append(ret_t)
            Parser.tokens.selectNext()
        else:
            raise SyntaxError("Line {}: Abertura de <?php esperado".format(Parser.tokens.line_n))
        
        return ret

    @staticmethod
    def parseBlock():
        if Parser.tokens.actual.type == "OCHA":
            ret = Comm()
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type != "CCHA":
                #print(Parser.tokens.actual.type, Parser.tokens.actual.value, Parser.tokens.line_n)
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
        # Ponto e Virgula
        if Parser.tokens.actual.type == "PVIR":
            ret = None
            Parser.tokens.selectNext()
        # Open Parenteses
        elif Parser.tokens.actual.type == "OCHA":
            ret = Parser.parseBlock()
        # Identifier
        elif Parser.tokens.actual.type == "IDEN":
            ret = Iden(Parser.tokens.actual.value, Parser.id_n)
            Parser.id_n += 1
            Parser.tokens.selectNext()
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            if Parser.tokens.actual.type == "IGUA":
                ret = Assign(ret, Parser.id_n)
                Parser.id_n += 1
                Parser.tokens.selectNext()
                ret.children.append(Parser.parseRelationExpression())
                if Parser.tokens.actual.type == "PVIR":
                    #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
                    Parser.tokens.selectNext()
                else:
                    raise SyntaxError("Line {}: Ponto e virgula esperado".format(Parser.tokens.line_n))
            else:
                raise SyntaxError("Line {}: Assignment ('=') esperado".format(Parser.tokens.line_n))
        # Echo
        elif Parser.tokens.actual.type == "ECHO":
            ret = Echo()
            Parser.tokens.selectNext()
            ret.children.append(Parser.parseRelationExpression())
            if Parser.tokens.actual.type == "PVIR":
                #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
                Parser.tokens.selectNext()
            else:
                raise SyntaxError("Line {}: Ponto e virgula esperado".format(Parser.tokens.line_n))
        # While
        elif Parser.tokens.actual.type == "WHIL":
            ret = While(Parser.id_n)
            Parser.id_n += 1
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
        # If
        elif Parser.tokens.actual.type == "IF":
            ret = If(Parser.id_n)
            Parser.id_n += 1
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
        # Declaracao function
        # elif Parser.tokens.actual.type == "FUND":
        #     ret = FuncDef()
        #     Parser.tokens.selectNext()
        #     if Parser.tokens.actual.type == "IDEF":
        #         ret.value = Parser.tokens.actual.value
        #         Parser.tokens.selectNext()
        #         if Parser.tokens.actual.type == "OPAR":
        #             Parser.tokens.selectNext()
        #             if Parser.tokens.actual.type == "CPAR":
        #                 Parser.tokens.selectNext()
        #             else:
        #                 if Parser.tokens.actual.type == "IDEN":
        #                     ret.children.append(Iden(Parser.tokens.actual.value, Parser.id_n))
        #                     Parser.id_n += 1
        #                     Parser.tokens.selectNext()
        #                 else:
        #                     raise SyntaxError("Line {}: Identifier esperado".format(Parser.tokens.line_n))
        #                 while Parser.tokens.actual.type == "VIRG":
        #                     Parser.tokens.selectNext()
        #                     if Parser.tokens.actual.type == "IDEN":
        #                         ret.children.append(Iden(Parser.tokens.actual.value, Parser.id_n))
        #                         Parser.id_n += 1
        #                         Parser.tokens.selectNext()
        #                     else:
        #                         raise SyntaxError("Line {}: Identifier esperado".format(Parser.tokens.line_n))
        #                 if Parser.tokens.actual.type == "CPAR":
        #                     Parser.tokens.selectNext()
        #                 else:
        #                     raise SyntaxError("Line {}: Fechamento de parenteses esperado".format(Parser.tokens.line_n))
        #             ret.children.append(Parser.parseBlock())
        #         else:
        #             raise SyntaxError("Line {}: Abertura de parenteses esperado".format(Parser.tokens.line_n))
        #     else:
        #         raise SyntaxError("Line {}: Identifier esperado".format(Parser.tokens.line_n))
        # Funcion call
        # elif Parser.tokens.actual.type == "IDEF":
        #     ret = FuncCall(Parser.tokens.actual.value, Parser.id_n)
        #     Parser.id_n += 1
        #     Parser.tokens.selectNext()
        #     if Parser.tokens.actual.type == "OPAR":
        #         Parser.tokens.selectNext()
        #         if Parser.tokens.actual.type == "CPAR":
        #             Parser.tokens.selectNext()
        #         else:
        #             ret.children.append(Parser.parseRelationExpression())
        #             while Parser.tokens.actual.type == "VIRG":
        #                 Parser.tokens.selectNext()
        #                 ret.children.append(Parser.parseRelationExpression())
        #             if Parser.tokens.actual.type == "CPAR":
        #                 Parser.tokens.selectNext()
        #             else:
        #                 raise SyntaxError("Line {}: Fechamento de parenteses esperado".format(Parser.tokens.line_n))
        # Return
        # elif Parser.tokens.actual.type == "RET":
        #     ret = Return(Parser.tokens.actual.value, Parser.id_n)
        #     Parser.id_n += 1
        #     Parser.tokens.selectNext()
        #     ret.children.append(Parser.parseRelationExpression())

        else:
            raise SyntaxError("Line {}: Identifier, Echo, While ou If esperado".format(Parser.tokens.line_n))
        

        return ret

    @staticmethod
    def parseRelationExpression():
        ret = Parser.parseExpression()
        while Parser.tokens.actual.type == "IGUAR" or Parser.tokens.actual.type == "MAIO" or Parser.tokens.actual.type == "MENO":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            ret = BinOp(Parser.tokens.actual.value, ret, Parser.id_n)
            Parser.id_n += 1
            Parser.tokens.selectNext()
            ret.children.append(Parser.parseExpression())
        
        return ret

    @staticmethod
    def parseExpression():
        ret = Parser.parseTerm()
        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "OR": #or Parser.tokens.actual.type == "PONT":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            ret = BinOp(Parser.tokens.actual.value, ret, Parser.id_n)
            Parser.id_n += 1
            Parser.tokens.selectNext()
            ret.children.append(Parser.parseTerm())
        
        return ret
    
    @staticmethod
    def parseTerm():        
        ret = Parser.parseFactor()
        while Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "AND":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            tmp_ret = BinOp(Parser.tokens.actual.value, ret, Parser.id_n)
            Parser.id_n += 1
            Parser.tokens.selectNext()
            tmp_ret.children.append(Parser.parseFactor())
            ret = tmp_ret
        
        return ret

    @staticmethod
    def parseFactor():
        if Parser.tokens.actual.type == "INT":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            ret = IntVal(int(Parser.tokens.actual.value), Parser.id_n)
            Parser.id_n += 1
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "NOT":
            #print("    ",Parser.tokens.actual.type, Parser.tokens.actual.value)
            ret = UnOp(Parser.tokens.actual.value, Parser.id_n)
            Parser.id_n += 1
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
            ret = Iden(Parser.tokens.actual.value, Parser.id_n)
            Parser.id_n += 1
            Parser.tokens.selectNext()
        
        # # Funcion call
        # elif Parser.tokens.actual.type == "IDEF":
        #     ret = FuncCall(Parser.tokens.actual.value, Parser.id_n)
        #     Parser.id_n += 1
        #     Parser.tokens.selectNext()
        #     if Parser.tokens.actual.type == "OPAR":
        #         Parser.tokens.selectNext()
        #         if Parser.tokens.actual.type == "CPAR":
        #             Parser.tokens.selectNext()
        #         else:
        #             ret.children.append(Parser.parseRelationExpression())
        #             while Parser.tokens.actual.type == "VIRG":
        #                 Parser.tokens.selectNext()
        #                 ret.children.append(Parser.parseRelationExpression())
        #             if Parser.tokens.actual.type == "CPAR":
        #                 Parser.tokens.selectNext()
        #             else:
        #                 raise SyntaxError("Line {}: Fechamento de parenteses esperado".format(Parser.tokens.line_n))
        
        # elif Parser.tokens.actual.type == "READ":
        #     ret_t = Readline()
        #     Parser.tokens.selectNext()
        #     if Parser.tokens.actual.type == "OPAR":
        #         Parser.tokens.selectNext()
        #         if Parser.tokens.actual.type == "CPAR":
        #             Parser.tokens.selectNext()
        #             ret = ret_t
        #         else:
        #             raise SyntaxError("Line {}: Fechamento de parenteses esperado apos readline".format(Parser.tokens.line_n))
        #     else:
        #         raise SyntaxError("Line {}: Parenteses esperado apos readline".format(Parser.tokens.line_n))
        # elif Parser.tokens.actual.type == "STRG":
        #     ret = StringVal(Parser.tokens.actual.value, Parser.id_n)
        #     Parser.id_n += 1
        #     Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == "TRUE" or Parser.tokens.actual.type == "FALSE":
            ret = BoolVal(Parser.tokens.actual.value, Parser.id_n)
            Parser.id_n += 1
            Parser.tokens.selectNext()
        
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
        ast = Parser.parseProgram()
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
        self.id_n = None
    
    def evaluate(self, st):
        raise NotImplementedError('subclasses must override evaluate()!')

class BinOp(Node):
    def __init__(self, value, c1, id_n):
        self.value = value
        self.children = [c1]
        self.id_n = id_n

    def evaluate(self, st):
        self.children[0].evaluate(st)
        Nasm.write("PUSH EBX")
        self.children[1].evaluate(st)
        Nasm.write("POP EAX")
        
        # aritmeticos
        if self.value == "+":
            Nasm.write("ADD EAX, EBX")
        elif self.value == "-":
            Nasm.write("SUB EAX, EBX")
        elif self.value == "*":
            Nasm.write("IMUL EAX, EBX")
        elif self.value == "/":
            Nasm.write("IDIV EAX, EBX")
            Nasm.write(" EAX, EBX")
        # booleanos
        elif self.value == ">":
            Nasm.write("CMP EAX, EBX")
            Nasm.write("JG J{}".format(self.id_n))
            Nasm.write("MOV EAX, False")
            Nasm.write("JMP E{}".format(self.id_n))
            Nasm.write("J{}:".format(self.id_n))
            Nasm.write("MOV EAX, True")
            Nasm.write("E{}:".format(self.id_n))
        elif self.value == "<":
            Nasm.write("CMP EAX, EBX")
            Nasm.write("JL J{}".format(self.id_n))
            Nasm.write("MOV EAX, False")
            Nasm.write("JMP E{}".format(self.id_n))
            Nasm.write("J{}:".format(self.id_n))
            Nasm.write("MOV EAX, True")
            Nasm.write("E{}:".format(self.id_n))
        elif self.value == "==":
            Nasm.write("CMP EAX, EBX")
            Nasm.write("JE J{}".format(self.id_n))
            Nasm.write("MOV EAX, False")
            Nasm.write("JMP E{}".format(self.id_n))
            Nasm.write("J{}:".format(self.id_n))
            Nasm.write("MOV EAX, True")
            Nasm.write("E{}:".format(self.id_n))
        
        elif self.value == "and":
            Nasm.write("AND EAX, EBX")
        elif self.value == "or":
            Nasm.write("OR EAX, EBX")
        # strings
        #elif self.value == ".":
        #    Nasm.write(" EAX, EBX")
        else:
            raise TypeError("BinOp Fail ({})".format(self.value))

        Nasm.write("MOV EBX, EAX")
        
        Nasm.write("")

        

class UnOp(Node):
    def __init__(self, value, id_n):
        self.value = value
        self.children = []
        self.id_n = id_n

    def evaluate(self, st):
        self.children[0].evaluate(st)
        if self.value == "+":
            Nasm.write("MOV EAX, EBX")
        elif self.value == "-":
            Nasm.write("NEG EBX")
            Nasm.write("MOV EAX, EBX")
        elif self.value == "!":
            Nasm.write("CMP EBX, True")
            Nasm.write("JE J{}".format(self.id_n))
            Nasm.write("MOV EAX, True")
            Nasm.write("JMP E{}".format(self.id_n))
            Nasm.write("J{}:".format(self.id_n))
            Nasm.write("MOV EAX, False")
            Nasm.write("E{}:".format(self.id_n))
        else:
            raise TypeError("UnOp Fail ({})".format(self.value))

        Nasm.write("MOV EBX, EAX")
        Nasm.write("")

class IntVal(Node):
    def __init__(self, value, id_n):
        self.value = value
        self.id = id_n

    def evaluate(self, st):
        Nasm.write("MOV EBX, {}".format(self.value))
        Nasm.write("")

class BoolVal(Node):
    def __init__(self, value, id_n):
        self.value = value
        self.id_n = id_n

    def evaluate(self, st):
        return ("bool", self.value)

# class StringVal(Node):
#     def __init__(self, value, id_n):
#         self.value = value
#         self.id_n = id_n

    # def evaluate(self, st):
    #     return ("string", self.value)

class NoOp(Node):
    def evaluate(self, st):
        pass

class Comm(Node):
    def evaluate(self, st):
        for c in self.children:
            c.evaluate(st)
            if "return" in st.symbols.keys():
                break

class Assign(Node):
    def __init__(self, c1, id_n):
        self.children = [c1]
        self.id_n = id_n

    def evaluate(self, st):
        id_name = self.children[0].value
        if id_name not in list(st.symbols.keys()):
            st.setSymbol(id_name)
            Nasm.write("PUSH DWORD 0")
            self.children[1].evaluate(st)
            Nasm.write("MOV [EBP-{}], EBX".format(st.getSymbol(id_name)*4))
        else:
            self.children[1].evaluate(st)
            Nasm.write("MOV [EBP-{}], EBX".format(st.getSymbol(id_name)*4))
        Nasm.write("")

class Iden(Node):
    def __init__(self, value, id_n):
        self.value = value
        self.id_n = id_n

    def evaluate(self, st):
        Nasm.write("MOV EBX, [EBP-{}]".format(st.getSymbol(self.value)*4))
        Nasm.write("")

class Echo(Node):
    def evaluate(self, st):
        self.children[0].evaluate(st)
        Nasm.write("PUSH EBX")
        Nasm.write("CALL print")
        Nasm.write("POP EBX")
        Nasm.write("")
        
# class Readline(Node):
#     def evaluate(self, st):
#         inp = input()
#         try:
#             inp = int(inp)
#         except ValueError:
#             raise TypeError("readline tem que ser 'int'")
#         return ("int", inp)

class While(Node):
    def __init__(self, id_n):
        self.id_n = id_n
        self.children = []

    def evaluate(self, st):
        Nasm.write("WHILE{}:".format(self.id_n))

        self.children[0].evaluate(st)

        Nasm.write("CMP EBX, False")
        Nasm.write("JE E{}".format(self.id_n))

        self.children[1].evaluate(st)
        
        Nasm.write("JMP WHILE{}".format(self.id_n))
        
        Nasm.write("E{}:".format(self.id_n))
        Nasm.write("")

class If(Node):
    def __init__(self, id_n):
        self.id_n = id_n
    def evaluate(self, st):
        self.children[0].evaluate(st)

        Nasm.write("CMP EBX, False")
        Nasm.write("JE E{}".format(self.id_n))

        self.children[1].evaluate(st)

        Nasm.write("E{}:".format(self.id_n))
        Nasm.write("")

# class FuncDef(Node):
#     def evaluate(self, st):
#         FuncTable.setSymbol(self.value, self)

# class FuncCall(Node):
#     def __init__(self, value, id_n):
#         self.value = value
#         self.children = []
#         self.id_n = id_n

#     def evaluate(self, st):
#         func = FuncTable.getSymbol(self.value)
#         if len(func.children)-1 != len(self.children):
#             raise TypeError("{}() recebe {} args, recebeu {}".format(self.value, len(func.children)-1, len(self.children)))
#         stn = SymbolTable()
#         # set Symbols
#         for i in range(len(self.children)):
#             stn.setSymbol(func.children[i].value, self.children[i].evaluate(st))
#         func.children[-1].evaluate(stn)
#         if "return" in stn.symbols.keys():
#             return stn.getSymbol("return")
#         return None

# class Return(Node):
#     def __init__(self, value, id_n):
#         self.value = value
#         self.children = []
#         self.id_n = id_n

#     def evaluate(self, st):
#         st.setSymbol(self.value, self.children[0].evaluate(st))

class SymbolTable():
    def __init__(self):
        self.symbols = defaultdict(tuple)
        self.desl = 1
    
    def setSymbol(self, symbol):
        self.symbols[symbol] = self.desl
        self.desl += 1
    
    def getSymbol(self, symbol):
        if symbol not in self.symbols.keys():
            raise NameError("{} nao definido".format(symbol))
        return self.symbols[symbol]

# class FuncTable():
#     funcs = defaultdict(Node)
    
#     @staticmethod
#     def setSymbol(symbol, node):
#         if symbol in FuncTable.funcs.keys():
#             raise NameError("{}() ja definido".format(symbol))
#         FuncTable.funcs[symbol] = node
    
#     @staticmethod
#     def getSymbol(symbol):
#         if symbol not in FuncTable.funcs.keys():
#             raise NameError("{}() nao definido".format(symbol))
#         return FuncTable.funcs[symbol]

class Nasm():
    text = []

    @staticmethod
    def write(t):
        Nasm.text.append("  " + t + "\n")


def main():
    with open("modelo_copia.asm") as f:
        modelo = f.readlines()
    
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

    nline = 83
    for line in Nasm.text:
        modelo.insert(nline, line)
        nline += 1

    print("".join(modelo))


if __name__ == "__main__":
    main()