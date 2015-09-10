CFLAGS=-Wall -ansi -pedantic
CC=gcc
NAME=ircserv
CHANFILE=chan
USERSFILE=users
SERVERFILE=server

ircserv: 
	$(CC) $(CFLAGS) $(NAME).c -o $(NAME)

.PHONY: clean
clean:
	rm $(NAME) $(CHANFILE)/* $(USERSFILE)/* $(SERVERFILE)/*
