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
###############################################################################


################## Rotinas de Configuracao e Execucao do universo #############

## Comandos secundarios
def cmdRouter(args):
	print "cmdRouter" + str(args)
	r = Router(args[1], args[2])
	routers[args[1]] = r
	elementos.append(r)

def cmdHost(args):
	print "cmdHost" + str(args)
	h = Host(args[1])
	hosts[args[1]] = h
	elementos.append(h)

def cmdDuplexLink(args):
	print "cmdDuplexLink" + str(args)

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
	print "cmdIrcc" + str(args)

def cmdIrcs(args):
	print "cmdIrcs" + str(args)

def cmdDnss(args):
	print "cmdDnss" + str(args)

def cmdSniffer(args):
	print "cmdSniffer" + str(args)
def cmdRoute(args):
	print "cmdRoute" + str(args)

## Comandos aceitos no arquivo de configuracao

def cmdFinish(args):
	print "este e o comando finish: " + str(args)

def cmdSet(args):
	comandosSet[args[0]](args)

def cmdSimulate(args):
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
    contador = 0
    while(contador < tmp):
        for elm in elementos:
            elm.passo()
        contador += 1
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
    executaComandos(cmds)
    executaSimulacoes(3)

###############################################################################

if __name__ == '__main__':
    main()



