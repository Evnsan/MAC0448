from enlace import Enlace
from host import Host
from datagrama import Datagrama
from segmento import Segmento
from mensagem import Mensagem
from router import Router

# Universo
tempo = 100
elementos = []

# __      __      __
#|  |    |  |    |  |
#|  |----|  |----|  |
#|--|    |--|    |--|
# h0      r0      h1

rotas ={'10.0.0.0': '0', '10.1.1.0': '1'}



#Rede
#-hosts
h0 = Host("h0")
h0.ip = '10.0.0.1'
h0
h1 = Host("h1")
h1.ip = '10.1.1.1'
h1
#-roteadores
r0 = Router("r0", 2)
ipRouter = ['0', '10.0.0.2','1','10.1.1.2', '2' , '192.168.3.3']
r0.setIp(ipRouter)
r0
#-enlaces
e0 = Enlace(h0, r0.getPorta(0), "10M", "5s")
e1 = Enlace(h1, r0.getPorta(1), "10M", "5s")
#e1 = Enlace(h0, h1, "10M", "5s")
#-atribuindo enlaces
h0.setEnlace(e0)
h1.setEnlace(e1)
r0.setEnlace(0, e0)
r0.setEnlace(1, e1)
r0.rotas = rotas
r0.setTempoPacote('2')
elementos.append(h0)
elementos.append(h1)
elementos.append(r0)
elementos.append(e0)
elementos.append(e1)


# Datagrama
m = Mensagem()
m.setMsg("IRC MSG")
s = Segmento('UDP', 8888, 6667)
s.setMensagem(m)
d = Datagrama(6, h0.ip, h1.ip,s)
d.setTamanho(15)
d

# Envio
e0.enviar(h0, d)
e0.printBuff()

# Fila de comandos
h0.adicionaComando(2, "cmp", "sdajk")
h0.adicionaComando(8, "cmp", "lsjk")
h0.adicionaComando(1, "cmp", "ldajk")
h0.adicionaComando(10, "cmp", "sdaj")
h0.setSniffer("snifferH0")

t = 0
while t < tempo:
    for elm in elementos:
        elm.passo(t)
 >   t += 1
