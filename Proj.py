from pulp import *

def calcula(w,d,l,Nj,Pn):
    prob = LpProblem("solucao", LpMinimize)

    x = LpVariable("x", w)
    y = LpVariable("y", d)
    z = LpVariable("z", l)

    prob += x

    prob += x + y + z == Nj
    prob += 3*x + y >= Pn

    status = prob.solve(GLPK(msg=0))

    if (status != 1):
        return -1
    
    res = int(value(prob.objective)) - w 
    
    return res 


equipasjogos = input()

x = equipasjogos.split()

equipas = int(x[0])
jogosJogados = int(x[1])

jogostotais = (equipas-1)*2

pontos = 3 + (jogostotais-1)

jogos = []

for la in range(jogosJogados):
    jogojogado = input()
    y = [jogojogado.split()]
    jogos += y


for e in range(equipas):
    e += 1
    w = 0
    d = 0
    l = 0
    size = len(jogos)
    for i in range(size):
        if (int(jogos[i][0]) == e or int(jogos[i][1]) == e):
            if (int(jogos[i][2]) == e):
                w += 1
            elif (int(jogos[i][2]) == 0):
                d += 1
            else:
                l += 1
    print(calcula(w,d,l,jogostotais,pontos))



