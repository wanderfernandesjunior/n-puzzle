#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" npuzzle.py
Referências consultadas:
 - Livro AIMA - "Artificial Intelligence - A Modern Approach"
 - Livro "Introdução aos Métodos Heurísticos de Otimização com Python"
 - Github oficial do livro AIMA (https://github.com/aimacode)
 - Documentação do Python (https://docs.python.org)
 - Página "Introduction to the A* Algorithm"
 (https://www.redblobgames.com/pathfinding/a-star/introduction.html)"""
import heapq  # usado para buscar próximo estado com menor f(n)
from random import randint  # usado na heuristica h3.


def ler_entrada():
    """
    Lê três parâmetros em linha de comando:
    - n: grau da matriz
    - heuristica:
        h1 (número de pastilhas no lugar errado),
        h2 (soma das distâncias até a posição meta de cada pastilha) ou
        h3 (heurística de Gaschnig)
    - condição inicial do tabuleiro"""
    while True:
        try:
            parametros = input()
            n = int(parametros.split(" ")[0])
            heuristica = str(parametros.split(" ")[1])
            if validar_parametros(n, heuristica):
                break
        except Exception as erro:
                print(f"Erro: {erro}")

    while True:
        try:
            condicaoinicial = input().split()
            condicaoinicial = [int(i) for i in condicaoinicial]
            if validar_tabuleiro_inicial(n, condicaoinicial):
                break
        except Exception as erro:
                print(f"Erro: {erro}")

    return n, heuristica, condicaoinicial


def validar_parametros(n, heuristica):
    """
    Valida os dois parâmetros em linha de comando:
    - n: numero inteiro maior ou igual a 3
    - heuristica: string "h1", "h2" ou "h3" """
    if n < 3:
        print("Erro: O grau da matriz n deve ser maior ou igual a 3.")
        return False
    if heuristica not in ["h1", "h2", "h3"]:
        print("Erro: O tipo de heurística deve ser h1, h2 ou h3.")
        return False
    return True


def validar_tabuleiro_inicial(n, condicaoinicial):
    """    Valida os dados entrados de tabuleiro:
    - condicaoinicial: valor 0 na posição vazia e m=n^2-1 valores de 1 a m"""
    if len(condicaoinicial) != n**2:
        print("Erro: Quantidade de posições informadas para condição inicial do tabuleiro inválida.")
        return False
    if not all([numero in condicaoinicial for numero in range(n**2)]):
        print("Erro: Valores das posições informadas para condição inicial do tabuleiro inválidas.")
        return False
    return True


def tabuleiro_solucionavel(n, condicaoinicial):
    """    Verifica se o tabuleiro de entrada é solucionável ou não:
    - quando n é ímpar, uma tabuleiro n-por-n é solucionével se e somente se seu número de inversões for par.
    - quando n é par, um tabuleiro n-por-n é solucionével se e somente se o número de inversões mais
    a linha do quadrado vazio for ímpar."""
    inversoes = 0
    linha_quadrado_vazio = condicaoinicial.index(0) // n

    for i in range(len(condicaoinicial)):
        for j in range(i+1, len(condicaoinicial)):
            if (condicaoinicial[i] > condicaoinicial[j]) and condicaoinicial[i] != 0 and condicaoinicial[j] != 0:
                inversoes += 1

    if(n % 2 != 0 and inversoes % 2 != 0):    # n ímpar e inversoes ímpar
        print("UNSOLVABLE")
        return False
    elif (n % 2 == 0 and (inversoes + linha_quadrado_vazio) % 2 == 0):    # n par e (inversoes+linha_quadrado_vazio) par
        print("UNSOLVABLE")
        return False
    else:
        return True


def caminhoEstado(no):
    "Sequencia de estados para chegar a um determinado No."
    if no is None:
        return []
    return caminhoEstado(no.pai) + [no.estado]


def h1(no, objetivo):
    """ Heurística que conta o número de pastilhas no lugar errado."""
    soma = 0
    for (estado, objetivo) in zip(no.estado, objetivo):
        if estado != objetivo and estado != 0:
            soma = soma + 1
    return soma


def h2(no, objetivo, n):
    """ Heurística Manhattan que soma das distâncias até a posição meta de cada pastilha."""
    X = n * list(range(0, n, 1))
    Y = []
    for i in range(n):
        Y = Y + n * [i]
    soma = 0
    for(estado, objetivo) in zip(no.estado, objetivo):
        if estado != 0:
            soma = soma + abs(X[estado] - X[objetivo]) + abs(Y[estado] - Y[objetivo])
    return soma


def h3(no, objetivo, n):
    """ Heurística Gasching que permite mover qualquer pastilha para o espaço vazio.
    Seja B o local atual do espaço em branco; se B estiver ocupado pelo bloco X (não o branco)
    no estado objetivo, mova X para B; caso contrário, mova qualquer bloco perdido para B.
    Some 1 ao custo calculado pela heurística para cada movimentação"""
    estado = list(no.estado)
    soma = 0
    while not testar_objetivo(tuple(estado), objetivo):
        posicao_vazia = estado.index(0)
        posicao_valor_correto = estado.index(objetivo[posicao_vazia])
        if posicao_vazia != n**2 - 1:
            estado[posicao_valor_correto], estado[posicao_vazia] = estado[posicao_vazia], estado[posicao_valor_correto]
        else:
            posicao_aleatoria = randint(0, n**2 - 1)
            estado[posicao_aleatoria], estado[posicao_vazia] = estado[posicao_vazia], estado[posicao_aleatoria]
        soma = soma + 1
    return soma


def realizar_movimento(estado, movimento):
    """Troca a posição vazia com a posição de movimento definida."""
    estado = list(estado)
    posicao_vazia = estado.index(0)
    estado[movimento], estado[posicao_vazia] = estado[posicao_vazia], estado[movimento]
    return tuple(estado)


def definir_movimentos_possiveis(n):
    """Vetor com indices dos quadrados a partir dos quais é possível mover uma pastilha."""
    movimentos_possiveis = []
    for i in range(n**2):
        # Quatro cantos do tabuleiro
        if i == 0:
            movimentos_possiveis.append([i+1, i+n])
        elif i == n-1:
            movimentos_possiveis.append([i-1, i+n])
        elif i == n**2-n:
            movimentos_possiveis.append([i+1, i-n])
        elif i == n**2-1:
            movimentos_possiveis.append([i-1, i-n])
        # Coluna superior do tabuleiro
        elif i > 0 and i < n:
            movimentos_possiveis.append([i-1, i+1, i+n])
        # Coluna inferior do tabuleiro
        elif i > n**2-n and i < n**2-1:
            movimentos_possiveis.append([i-1, i+1, i-n])
        # Coluna lateral esquerda do tabuleiro
        elif i > 0 and i < n**2-n and i % n == 0:
            movimentos_possiveis.append([i+1, i+n, i-n])
        # Coluna lateral direita do tabuleiro
        elif i > n-1 and i < n**2-1 and (i+1) % n == 0:
            movimentos_possiveis.append([i-1, i+n, i-n])
        # Meios do tabuleiro
        else:
            movimentos_possiveis.append([i-1, i+1, i+n, i-n])

    return movimentos_possiveis


def expandir(no, movimentos_possiveis):
    "Expande um no, gerando os novos estados possiveis."
    estado_atual = no.estado
    posicao_vazia = estado_atual.index(0)
    for movimento in movimentos_possiveis[posicao_vazia]:
        proximo_estado = realizar_movimento(estado_atual, movimento)
        custo = no.custo_caminho + 1  # custo 1 de cada movimentação
        yield No(proximo_estado, no, custo)


def testar_objetivo(estado, objetivo):
    return estado == objetivo


class No:
    "Classe No com o estado, pai do estado e custo do caminho."
    def __init__(self, estado, pai=None, custo_caminho=0):
        self.estado = estado
        self.pai = pai
        self.custo_caminho = custo_caminho

    def __lt__(self, no):
        return self.custo_caminho < no.custo_caminho


class FilaPorPrioridade:
    """Fica na qual o elemento com menor f() é escolhido primeiro.
    Ref.: https://docs.python.org/3.6/library/heapq.html """

    def __init__(self, estados=[], funcaof=lambda x: x):
        self.funcaof = funcaof
        self.estados = []
        for estado in estados:
            self.adicionar(estado)  # heap dos pares (valor de f(), estado)

    def adicionar(self, estado):
        """Adiciona um estado com seu funcaof na fila."""
        par = [self.funcaof(estado), estado]
        heapq.heappush(self.estados, par)

    def retirar(self):
        """Retira e retorna estado com o menor valor de f()."""
        return heapq.heappop(self.estados)[1]


def main():
    """  Programa Principal. """
    n, heuristica, condicaoinicial = ler_entrada()
    objetivo = tuple(list(range(1, n**2, 1)) + [0])
    movimentos_possiveis = definir_movimentos_possiveis(n)

    if tabuleiro_solucionavel(n, condicaoinicial):
        """Seleciona heuristica a utilizar e monta função f(n) = g(n) + h(n)."""
        if heuristica == "h1": f = lambda no: no.custo_caminho + h1(no, objetivo)
        if heuristica == "h2": f = lambda no: no.custo_caminho + h2(no, objetivo, n)
        if heuristica == "h3": f = lambda no: no.custo_caminho + h3(no, objetivo, n)
        "Busca nos nós com valor f(nó) mínimo usando estrutura de heap."
        fronteira = FilaPorPrioridade([No(condicaoinicial)], funcaof=f)
        alcancados = {}
        while fronteira:
            no = fronteira.retirar()
            if testar_objetivo(tuple(no.estado), objetivo):
                print("----- INIT -----")
                for estado in caminhoEstado(no):
                    print(*estado)
                print("----- GOAL -----")
                return no
            for filho in expandir(no, movimentos_possiveis):
                novo_estado = filho.estado
                novo_custo_caminho = filho.custo_caminho
                if novo_estado not in alcancados or novo_custo_caminho < alcancados[novo_estado].custo_caminho:
                    # adiciona fronteira se: novo estado nunca alcancado OU alcançado por um caminho de menor custo.
                    alcancados[novo_estado] = filho
                    fronteira.adicionar(filho)

if __name__ == '__main__':
    main()