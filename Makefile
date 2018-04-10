all:
	gcc -Wall client.c -o client

clean:
	rm -f client server server-mt
