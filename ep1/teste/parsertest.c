#include <stdio.h> 
#include "parsertest.tab.h"

int main(int args, char** argv){
    FILE *fp = fopen("parsertest.in", "r");
    if(fp){
        printf("Estamos onde queriamos\n");
        parser(fp);
        return 0;
    }
    else{
        fprintf(stderr, "I can't open parsertest.in\n");
        return -1;
    }
}
