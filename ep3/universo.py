#!/usr/bin/python

from parser import Parser




## Comandos secundarios

def cmdRouter(args):
	print "cmdRouter" + str(args)


def cmdHost(args):
	print "cmdHost" + str(args)

def cmdDuplexLink(args):
	print "cmdDuplexLink" + str(args)

def cmdIp(args):
	print "cmdIp" + str(args)

def cmdPerformance(args):
	print "cmdPerformance" + str(args)

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

comandos = {'set': cmdSet, 'simulate': cmdSimulate, 'finish': cmdFinish}
comandosSet = {'host': cmdHost, 'router': cmdRouter,           'duplex-link': cmdDuplexLink, 
			   'ip': cmdIp,     'performance': cmdPerformance, 'ircc': cmdIrcc,
			   'ircs': cmdIrcs, 'dnss': cmdDnss,               'sniffer': cmdSniffer,
			   'route': cmdRoute}

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



