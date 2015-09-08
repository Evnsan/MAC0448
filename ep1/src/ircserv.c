/* Evandro Ausgusto Nunes Sanches <evnsanches@ig.com.br>
 * Pedro Ferreira Alexandre <pedro.alexandre@usp.br>
 * Em 03/09/2015
 * 
 * Codigo desenvolvido como projeto da disciplina MAC0448 - Programa-
 * cao para redes de computadores. Este EP(ExerciocioPrograma) utili-
 * za como base o codigo desenvolvido pelo Professor Daniel Batista 
 * <batista@ime.usp.br>.
 *
 * Depois de compilado execute
 * ./servidor 6667
 * 
 * Com este comando o servidor ficara escutando por conexões na porta
 * 6667 TCP. A cada conexão o servidor utiliza 'fork' para gerar um
 * processo filho que cuidara de executar o protocolo  IRC para a co-
 * nexao em questao.
 *
 * Obs.: Você pode conectar no servidor remotamente também. Basta saber o
 * endereço IP remoto da máquina onde o servidor está rodando e não
 * pode haver nenhum firewall no meio do caminho bloqueando conexões na
 * porta escolhida.
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <time.h>
#include <unistd.h>

/*trecho adicionado para o irc server - EP1*/
#include <dirent.h>
#define TESTE_NIVEL_1 1
#define TESTE_NIVEL_2 0
#define MSGMAX 512
#define RCMDMAX 10
#define NICKMAX 50
#define MIDMAX 10
#define PATHMAX 256 
#define PATHCHAT "users/"
#define PATHCHAN "chan/"
#define CHAN1 "ircserv"
#define CHAN2 "ircnaoserv"

typedef struct {
    char msgv[RCMDMAX][MSGMAX];
    int n;
} Mensagens;

Mensagens* parser(const char *entrada);
int isNickValid(char *entrada);
int isChanValid(char *entrada);
int flagLogged = 0; 
int flagNickInicial = 0; 

/*variaveis globais*/
char nick[NICKMAX];

/*final deste trecho*/

#define LISTENQ 1
#define MAXDATASIZE 100
#define MAXLINE 4096


int main (int argc, char **argv) {
   /* Os sockets. Um que será o socket que vai escutar pelas conexões
    * e o outro que vai ser o socket específico de cada conexão */
	int listenfd, connfd;
   /* Informações sobre o socket (endereço e porta) ficam nesta struct */
	struct sockaddr_in servaddr;
   /* Retorno da função fork para saber quem é o processo filho e quem
    * é o processo pai */
   pid_t childpid;
   /* Armazena linhas recebidas do cliente */
	char	recvline[MAXLINE + 1];
   /* Armazena o tamanho da string lida do cliente */
   ssize_t  n;

   /*trecho adicionado para a criacao dos canais hardcoded*/
   char chanpath[PATHMAX];
   
   strcpy(chanpath, PATHCHAN);
   strcat(chanpath, CHAN1);
   fclose(fopen(chanpath, "w"));
   strcpy(chanpath, PATHCHAN);
   strcat(chanpath, CHAN2);
   fclose(fopen(chanpath, "w"));
   /*final do trecho*/
   
	if (argc != 2) {
      fprintf(stderr,"Uso: %s <Porta>\n",argv[0]);
      fprintf(stderr,"Vai rodar um servidor de echo na porta <Porta> TCP\n");
		exit(1);
	}

   /* Criação de um socket. Eh como se fosse um descritor de arquivo. Eh
    * possivel fazer operacoes como read, write e close. Neste
    * caso o socket criado eh um socket IPv4 (por causa do AF_INET),
    * que vai usar TCP (por causa do SOCK_STREAM), já que o IRC
    * funciona sobre TCP, e será usado para uma aplicação convencional sobre
    * a Internet (por causa do número 0) */
	if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
		perror("socket :(\n");
		exit(2);
	}

   /* Agora é necessário informar os endereços associados a este
    * socket. É necessário informar o endereço / interface e a porta,
    * pois mais adiante o socket ficará esperando conexões nesta porta
    * e neste(s) endereços. Para isso é necessário preencher a struct
    * servaddr. É necessário colocar lá o tipo de socket (No nosso
    * caso AF_INET porque é IPv4), em qual endereço / interface serão
    * esperadas conexões (Neste caso em qualquer uma -- INADDR_ANY) e
    * qual a porta. Neste caso será a porta que foi passada como
    * argumento no shell (atoi(argv[1]))
    */
	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family      = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port        = htons(atoi(argv[1]));
	if (bind(listenfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) == -1) {
		perror("bind :(\n");
		exit(3);
	}

   /* Como este código é o código de um servidor, o socket será um
    * socket passivo. Para isto é necessário chamar a função listen
    * que define que este é um socket de servidor que ficará esperando
    * por conexões nos endereços definidos na função bind. */
	if (listen(listenfd, LISTENQ) == -1) {
		perror("listen :(\n");
		exit(4);
	}

   printf("[Servidor no ar. Aguardando conexoes na porta %s]\n",argv[1]);
   printf("[Para finalizar, pressione CTRL+c ou rode um kill ou killall]\n");
   
   /* O servidor no final das contas é um loop infinito de espera por
    * conexões e processamento de cada uma individualmente */
	for (;;) {
      /* O socket inicial que foi criado é o socket que vai aguardar
       * pela conexão na porta especificada. Mas pode ser que existam
       * diversos clientes conectando no servidor. Por isso deve-se
       * utilizar a função accept. Esta função vai retirar uma conexão
       * da fila de conexões que foram aceitas no socket listenfd e
       * vai criar um socket específico para esta conexão. O descritor
       * deste novo socket é o retorno da função accept. */
		if ((connfd = accept(listenfd, (struct sockaddr *) NULL, NULL)) == -1 ) {
			perror("accept :(\n");
			exit(5);
		}
      
      /* Agora o servidor precisa tratar este cliente de forma
       * separada. Para isto é criado um processo filho usando a
       * função fork. O processo vai ser uma cópia deste. Depois da
       * função fork, os dois processos (pai e filho) estarão no mesmo
       * ponto do código, mas cada um terá um PID diferente. Assim é
       * possível diferenciar o que cada processo terá que fazer. O
       * filho tem que processar a requisição do cliente. O pai tem
       * que voltar no loop para continuar aceitando novas conexões */
      /* Se o retorno da função fork for zero, é porque está no
       * processo filho. */
      if ( (childpid = fork()) == 0) {
         /**** PROCESSO FILHO ****/
         printf("[Uma conexao aberta]\n");
         /* Já que está no processo filho, não precisa mais do socket
          * listenfd. Só o processo pai precisa deste socket. */
         close(listenfd);
         
         /* Agora pode ler do socket e escrever no socket. Isto tem
          * que ser feito em sincronia com o cliente. Não faz sentido
          * ler sem ter o que ler. Ou seja, neste caso está sendo
          * considerado que o cliente vai enviar algo para o servidor.
          * O servidor vai processar o que tiver sido enviado e vai
          * enviar uma resposta para o cliente (Que precisará estar
          * esperando por esta resposta) 
          */

         /* ========================================================= */
         /* ========================================================= */
         /*                         EP1 INÍCIO                        */
         /* ========================================================= */
         /* ========================================================= */
         /* TODO: É esta parte do código que terá que ser modificada
          * para que este servidor consiga interpretar comandos IRC   */
         /*iniciando conexao - definindo nick e user*/
         /*inicializacao*/
         nick[0] = '9';
         
         /*controle*/
         int i = 0;

         Mensagens* resps;
         if(1){
            const char *MOTDSTART = "375 :- SERVSERV Mensagem do dia - \n";
            const char *MOTD1 = "372 :- Bom dia1 - \n";
            const char *MOTD2 = "372 :- Bom dia2 - \n";
            const char *MOTD3 = "327 :- Bom dia3 - \n";
            const char *MOTDEND = "376 :- Final da Mensagem do dia - \n";

         
            write(connfd, MOTDSTART, strlen(MOTDSTART));
            write(connfd, MOTD1, strlen(MOTD1));
            write(connfd, MOTD2, strlen(MOTD2));
            write(connfd, MOTD3, strlen(MOTD3));
            write(connfd, MOTDEND, strlen(MOTDEND));
         }
         /*enviar user/server count*/
         /*enviar nome e versao do server*/
         
         while ((n=read(connfd, recvline, MAXLINE)) > 0) {
            recvline[n]=0;
            printf("[Cliente conectado no processo filho %d enviou:] ",
                    getpid());
            if ((fputs(recvline,stdout)) == EOF) {
               perror("fputs :( \n");
               exit(6);
            }
            resps = parser(recvline);
            if(resps != NULL){
                for( i = 0; i < resps->n; i++){ 
                    /***/
                    if(TESTE_NIVEL_2){
                        printf("entrou no loop i = %d e msg \"%s\"\n", i, resps->msgv[i]);
                    }
                    /***/
                    write(connfd, resps->msgv[i], strlen(resps->msgv[i]));
                }
                free(resps);
            }
         }
         /* ========================================================= */
         /* ========================================================= */
         /*                         EP1 FIM                           */
         /* ========================================================= */
         /* ========================================================= */

         /* Após ter feito toda a troca de informação com o cliente,
          * pode finalizar o processo filho */
         printf("[Uma conexao fechada]\n");
		 close(connfd);
         exit(0);
      }
      /**** PROCESSO PAI ****/
      /* Se for o pai, a única coisa a ser feita é fechar o socket
       * connfd (ele é o socket do cliente específico que será tratado
       * pelo processo filho) */
		close(connfd);
	}
	exit(0);
}

Mensagens* parser(const char *entrada){
    Mensagens *retorno;
    char sulfixo[MSGMAX + 1];
    char *cmd;
    FILE *fp;
    char *middle[MIDMAX];
    char *trail;
    char *tmp;
    int nmids;
    char filename1[PATHMAX], filename2[PATHMAX];
    DIR *dir;
    struct dirent *ent;
    /*controle*/
    int i;

    retorno = (Mensagens*)malloc(sizeof(*retorno));
    retorno->n = 0;
    
    /***/
    if(TESTE_NIVEL_1){
        printf("Parser: Entrada = \"%s\"\n", entrada);
    }
    /***/
    for(i = 0; i <= MSGMAX; i++)
        sulfixo[i] = '\0';

    strcpy(sulfixo, entrada);

    /*remove prefixo e recebe comando*/
    if(sulfixo[0] == ':'){
        strtok(sulfixo , " ");
        printf("aqui==> \"%s\"\n", sulfixo);
        cmd = strtok(NULL, " \r\n\0");
    }
    else
        cmd = strtok(sulfixo, " \r\n\0");

    tmp = strtok(NULL, ":\r\n\0");
    /*trail*/
    trail = strtok(NULL, "\r\n\0");
    
    /*mids*/
    printf("tmp = \"%s\"\n", tmp);
    nmids = 0;
    middle[nmids] = strtok(tmp, " \r\n\0");
    while(middle[nmids] != NULL){
        nmids++;
        middle[nmids] = strtok(NULL, " \r\n\0 ");
    }

    /***/
    if(TESTE_NIVEL_1){
        printf("Parser: cmd = \"%s\"\n", cmd);
        for(i = 0; i < nmids; i++)
            printf("Parser: middle[%d] = \"%s\"\n",i, middle[i]);
        printf("Parser: trail = \"%s\"\n", trail);
    }
    /***/

    /*parsing cmd*/
    /*NICK*/
    if(!strcmp(cmd, "NICK")){
        printf("entrou no CDM = NICK\n");
        if(isNickValid(middle[0])){
            printf("nick valido\n");
            /*verificar se ja tinha Nick*/
            /*criar arquivo de Nick se nao colidir*/
            strcpy(filename1, PATHCHAT);
            strcat(filename1,middle[0]);
            if((fp = fopen(filename1,"r")) == NULL){
                /*User ja tinha nick*/
                if(nick[0] != '9'){
                /*sim - muda o nome dos arquivos*/
                    strcpy(filename2, PATHCHAT);
                    strcat(filename2,nick);
                    rename(filename2, filename1);
                    strcat(filename1,".chan");
                    strcat(filename2,".chan");
                    rename(filename2, filename1);
                    fp = fopen(filename1, "r");
                    strcpy(nick, middle[0]);
                    retorno->n = 2;
                    strcpy(retorno->msgv[0], ":ircserv NOTICE * :***Changing your nick...\n");
                    strcpy(retorno->msgv[1], ":ircserv NOTICE * :***DONE...\n");
                }
                else{
                /*nao - cria arquivos*/
                    printf("path: %s\n", filename1);
                    fp = fopen(filename1,"w");
                    fclose(fp);
                    strcat(filename1,".chan");
                    fp = fopen(filename1,"w");
                    strcpy(nick, middle[0]);
                    flagNickInicial = 1;
                    retorno->n = 1;
                    strcpy(retorno->msgv[0], ":ircserv NOTICE * :*** Looking up your hostname...\n");
                /*criar resposta*/
                }
            }
            else{
                printf("nick ja existe: %s \n", middle[0]);
                retorno->n = 1;
                strcpy(retorno->msgv[0], ":ircserv 433");
                strcat(retorno->msgv[0], middle[0]);
                strcat(retorno->msgv[0], " :Nickname is already in use\n");
                /*criar resposta*/
            }
            fclose(fp);
        }
        else{
            /*retornar codigo de badnick*/
            printf("Nick invalido\n");
        }
    }
    /*USER*/
    else if(!strcmp(cmd, "USER") && flagNickInicial){
        flagNickInicial = 0;
        flagLogged = 1;
        strcpy(filename1, PATHCHAT);
        strcat(filename1, nick);
        fp = fopen(filename1, "w");
        fprintf(fp, "%s", cmd);
        for(i = 0; i < nmids; i++){
            fprintf(fp, " %s", middle[i]);
        }
        if(trail != NULL)
           fprintf(fp, " %s", trail);
        fprintf(fp, "\n");
        fclose(fp);
        retorno->n = 1;
        strcpy(retorno->msgv[0], ":ircserv NOTICE * :*** Welcome...\n");
    }
    /*LIST*/
    else if(!strcmp(cmd,"LIST") && flagLogged){
        if(nmids > 0){
            if(middle[0][0] == '#'){
            }
        }
        else { 
            if ((dir = opendir (PATHCHAN)) != NULL) {
                  /* print all the files and directories within directory */
                  while ((ent = readdir (dir)) != NULL) {
                      if(isalpha(ent->d_name[0]))
                          printf ("%s\n", ent->d_name);
                  }
                  closedir (dir);
            } else {
                  /* could not open directory */
            }
        }
    }
    /*JOIN*/
    else if(!strcmp(cmd,"JOIN") && flagLogged){
        if(isChanValid(middle[0])){
            printf("chan valido\n");
            /*verificar se ja tinha chan*/
            strcpy(filename1, PATHCHAN);
            strcat(filename1, &middle[0][1]);
            printf("chan name : \"%s\"\n", filename1);
            if((fp = fopen(filename1,"r")) == NULL){
                /*cria arquivos*/
                fp = fopen(filename1, "w");
                fprintf(fp, "%s\n", nick);
                fclose(fp);
                retorno->n = 1;
                strcpy(retorno->msgv[0], ":ircserv NOTICE * :*** Canal Criado...\n");
                /*criar resposta*/
            }
            else{
                /*adicionar nick no filename1*/
                fprintf(fp, "%s\n", nick);
                fclose(fp);
                retorno->n = 1;
                strcpy(retorno->msgv[0], ":ircserv NOTICE * :*** Adicionado ao Canal...\n");
                /*criar resposta*/
            }
        }
        else{
            /*retornar codigo de badChan*/
            printf("Chan invalido\n");
        }
    }
    
    /*QUIT*/
    else if(!strcmp(cmd,"QUIT") && flagLogged){
    }

    return retorno;
}

int isNickValid(char *entrada){
    int i;
    char c;
    if(!isalpha(entrada[0]))
            return 0;
    for(i = 1; i < strlen(entrada); i++){
        c = entrada[i];
        if(!isalnum(c) && c != '-' && c != '[' && c != ']' 
                && c != 92 && c != '`' && c != '^' 
                && c != '{' && c != '}'){
            return 0;
        }
    }
    return 1;
}
int isChanValid(char *entrada){
    int i;
    char c;
    if(entrada[0] != '#' && entrada[0] != '&')
        return 0;
    for(i = 1; i < strlen(entrada); i++){
        c = entrada[i];
        if(c == ' ' || c == ',' || c == '\n' 
                || c == '\r' || c == 7){
            printf("==>%c\n", c);
            return 0;
            }
    }
    return 1;
}
