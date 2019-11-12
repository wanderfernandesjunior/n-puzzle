# n-puzzle

Solução do problema n-puzzle (busca com A* e três tipos de heurísticas)

ENTRADA: O programa lê três parâmetros:
- n: grau da matriz
- heuristica:
    h1 (número de pastilhas no lugar errado),
    h2 (soma das distâncias até a posição meta de cada pastilha) ou
    h3 (heurística de Gaschnig)
- condição inicial do tabuleiro

SAÍDA: o programa retorna a primeira solução encontrada, por exemplo:

    localhost:~$ ./npuzzle
    3 h2
    0 1 3 4 2 5 7 8 6
    ----- INIT -----
    0 1 3 4 2 5 7 8 6
    1 0 3 4 2 5 7 8 6
    1 2 3 4 0 5 7 8 6
    1 2 3 4 5 0 7 8 6
    1 2 3 4 5 6 7 8 0
    ----- GOAL -----
    
Referências consultadas:
    
 - Livro AIMA - "Artificial Intelligence - A Modern Approach"
 - Livro "Introdução aos Métodos Heurísticos de Otimização com Python"
 - Github oficial do livro AIMA (https://github.com/aimacode)
 - Documentação do Python (https://docs.python.org)
 - Página "Introduction to the A* Algorithm"
 (https://www.redblobgames.com/pathfinding/a-star/introduction.html)
