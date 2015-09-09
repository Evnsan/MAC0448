CFLAGS=-Wall -ansi -pedantic
CC=gcc
NAME=ircserv
CHANFILE=chan
USERSFILE=users

ircserv: 
	$(CC) $(CFLAGS) $(NAME).c -o $(NAME)

.PHONY: clean
clean:
	rm $(NAME) $(CHANFILE)/* $(USERSFILE)/* 
