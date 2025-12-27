from pulp import *
equipasjogos = input()

x = equipasjogos.split()

equipas = int(x[0])
jogosJogados = int(x[1])

Pontosnecessários = ((equipas-1)*3)/2
print(Pontosnecessários)