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
    n = len(x)
    carries = [Signal(bool(0)) for _ in range(n + 1)]

    fa_instances = [
        fullAdder(x[i], y[i], carries[i], soma[i], carries[i + 1])
        for i in range(n)
    ]

    @always_comb
    def comb():
        carry.next = carries[n]

    return fa_instances + [comb]


@block
def addervb(x, y, soma, carry):
    n = len(x)
    total = Signal(modbv(0)[n + 1:])

    @always_comb
    def comb():
        total.next = x + y
        soma.next = total[n:]
        carry.next = total[n]

    return comb
