# Compilador

*Ultima atualizacao README.md: 23/04*

#### Compilador de .php

Keywords disponíveis:
- "{ }" bloco
- "$" variável
- "echo"
- "while"
- "if" e "else"
- "readline"

Operadores disponíveis:
- "+"
- "-"
- "*"
- "/"
- "( )"
- "=="
- ">"
- "<"
- "or"
- "and"
- "!"

Exemplo de uso:
> python compilador.py exemplo_entrada.php

Diagrama sintático:

![Diagrama sintático](Diagrama-sintatico.png)

EBNF:
```
BLOC = "{", COMM, {COMM}, "}"
COMM = (IDEN, "=", EXPR, ";")
      | ("echo", EXPR, ";")
      | BLOC
      | ("while", "(", RELE, ")", COMM)
      | ("if", "(", RELE, ")", COMM)
      | ("if", "(", RELE, ")", COMM, "else", COMM)
RELE = EXPR, {("=="|">"|"<"), EXPR}
EXPR = TERM, {("+"|"-"|"or"), TERM}
TERM = FACT, {("*"|"/"|"and"), FACT}
FACT = num
      | (("+"|"-"|"!"), FACT)
      | ( "(", RELE, ")" )
      | IDEN
      | "readline"
IDEN =  "$", letra, {( letra | num | "_" )}
```
