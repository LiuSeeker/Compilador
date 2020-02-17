import sys

NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
OPERATORS = ["+", "-"]

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def parser(arg, op_index):
    # Ta redundante em algum lugar
    if op_index == len(OPERATORS):
        return arg
    temp = []

    arg2 = arg.split(OPERATORS[op_index])
    if arg == arg2:
        return arg
    string = intersperse(arg2, OPERATORS[op_index])
    for e in string:
        parser_result = parser(e, op_index+1)
        if type(parser_result) is not list:
            parser_result = [parser_result]
        temp = temp + parser_result
    return temp

def main():
    
    if len(sys.argv) <= 1:
        raise SyntaxError("Sem argumentos")

    # Parser
    total = []
    for arg in sys.argv[1:]:
        op_index = 0
        total = total + parser(arg, op_index)
    while True:
        try:
            total.remove("")
        except ValueError:
            break

    total_len = len(total)

    if total_len < 3:
        raise SyntaxError("Sem informacao suficiente")

    # Verificador léxico e sintático
    for i in range(total_len):
        if i == 0:
            if total[i] in OPERATORS:
                raise SyntaxError("Primeiro caractere operador")

        elif i == total_len-1:
            if total[i] in OPERATORS:
                raise SyntaxError("Ultimo caractere operador")

        if i < total_len-1:
            if total[i] in OPERATORS and total[i+1] in OPERATORS:
                raise SyntaxError("Dois operadores seguidos")

        for char in total[i]:
            if char not in NUMBERS and char not in OPERATORS:
                raise SyntaxError("Caractere nao permitido {}".format(char))
    
    # Calculo
    result = 0
    i = 0
    while i < total_len:
        if i == 0:
            result += int(total[i])
            i += 1
            continue
        elif total[i] == "+":
            result += int(total[i+1])
        elif total[i] == "-":
            result -= int(total[i+1])
        else:
            raise SyntaxError("Dois numeros seguidos")
        i += 2

    print(result)

if __name__ == "__main__":
    main()