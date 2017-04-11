#!/usr/bin/python
#-*- coding: utf-8-*-

import Escalonadores as esc
import os

#name = input("Nome do arquivo: ")
#fl = open(name, "r")
fl = open("entrada.txt", "r")
procs = []

#Lendo arquivo e formando as tuplas
#[Entrada, Tempo de execução, Tempo de Retorno, Tempo de Resposta, Tempo de Espera]
for line in fl.readlines():
    if (line != "\n") and (line != "\t") and (line != " "):
        ln = line.replace("\n","").split(" ")
        procs.append([int(ln[0]),int(ln[1]),0,0,0])
fl.close()

procs.sort(key=lambda tup: tup[0]) #Ordena as tuplas por ordem crescente do tempo de entrada na fila

esc.fcfs(procs)
esc.sjf(procs)
esc.rr(procs)
