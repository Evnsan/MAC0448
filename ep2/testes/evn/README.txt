Leia-me oldserver.py
Para inicia o servidor execute o scripit em python contido no arquivo oldserver.py 
da seguinte forma:
	./oldserver.py
No início do arquivo é possível editar as pordas dos sockets UDP(UDP_PORT)  e 
TCP(TCP_PORT) utilizados, o tempo entre cada checagem por clientes 
inativos(CHECK_PERIOD) e o limite de tempo permitido para clientes antes de 
serem retirados da lista de clientes(CHECK_TIMEOUT) e támbem o tamanho maximo da
fila de espera por conexoes TCP.
O servidor guardará as informações dos clientes em arquivos que ele manipulará 
durante sua execução. São eles:
____________________________________________________________________________________
[username.gm] → um para cada usuario com informacoes de potuação e status de um jogo
em andamento no seguinte formato:

PONTUACAO
ADVERSARIO
SERVER|CLIENTE DO CHAT
PORTA
CLASSE 0 | 1
FILENAME

onde classe é a marca no jogo (x ou o) e o filename é o nome do arquivo comum da
partida compartilhado pelos dois jogadores
____________________________________________________________________________________
[usernameAusernameB] → um para cada dupla de jogadores que já jogaram alguma partida
com informacoes da ultima partina no seguinte formato:

VEZ
POS0 POS1 POS2  POS3 POS4 POS5 POS6 POS7 POS8

onde POSi é um valor entre {0,1,2} que simboliza 0: posicao do tabuleiro livre, 1
posicao marcada pelo jogador1 2 posicao marcada pelo jogador2.
____________________________________________________________________________________
users → arquivo que contendo os usuario já cadastrados e suas senha no seguinte
formato:
user1;senha1
user2;senha2
:	:
.	.
____________________________________________________________________________________
log/[username] → um para cada usuario já cadastrado no servidor. Contendo
informações sobre cada comando executado em cada atividade do mesmo. Segue o 
seguinte formato:
[DIADASEMANA MES DIADOMES HORA:MIN:SEG ANO] COMANDO|COMENTARIO
[DIADASEMANA MES DIADOMES HORA:MIN:SEG ANO] COMANDO|COMENTARIO
:	:	:	:	:	:	:	:
.	.	.	.	.	.	.	.
____________________________________________________________________________________
session/[username] → um para cada cliente que estiver logado.
____________________________________________________________________________________

INFORMAÇÕES GERAIS:

O servidor consiste em um thread principal, "main", responsável por eliminar clientes
inativos por tempo maior que um dado limite. Para tanto, uma estrutura de apoio é
utilizada, Heartbeats - um dicionario especializado que usa como chave (ip, porta) e
devolve cliente. Basicamentea thread executa a rotina pede ao Heartbeat pelos clientes
inativo e remove eles da estrutura fechando seus sockets se necessario em um looping
infinito.
Além da main thread, ainda existem mais duas thread principais, UDP - responsável
pelas mensagens das conexões UDP e TCP - responsável
