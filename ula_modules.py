#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blocos combinacionais de somadores em MyHDL.

Este modulo declara implementacoes de:
- meio somador (half adder),
- somador completo (full adder),
- somador de 2 bits,
- somador generico por encadeamento,
- somador vetorial comportamental.
"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    @always_comb
    def comb():
        soma.next = a ^ b
        carry.next = a and b

    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    s = [Signal(bool(0)) for i in range(3)]
    haList = [None for i in range(2)]

    haList[0] = halfAdder(a, b, s[0], s[1]) 
    haList[1] = halfAdder(c, s[0], soma, s[2])

    @always_comb
    def comb():
        carry.next = s[1] | s[2]

    return instances()


@block
def adder2bits(x, y, soma, carry):
    c0 = Signal(bool(0)) 
    c1 = Signal(bool(0)) 

    result_half = halfAdder(x[0], y[0], soma[0], c0)
    result_full = fullAdder(x[1], y[1], c0, soma[1], c1)
    
    @always_comb
    def comb():
        carry.next = c1

    return instances()


@block
def adder(x, y, soma, carry):
    """Somador generico para vetores de mesmo tamanho.

    Implementacao esperada por ripple-carry (encadeamento de carries)
    usando celulas de full adder.

    Args:
        x: Vetor de entrada.
        y: Vetor de entrada.
        soma: Vetor de saida com mesma largura de x/y.
        carry: Carry de saida mais significativo.
    """
    return instances()


@block
def addervb(x, y, soma, carry):
    """Somador vetorial em estilo comportamental.

    Versao combinacional que pode usar operacoes aritmeticas diretas
    sobre os vetores para gerar soma e carry.

    Args:
        x: Vetor de entrada.
        y: Vetor de entrada.
        soma: Vetor de saida.
        carry: Carry de saida.
    """
    @always_comb
    def comb():
        pass

    return instances()
