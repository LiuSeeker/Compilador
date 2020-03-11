import sys
import re

class Token:
    def __init__(self, t, value):
        self.type = t
        self.value = value

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None
        self.selectNext()

    def selectNext(self):
        if self.position < len(self.origin):
            while self.origin[self.position] == " ":
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
            
            else:
                raise SyntaxError("Caractere nao permitido {}".format(self.origin[self.position]))
            
        else:
            self.actual = Token("EOF", "")


class Parser:
    tokens = None
    
    @staticmethod
    def parseTerm():
        ret = 0
        
        ret = Parser.parseFactor()
        while Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
            if Parser.tokens.actual.value == "*":
                Parser.tokens.selectNext()
                ret *= Parser.parseFactor()
            elif Parser.tokens.actual.value == "/":
                Parser.tokens.selectNext()
                ret /= Parser.parseFactor()
        
        return ret
    
    @staticmethod
    def parseExpression():
        ret = 0
        
        ret = Parser.parseTerm()
        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                print("tika")
                ret += Parser.parseTerm()
            elif Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                ret -= Parser.parseTerm()
        
        return ret

    @staticmethod
    def parseFactor():
        print(Parser.tokens.actual.type, Parser.tokens.actual.value)
        if Parser.tokens.actual.type == "INT":
            ret = Parser.tokens.actual.value
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                ret = 1 * Parser.parseFactor()
            elif Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                ret = -1 * Parser.parseFactor()
        elif Parser.tokens.actual.type == "OPAR":
            Parser.tokens.selectNext()
            ret = Parser.parseExpression()
            
            if Parser.tokens.actual.type != "CPAR":
                if Parser.tokens.actual.type == "INT":
                    raise SyntaxError("Dois numeros seguidos")
                else:
                    raise SyntaxError("Fechamento de parenteses esperado")
            Parser.tokens.selectNext()
        
        elif Parser.tokens.actual.type == "EOF":
            raise SyntaxError("Ultimo caractere operador")
        elif Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
            raise SyntaxError("Dois operadores de multiplicacao e/ou divisiao seguidos")

        elif Parser.tokens.actual.type == "CPAR":
            raise SyntaxError("Fechamento de parentes desnecessario")
        
        return ret

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        if Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
            raise SyntaxError("Primeiro caractere operador nao permitido")
        result = Parser.parseExpression()
        if Parser.tokens.actual.type != "EOF":
            if Parser.tokens.actual.type == "CPAR":
                raise SyntaxError("Fechamento de parentes desnecessario")
            elif Parser.tokens.actual.type == "INT":
                raise SyntaxError("Dois numeros seguidos")
        return result

class PrePro:
    @staticmethod
    def filter(string):
        ## https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
        string = re.sub(re.compile("/\*.*?\*/",re.DOTALL) ,"" ,string) # remove all occurrences streamed comments (/*COMMENT */) from string
        return string

def main():
   
    if len(sys.argv) <= 1:
        raise SyntaxError("Sem argumentos")
    
    code = "".join(sys.argv[1:])    

    code = PrePro.filter(code)

    result = Parser.run(code)
    print(result)

if __name__ == "__main__":
    main()