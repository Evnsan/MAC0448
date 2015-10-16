
Alunos--
nome: Evandro Augusto Nunes Sanches nUsp:5388861
nome: Pedro Ferreira Alexandre nUsp:7577448



/***********************************************/
LEIA-ME oldserver.py

Para a execução do servidor é obrigatório que sejam criados dois diretórios juntos
com as demais pastas do projeot:
1) ./SESSION
2) ./LOG
____________________________________________________________________________________
Para inicia o servidor execute o script em python contido no arquivo oldserver.py 
da seguinte forma:
	./oldserver.py
No início do arquivo é possível editar as portas dos sockets UDP(UDP_PORT)  e 
TCP(TCP_PORT) utilizados, o tempo entre cada checagem por clientes 
inativos(CHECK_PERIOD) e o limite de tempo permitido para clientes antes de 
serem retirados da lista de clientes(CHECK_TIMEOUT) e também o tamanho máximo da
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
GAMEFILENAME

onde classe é a marca no jogo (x ou o) e o filename é o nome do arquivo comum da
partida compartilhado pelos dois jogadores
____________________________________________________________________________________
[usernameAusernameB] → um para cada dupla de jogadores que já jogaram alguma partida
com informacoes da ultima partina no seguinte formato:

VEZ
POS0 POS1 POS2  POS3 POS4 POS5 POS6 POS7 POS8

onde POSi é um valor entre {0,1,2} que simboliza 0: posicao do tabuleiro livre, 1:
posicao marcada pelo jogador1, 2: posicao marcada pelo jogador2.
____________________________________________________________________________________
users → arquivo que contem os usuarios já cadastrados e suas senhas no seguinte
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
TABULEIRO:  JOGO DA VELHA
As posições a seguir retratam como devem ser escolhidas as coordenadas
das jogadas no tabuleiro.   

    0_|1|_2
    3_|4|_5
    6_|7|_8
        

INFORMAÇÕES GERAIS:

O servidor consiste em um thread principal, "main", responsável por eliminar clientes
inativos por tempo maior que um dado limite. Para tanto, uma estrutura de apoio é
utilizada, Heartbeats - um dicionario especializado que usa como chave (ip, porta) e
devolve cliente. Basicamentea, thread executa a rotina, pede ao Heartbeat pelos clientes
inativos e remove eles da estrutura fechando seus sockets se necessario em um looping
infinito.
Além da main thread, ainda existem mais duas thread principais, UDP - responsável
pelas mensagens das conexões UDP e TCP - responsável por aceitar conexões TCP. Fora
as threads principais, toda conexão TCP cria uma thread TCP-Client para cada cliente
TCP conectado.
A representação dos clientes utilizando o servidor é feita pela estrutura Cliente e
são acessadas através do dicionario Heartbeats.
Cada instância deste objeto contém informações como: socket de conexão, ip, porta,
user name e outras coisas.
Por ultimo é importante ressaltar que cada cliente se comporta como uma máquina de
estado que só aceita certos comandos em cada estado. 


/***********************************************/
LEIA-ME oldcliente.py


Para iniciar o aplicativo execute o script em python contido no arquivo oldcliente.py
da seguinte forma:
	./oldserver.py SERVER [PORTAALTERNATIVAUDP] [PORTAALTERNATIVASERVER]
No início do arquivo é possível editar as portas de destino dos sockets UDP(SERVER_UDP_PORT)
e TCP(SERVER_TCP_PORTA), as portas UDP(UDP_PORTA) e TCP(TCP_PORTA) do socket do cliente e a 
porta utilizada pelo chat UDP(CHAT_PORTA).
MODO DE USO:
-Interação via prompt de comando:
--Toda linha escrita no prompt é enviada para o adversario do jogo
--Todo comando precedido de ':' é enviado para o servidor
--Caracter '+' informa o estado atual na maquina de estados

-Comandos Principais:
--USER nome -> inicia o login de 'nome'
--PASS chave -> informa senha 'chave'
--NEWUSER nome -> cadastra novo usuario 'nome'
--NEWPASS chave -> cadastra nova senha 'chave' (somente para usuarios que estao se registrando) 
--LIST -> lista usuarios logados e seus estados
--HALL -> lista Hall da Fama
--PLAYINV nome porta --> Convida usuario 'nome' para jogar e conectar no chat na porta 'porta'
--PLAYACC nome porta --> Aceita convite de usuario 'nome' com chat na porta 'porta'
--PLAYDNY nome -> declina convite do usuario 'nome'
--ABORT -> retorna para o estado anterior na maquina de estados do servidor e do cliente
--BOARD -> pede pelo tabuleiro de jogo atual
--GETESTD -> pergunta o estado no servidor para sincronizar o cliente

INFORMAÇÕES GERAIS:
O cliente não guardará as informações de forma persistente de nenhuma forma. Mas sim manterá
informações de seu estado em memória. Este estado é a base para sua execução, assim quando
uma ação e executada pelo usuario, a mensagem é montada e enviada para o servidor que emitirá
uma resposta. Esta última causa a mudança de estado do cliente que passa a agir de forma
diferente de acordo com o estado atingido.
Nesta lógica o cliente é basicamente uma máquina de estados ao estilo tradicional, passando
de estado para estado mediante a ação das mensagens recebidas.
Para efeito de sincronia, o protocolo desenvolvido suporta uma mensagem em especial, GETESTD,
que pede ao servidor que informe o estado no qual o cliente se encontra na maquina de estados
do servido. Após uma tradução o cliente atinge o estado necessário.
Quando um jogo é iniciado, o cliente tentará iniciar uma conexão com o aplicativo cliente de
seu adversário da seguinte forma:
[Anfitrião] abre a porta e informa ao cliente
[Convidado] recebe msg pelo servidor, inicia novo socket e envia CHATACK
[Anfitrião] recebe CHATACK pelo novo socket e responde CHATACK
Neste ponto ambos estão conversando.

Estado Atual:
Para a atual versão do cliente, no caso do UDP a ultima tarefa deve ser feita manualmente digi-
tando CHATACK no prompt e apertando enter.
O tcp não foi implementado por falta de tempo, e pode gerar problemas ao iniciar partida pelo
cliente.
O servidor esta completo nesta parte, e o jogo pode ser executado perfeitamente utilizando o telnet
ou netcat, para TCP e UDP.


