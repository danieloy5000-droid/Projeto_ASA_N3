from pulp import *

def calcula(equipas, tabela, quadro, equipa_win):
    prob = LpProblem("solucao", LpMinimize)

    variaveis_jogo = {}
    total_vitorias_precisas = []

    for (i, j), nj in quadro.items():
        if nj > 0:
            w = LpVariable(f"w_{i}_{j}_{equipa_win}", 0, nj, cat='Integer')
            d = LpVariable(f"d_{i}_{j}_{equipa_win}", 0, nj, cat='Integer')
            l = LpVariable(f"l_{i}_{j}_{equipa_win}", 0, nj, cat='Integer')

            variaveis_jogo[(i,j)] = (w, d, l)

            prob += w + d + l == nj

            if (i == equipa_win):
                total_vitorias_precisas.append(w)
            if (j == equipa_win):
                total_vitorias_precisas.append(l)

    if (len(total_vitorias_precisas) == 0):
        for e in range(1, equipas+1):
            if(equipa_win == e):
                continue
            elif(tabela[equipa_win] < tabela[e]):
                return -1
    
    if total_vitorias_precisas:
        prob += lpSum(total_vitorias_precisas)
    else:
        return 0

    pontuacao_final = {}
    for e in range(1, equipas+1):
        expressao = tabela[e]

        for (i, j), (w, d, l) in variaveis_jogo.items():
            if e == i:
                expressao += 3*w + d
            if e == j:
                expressao += 3*l + d 

        pontuacao_final[e] = expressao    

    for e in range(1, equipas+1):
        if e != equipa_win:
            prob += (pontuacao_final[equipa_win] >= pontuacao_final[e])

    status = prob.solve(GLPK(msg=0))

    if status != 1:
        return -1
    
    res = value(prob.objective)

    if res is None:
        return 0
    
    return int(res)


    

equipasjogos = input()

x = equipasjogos.split()

equipas = int(x[0])
jogosJogados = int(x[1])

pontosAtuais = {i:0 for i in range(1, equipas+1)}

jogos = []

for la in range(jogosJogados):
    jogojogado = input()
    y = jogojogado.split()
    casa, fora, vencedor = int(y[0]), int(y[1]), int(y[2])
    u = (casa, fora, vencedor)
    jogos.append(u)

jogosFeitos = {}
for i in range(1, equipas+1):
    for j in range (i+1, equipas+1):
        jogosFeitos[(i,j)] = 2

for (casa, fora, vencedor) in jogos:
    if vencedor == 0:
        pontosAtuais[casa] += 1
        pontosAtuais[fora] += 1
    elif vencedor == casa:
        pontosAtuais[casa] += 3
    else:
        pontosAtuais[fora] += 3

    confronto = tuple(sorted((casa, fora)))
    if confronto in jogosFeitos:
        jogosFeitos[confronto] -= 1


for e in range(1, equipas+1):
    print(calcula(equipas, pontosAtuais, jogosFeitos, e))