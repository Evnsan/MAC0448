CFLAGS=-Wall -ansi -pedantic -std=gnu99
CC=gcc
NAME=ircserv

ircserv: lex.yy.c $(NAME).tab.c $(NAME).tab.h
	$(CC) $(CFLAGS) $(NAME).tab.c lex.yy.c $(NAME).c -lfl -o $(NAME)

$(NAME).tab.c $(NAME).tab.h: $(NAME).y
	bison -d $(NAME).y

lex.yy.c: $(NAME).l $(NAME).tab.h
	flex $(NAME).l

.PHONY: clean

clean:
	rm $(NAME) *.h $(NAME).tab.c 
