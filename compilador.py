import sys

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
            
            else:
                raise SyntaxError("Caractere nao permitido {}".format(self.origin[self.position]))
            
        else:
            self.actual = Token("EOF", "")


class Parser:
    tokens = None
    
    @staticmethod
    def parseExpression():
        ret = 0
        
        if Parser.tokens.actual.type == "INT":
            ret = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
                if Parser.tokens.actual.value == "+":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        ret += Parser.tokens.actual.value
                    elif Parser.tokens.actual.type == "EOF":
                        raise SyntaxError("Ultimo caractere operador")
                    else:
                        raise SyntaxError("Dois operadores seguidos")
                elif Parser.tokens.actual.value == "-":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        ret -= Parser.tokens.actual.value
                    elif Parser.tokens.actual.type == "EOF":
                        raise SyntaxError("Ultimo caractere operador")
                    else:
                        raise SyntaxError("Dois operadores seguidos")
                Parser.tokens.selectNext()
            
            return ret

        else:
            raise SyntaxError("Primeiro caractere operador")

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        result = Parser.parseExpression()
        if Parser.tokens.actual.type != "EOF":
            raise SyntaxError("Dois numeros seguidos")
        return result

def main():
   
    if len(sys.argv) <= 1:
        raise SyntaxError("Sem argumentos")

    code = "".join(sys.argv[1:])

    result = Parser.run(code)
    print("R: {}".format(result))

if __name__ == "__main__":
    main()