CFLAGS=-Wall -ansi -pedantic 
CC=gcc

parsertest: lex.yy.c parsertest.tab.c parsertest.tab.h
	$(CC) $(CFLAGS) parsertest.tab.c lex.yy.c parsertest.c -lfl -o parsertest

parsertest.tab.c parsertest.tab.h: parsertest.y
	bison -d parsertest.y

lex.yy.c: parsertest.l parsertest.tab.h
	flex parsertest.l

.PHONY: clean

clean:
	rm parsertest *.h parsertest.tab.c 
