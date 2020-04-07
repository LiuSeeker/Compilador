# Compilador

*Ultima atualizacao README.md: 06/04*

#### Compilador de .php

Keywords disponíveis:
- "{ }" bloco
- "$" variável
- "echo"


Operadores disponíveis:
- "+"
- "-"
- "*"
- "/"
- "( )"

Exemplo de uso:
> python compilador.py exemplo_entrada.php

Diagrama sintático:

![Diagrama sintático](Diagrama-sintatico.png)

EBNF:
```
BLOC = "{", COMM, {COMM}, "}"
COMM = ( (IDEN, "=", EXPR) | ("echo", EXPR) | BLOC ), ";"
EXPR = TERM, {("+"|"-"), TERM}
TERM = FACT, {("*"|"/"), FACT}
FACT = ( num | (("+"|"-"), FACT) | ( "(", EXPR, ")" ) | IDEN )
IDEN =  "$", letra, {( letra | num | "_" )}
```
