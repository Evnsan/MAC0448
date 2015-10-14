def geraTabuleiroFinal(tab, winnerLine):
    tab[winnerLine[0]] = '8'
    tab[winnerLine[1]] = '8'
    tab[winnerLine[2]] = '8'
    return tab


def victoryLine(seq, tab):
    if (tab[seq[0]] == tab[seq[1]] and tab[seq[1]] == tab[seq[2]]):
        winner = tab[seq[0]]
        if winner != '0':  # pra nao considerar uma tripla de zeros como linha vitoriosa
            return winner    
    return 0
#retorna 0 se nao houve vencedor, ou o inteiro que representa a classe do vencedor
def whoWon(tabuleiro):
    g1 = [0,1,2]
    g2 = [3,4,5]
    g3 = [6,7,8]
    g4 = [0,3,6]
    g5 = [1,4,7]
    g6 = [6,7,8]
    g7 = [0,4,8]
    g8 = [2,4,6]


    gameGabarito = [g1,g2,g3,g4,g5,g6,g7,g8]
    for g in gameGabarito:
        winner = victoryLine(g, tabuleiro)
        if(winner > 0):
            linhaVencedora = g
            return winner, linhaVencedora
    return ('0',[]) 


tabuleiro = ['0','0','0','0','0','0','0','0','0']

winner,winnerLine = whoWon(tabuleiro)
print int(winner)
if int(winner) > 0:
    print geraTabuleiroFinal(tabuleiro, winnerLine)

tabuleiro = ['1','1','1','0','0','0','0','0','0']

winner,winnerLine = whoWon(tabuleiro)
print winner
if int(winner) > 0:
    print geraTabuleiroFinal(tabuleiro, winnerLine)
tabuleiro = ['1','0','1','1','0','0','0','0','1']

winner,winnerLine = whoWon(tabuleiro)
print winner
if int(winner) > 0:
    print geraTabuleiroFinal(tabuleiro, winnerLine)

tabuleiro = ['0','0','0','1','1','1','0','0','0']

winner,winnerLine = whoWon(tabuleiro)
print winner
if int(winner) > 0:
    print geraTabuleiroFinal(tabuleiro, winnerLine)


tabuleiro = ['0','0','2','1','2','1','2','0','0']

winner,winnerLine = whoWon(tabuleiro)
print winner
if int(winner) > 0:
    print geraTabuleiroFinal(tabuleiro, winnerLine)

tabuleiro = ['1','2','1','1','2','2','2','1','2']

winner,winnerLine = whoWon(tabuleiro)
print winner
if int(winner) > 0:
    print geraTabuleiroFinal(tabuleiro, winnerLine)
