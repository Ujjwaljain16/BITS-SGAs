CC = gcc
CFLAGS = -Wall -Wextra -O2

all: client

client: http_client.c
	$(CC) $(CFLAGS) http_client.c -o client

clean:
	rm -f client
