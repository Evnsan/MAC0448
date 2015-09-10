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
#include <sys/stat.h>
#include <ctype.h>

#define TESTE_NIVEL_1 1
#define TESTE_NIVEL_2 0
#define MSGMAX 512
#define RCMDMAX 100
#define NICKMAX 50
#define CHANMAX 50
#define FILENAMEMAX 50
#define TAMLINEMAX 51
#define MIDMAX 10
#define PATHMAX 256 
#define PATHCHAT "users/"
#define PATHCHAN "chan/"
#define PATHSERVER "server/"
#define USERSFILE "users"
#define CHAN1 "ircserv"
#define CHAN2 "ircnserv"

typedef struct {
    char msgv[RCMDMAX][MSGMAX];
    int n;
} Mensagens;

/*Comandos*/
int cmdPart(char *channel);
int cmdNick(char *entrada);
int cmdJoin(char *channel);
int cmdUser(char *middle[],int nmids, char *trail);
/*Auxiliares*/
Mensagens* parser(const char *entrada);
int isNickValid(char *entrada);
int isChanValid(char *entrada);
int existFile(char* filepath);
int removeLineFromFile(char* linein, char* filename);

/*variaveis globais*/
char nick[NICKMAX];
int flagLogged = 0; 
int flagNickInitial = 0; 

/*Final deste trecho*/

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

   /*trecho adicionado para a criacao dos canais hardcoded e estrutura de arquivos*/
   char path[PATHMAX];
   
   mkdir(PATHCHAN, 0755);
   mkdir(PATHCHAT, 0755);
   mkdir(PATHSERVER, 0755);
   strcpy(path, PATHSERVER);
   strcat(path, USERSFILE);
   fclose(fopen(path, "w"));
   strcpy(path, PATHCHAN);
   strcat(path, CHAN1);
   fclose(fopen(path, "w"));
   strcpy(path, PATHCHAN);
   strcat(path, CHAN2);
   fclose(fopen(path, "w"));
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
    char *middle[MIDMAX];
    char *trail;
    char *tmp;
    int nmids;
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
        /***/
        if(TESTE_NIVEL_1){
            printf("Parser aqui==> \"%s\"\n", sulfixo);
        }
        /***/
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
        /***/
        if(TESTE_NIVEL_1){
            printf("Parser: entrou no CDM = NICK\n");
        }
        /***/
        switch(cmdNick(middle[0])){
            case 1:
                /*criar resposta de ok - ja tinha nick -> mudou*/
                retorno->n = 2;
                strcpy(retorno->msgv[0], ":ircserv NOTICE * :***Changing your nick...\n");
                strcpy(retorno->msgv[1], ":ircserv NOTICE * :***DONE...\n");
                break;
            case 0:
                /*criar resposta de ok - nao tinha nick -> criou*/
                retorno->n = 3;
                strcpy(retorno->msgv[0], ":ircserv NOTICE * :***Setting your nick...\n");
                strcpy(retorno->msgv[1], ":ircserv NOTICE * :***DONE...\n");
                strcpy(retorno->msgv[3], ":ircserv NOTICE * :*** Looking up your hostname...\n");
                break;
            case -1:
                /*criar resposta de nick em uso*/
                retorno->n = 1;
                strcpy(retorno->msgv[0], ":ircserv 433");
                strcat(retorno->msgv[0], middle[0]);
                strcat(retorno->msgv[0], " :Nickname is already in use\n");
                break;
            case -2:
                /*criar resposta de badnick*/
                break;
            default: ;
                /*deu merda*/
        }
    }
    /*USER*/
    else if(!strcmp(cmd, "USER") && flagNickInitial){
        flagNickInitial = 0;
        flagLogged = 1;
        switch(cmdUser(middle, nmids, trail)){
          case 0:
              retorno->n = 1;
              strcpy(retorno->msgv[0], ":ircserv NOTICE * :*** Welcome...\n");
              break;
          default: ;
              /*deu merda*/
        }
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
        switch(cmdJoin(middle[0])){
            case 1:
                /*criar resposta de ok - ja tinha canal-> adicionou*/
                retorno->n = 1;
                strcpy(retorno->msgv[0], ":ircserv NOTICE * :*** Adicionado ao Canal...\n");
            case 0:
                /*criar resposta de ok - nao tinha canal-> criou/adicionou*/
                retorno->n = 1;
                strcpy(retorno->msgv[0], ":ircserv NOTICE * :*** Canal Criado...\n");
                break;
            case -1:
                /*criar resposta de canal protejido*/
                break;
            case -2:
                /*criar resposta de badchan*/
                break;
            default: ;
                /*deu merda*/
        }
    }
    
    /*QUIT*/
    else if(!strcmp(cmd,"QUIT") && flagLogged){
    }
    
    /*PART*/
    else if(!strcmp(cmd,"PART") && flagLogged){
        if(isChanValid(middle[0])){
            printf("PART: chan valido\n");
            /*verificar se ja tinha chan*/
            cmdPart(&middle[0][1]);
        }
        else
            /*retornar codigo de badChan*/
            printf("PART: Chan invalido\n");
    }

    return retorno;
}
/***************COMANDOS**************/
/**NICK**/
int cmdNick(char *entrada){
    char filename1[PATHMAX], filename2[PATHMAX];
    char chanpath[PATHMAX];
    char oldnick[NICKMAX];
    char chan[CHANMAX];
    FILE *fp;
    char *line;
    size_t len;
    ssize_t read;

    if(isNickValid(entrada)){
    /***/
    if(TESTE_NIVEL_1){
        printf("NICK: nick valido\n");
    }
    /***/
        /*verificar se ja tinha Nick*/
        /*criar arquivo de Nick se nao colidir*/
        strcpy(filename1, PATHCHAT);
        strcat(filename1,entrada);
        if(!existFile(filename1)){
            /*Verifica se User ja tinha nick*/
            if(nick[0] != '9'){
            /*sim - muda o nome dos arquivos*/
                strcpy(filename2, PATHCHAT);
                strcat(filename2,nick);
                rename(filename2, filename1);
                strcat(filename1,".chan");
                strcat(filename2,".chan");
                rename(filename2, filename1);
                /*verifica se ja esta logado*/
                if(flagLogged){
                    /*sim - muda o nick nos canais*/
                    if((fp = fopen(filename1, "r")) != NULL){
                        strcpy(oldnick, nick);
                        strcpy(nick, entrada);
                        /*atualizar nos canais*/
                        line = malloc(TAMLINEMAX * sizeof(char));
                        while((read = getline(&line, &len, fp)) != -1){
                            line[strlen(line) - 1] = '\0';
                            printf("NICK: line: \"%s\"\n", line);
                            strcpy(chanpath, PATHCHAN);
                            strcat(chanpath, line);
                            printf("NICK: chanpath: \"%s\"\n", chanpath);
                            removeLineFromFile(oldnick,chanpath);
                            strcpy(chan, "#");
                            strcat(chan, line);
                            cmdJoin(chan);
                        }
                        if(line) free(line);
                        fclose(fp);
                        /*atualizar em server/users*/
                        strcpy(filename1, PATHSERVER);
                        strcat(filename1, USERSFILE);
                        removeLineFromFile(oldnick,filename1);
                        if((fp = fopen(filename1, "a")) != NULL){
                            fprintf(fp, "%s\n", nick);
                            fclose(fp);
                        }
                    }
                    else{
                        strcpy(nick, entrada);
                    }
                    return 1;
                }
                else{
                    strcpy(nick, entrada);
                    return 1;
                }

            }
            else{
            /*nao - cria arquivos*/
                printf("path: %s\n", filename1);
                fclose(fopen(filename1,"w"));
                strcat(filename1,".chan");
                fclose(fopen(filename1,"w"));
                strcpy(nick, entrada);
                flagNickInitial = 1;
                return 0;
            }
        }
        else{
            /*retornar codigo de nick em uso*/
            /***/
            if(TESTE_NIVEL_1){
                printf("nick ja existe: %s \n", entrada);
            }
            /***/
            return -1;
        }
    }
    else{
        /*retornar codigo de badnick*/
        /***/
        if(TESTE_NIVEL_1){
            printf("Nick invalido\n");
        }
        /***/
        return -2;
    }
}
/**USER**/
int cmdUser(char *middle[],int nmids, char *trail){
    FILE *fp;

    int i;
    char path[PATHMAX];
    char nickNewLine[NICKMAX];
    char filename1[FILENAMEMAX];
    strcpy(filename1, PATHCHAT);
    strcat(filename1, nick);
    strcpy(path, PATHSERVER);
    strcat(path, USERSFILE);
    nickNewLine[0] ='\0';
    fp = fopen(filename1, "w");
    fprintf(fp, "%s", "USER");
    for(i = 0; i < nmids; i++){
        fprintf(fp, " %s", middle[i]);
    }
    if(trail != NULL)
       fprintf(fp, " %s", trail);
    fprintf(fp, "\n");
    fclose(fp);

    fp = fopen(path, "a");
    strcpy(nickNewLine, nick);
    strcat(nickNewLine, "\n");
    fprintf(fp, "%s", nickNewLine);

    fclose(fp);
    return 0;
}

/**LIST**/
/**JOIN**/
int cmdJoin(char *channel){
    char filename1[FILENAMEMAX], filename2[FILENAMEMAX];
    FILE *fp;

    if(isChanValid(channel)){
        /***/
        if(TESTE_NIVEL_1){
            printf("JOIN: chan valido\n");
        }
        /***/
        /*verificar se ja tinha chan*/
        strcpy(filename1, PATHCHAN);
        strcat(filename1, &channel[1]);
        strcpy(filename2, PATHCHAT);
        strcat(filename2, nick);
        strcat(filename2, ".chan");
        /***/
        if(TESTE_NIVEL_1){
            printf("JOIN: chan name : \"%s\"\n", filename1);
        }
        /***/
        if(!existFile(filename1)){
            /*cria arquivos*/
            fp = fopen(filename1, "w");
            fprintf(fp, "%s\n", nick);
            fclose(fp);
            fp = fopen(filename2, "a");
            fprintf(fp, "%s\n", &channel[1]);
            fclose(fp);
            return 0;
        }
        else{
            /*adicionar nick no filename1*/
            removeLineFromFile(nick, filename1);
            fp = fopen(filename1, "a");
            fprintf(fp, "%s\n", nick);
            fclose(fp);
            removeLineFromFile(&channel[1], filename2);
            fp = fopen(filename2, "a");
            fprintf(fp, "%s\n", &channel[1]);
            fclose(fp);
            return 1;
            /*criar resposta*/
        }
    }
    else{
        /*retornar codigo de badChan*/
        /***/
        if(TESTE_NIVEL_1){
            printf("JOIN: chan invalido\n");
        }
        /***/
        return -2;
    }
}
/**PART**/
int cmdPart(char *channel){
    char filename[FILENAMEMAX];
    char line[TAMLINEMAX];

    printf("CMDPART: recebeu channel: \"%s\"\n", channel);
    strcpy(filename, PATHCHAN);
    strcat(filename, channel);
    
    strcpy(line, nick);
    strcat(line, "\n");

    removeLineFromFile(line, filename);

    return 0;
}

/**********FUNCOES AUXILIARES*********/

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

int existFile(char* filepath){
    if(access(filepath, F_OK) != -1)
        return 1;
    else
        return 0;
}

int removeLineFromFile(char *entrada, char* filename){
    FILE *fp1, *fp2;
    char *line;
    size_t len;
    ssize_t read;
    char filenamebkp[FILENAMEMAX];
    char linein[TAMLINEMAX];
    int lineinTam;

    strcpy(linein, entrada);
    lineinTam = strlen(linein);
    if(linein[lineinTam - 1] != '\n'){
        linein[lineinTam] = '\n';
        linein[lineinTam + 1] = '\0';
    }
    /***/
    if(TESTE_NIVEL_1){
        printf("REMOVELINEFROMFILE: line in = \"%s\"\n", linein);
    }
    /***/

    if(existFile(filename)){
        if((fp1 = fopen(filename, "r+")) != NULL){
            strcpy(filenamebkp, filename);
            strcat(filenamebkp, "BKP");
            if((fp2 = fopen(filenamebkp, "w")) != NULL){
                line = malloc(TAMLINEMAX * sizeof(char));
                while((read = getline(&line, &len, fp1)) != -1){
                    printf("REMOVEFROMLINE: entrou no while e linha é \"%s\"\n",line);
                    if(strcmp(linein, line))
                        fprintf(fp2,"%s", line);
                }
                printf("REMOVEFROMLINE: passou do while\n");
                if(line) free(line);
                if(ftell(fp2)){
                    fclose(fp2);
                    fclose(fp1);
                    remove(filename);
                    rename(filenamebkp, filename);
                }
                else{
                    fclose(fp2);
                    fclose(fp1);
                    remove(filename);
                    remove(filenamebkp);

                }

            }
            else{
                return -3; /* ERRO - nao pode criar fileBKP */
                fclose(fp1);
            }
        }
        else
            return -2; /* ERRO - file em uso */


    }
    return -1; /* ERRO - file nao existe */
}
    
