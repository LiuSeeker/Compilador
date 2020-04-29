# Compilador

*Ultima atualizacao README.md: 23/04*

#### Compilador de .php

Keywords disponíveis:
- "\<?php ?\>"
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
- "." concatenação

Exemplo de uso:
> python compilador.py exemplo_entrada.php

Diagrama sintático:

![Diagrama sintático](Diagrama-sintatico.png)

EBNF:
```
PROG = "<?php", COMM, "?>"
BLOC = "{", {COMM}, "}"
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
      | ("readline", "(", ")")
      | "true"
      | "false"
      | STRG
IDEN =  "$", letra, {( letra | num | "_" )}
STRG = '"', {letra}, '"'
```
