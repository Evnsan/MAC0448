%{

#include <stdio.h>
extern int yylex();
extern int yyparse();
extern FILE *yyin;
     
void yyerror(const char *s);

%}

%union {
    int ival;
    float fval;
    char *sval;
}

%token <ival> INT
%token <fval> FLOAT
%token <sval> STRING

%%

snazzle:
    snazzle INT { printf("bison found a int \"%d\"\n", $2); }
    | snazzle FLOAT { printf("bison found a float \"%f\"\n", $2); }
    | snazzle STRING { printf("bison found a string \"%s\"\n", $2); }
    | INT            { printf("bison found a int \"%d\"\n", $1); }
    | FLOAT          { printf("bison found a float \"%f\"\n", $1); }
    | STRING         { printf("bison found a string \"%s\"\n", $1); }
    ;

%%

int parser(FILE *myfile) {
    yyin = myfile;
    do{
        yyparse();
        printf("terminou mais uma\n");
    }while(!feof(yyin));

    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "EEK, Parser error! Mensage: %s\n", s);
}
