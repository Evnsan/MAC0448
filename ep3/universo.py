#!/usr/bin/python

from parser import Parser


## Comandos aceitos no arquivo de configuracao

def cmdFinish(args):
	print "este e o comando finish: "  + str(args)

def cmdSet(args):
	print "este e o comando set: " + str(args)


def cmdSimulate(args):
	print "este e o comando cmdSimulate: " + str(args)

comandos = {'set': cmdSet, 'simulate': cmdSimulate, 'finish': cmdFinish}
comandosSet = {}
comandosSimulate = {}


def executaComandos(cmds):
	for cmd,args in cmds:
	
		comandos[cmd](args)

def main():
	p = Parser()
	cmds = p.lerComandos()
	executaComandos(cmds)







if __name__ == '__main__':
    main()



