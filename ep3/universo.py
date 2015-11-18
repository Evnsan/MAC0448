#!/usr/bin/python

import sys


################## Biblioteca de classes - elementos da rede ##################
from parser import Parser
from router import Router
from host import Host
from enlace import Enlace
###############################################################################

################## Listas Globais - Variaveis Globais #########################
elementos = [] 
routers = {}
hosts = {}
aplicacoes = {}
tempoDeSimulacao = 0
###############################################################################

def rotinaCmdAplicacao(args):
    h = hosts[args[1]]
    nomeAplicacao = args[2]
    aplicacoes[nomeAplicacao] = h
    h.nomeAplicacao = nomeAplicacao



################## Rotinas de Configuracao e Execucao do universo #############

## Comandos secundarios
def cmdRouter(args):
	print "cmdRouter" + str(args)
	r = Router(args[1], int(args[2]))
	routers[args[1]] = r
	elementos.append(r)

def cmdHost(args):
	print "cmdHost" + str(args)
	h = Host(args[1])
	hosts[args[1]] = h
	elementos.append(h)

def cmdDuplexLink(args):
    print "cmdDuplexLink" + str(args)
    e = Enlace(None, None, args[3], args[4])
    elementos.append(e)
    #colocar os enlaces nos hosts/routers
    #TerminalA
    node, porta = parsePonto(args[1])
    try:
        hosts[node].setEnlace(e)
        e.setTerminalA(hosts[node])
    except KeyError:
        routers[node].setEnlace(int(porta), e)
        e.setTerminalA(routers[node])
    
    #TerminalB
    node, porta = parsePonto(args[1])
    try:
        hosts[node].setSniffer(args[3])
        e.setTerminalB(hosts[node])
    except KeyError:
        routers[node].setSniffer(int(porta), args[3])
        e.setTerminalB(routers[node])

def cmdIp(args):
	print "cmdIp" + str(args)

def cmdPerformance(args):
	print "cmdPerformance" + str(args)
	del args[0]
	r = routers[args[0]]
	del args[0]
	r.setTempoPacote(args[0])
	del args[0]
	r.setPortas(args)

def cmdIrcc(args):
    rotinaCmdAplicacao(args)
    print "cmdIrcc" + str(args)

def cmdIrcs(args):
    rotinaCmdAplicacao(args)
    print "cmdIrcs" + str(args)

def cmdDnss(args):
    rotinaCmdAplicacao(args)
    print "cmdDnss" + str(args)

def parsePonto(arg):
    host = None 
    porta = None 
    try:
        host, porta =  arg.split(".")
    except ValueError:
        host = arg
    print str(host) + " " + str(porta)
    return [host, porta]
    
def cmdSniffer(args):
    print "cmdSniffer" + str(args)
    node, porta = parsePonto(args[1])
    try:
        hosts[node].setSniffer(args[3])
    except KeyError:
        routers[node].setSniffer(int(porta), args[3])

        
def cmdRoute(args):
    nomeRouter = args[1]
    del args[0]
    del args[0]
    router = routers[nomeRouter]
    for i in xrange(0, len(args)/2,2):
        router.setRota(args[i],args[i+1])
    print "cmdRoute" + str(args)

## Comandos aceitos no arquivo de configuracao

def cmdFinish(args):
    print "este e o comando finish: " + str(args)
    global tempoDeSimulacao
    tempoDeSimulacao = 1000 * float(args[0])
    print tempoDeSimulacao

def cmdSet(args):
	comandosSet[args[0]](args)

def cmdSimulate(args):
    h = aplicacoes[args[1]]
    tempo = args[0]
    comandos = args[2]
    for i in range(3):
        del args[0]
    h.adicionaComando(float(tempo)*1000, comandos, args)        
    print "este e o comando cmdSimulate: " + str(args)




comandos = {'set': cmdSet,
            'simulate': cmdSimulate,
            'finish': cmdFinish}

comandosSet = {'host': cmdHost,
               'router': cmdRouter,
               'duplex-link': cmdDuplexLink, 
			   'ip': cmdIp,
               'performance': cmdPerformance,
               'ircc': cmdIrcc,
			   'ircs': cmdIrcs,
               'dnss': cmdDnss,
               'sniffer': cmdSniffer,
			   'route': cmdRoute}

comandosSimulate = {}
###############################################################################

################## Rotinas do ciclo de execucao do universo ###################
def executaSimulacoes(tmp):
    relogio = 0
    while(relogio < tmp):
        for elm in elementos:
            elm.passo(relogio)
        relogio += 1
    print "Final da execucao"

def executaComandos(cmds):
	for cmd,args in cmds:
		comandos[cmd](args)

def main():
    p = Parser()
    if(len(sys.argv) > 1):
        print "Arquivo de configuracao: " + str(sys.argv[1])
        p.setArqConfiguracao(sys.argv[1])
    cmds = p.lerComandos()


    for c in cmds:
        print c
    #print "AQUI===>" + str(cmds)
    executaComandos(cmds)
    #print tempoDeSimulacao
    executaSimulacoes(tempoDeSimulacao)
    ###############################################################################

if __name__ == '__main__':
    main()



