#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>

#define BUFSZ 1024

void logexit(const char *str)
{
	perror(str);
	exit(EXIT_FAILURE);
}

char * encrypt(int offset, char *string) {
	if (offset > 25) offset = offset%26;

	for(int i = 0; i < strlen(string); i++) {
		int enc = (int)string[i] + offset;
		if(enc > 122) enc -= 26;
		string[i] = (char)enc;
	}

	return string;
}

int main(int argc, char *argv[]) {
	int s;

	struct in_addr inaddr;
	if(inet_pton(AF_INET, "127.0.0.1", &inaddr) < 1)
		logexit("pton");

	struct sockaddr_in addr;
	struct sockaddr *addrptr = (struct sockaddr *)&addr;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(5000);
	addr.sin_addr = inaddr;

	s = socket(AF_INET, SOCK_STREAM, 0);
	if(s == -1) logexit("socket");

	struct timeval tout;
	tout.tv_sec = 15;
	tout.tv_usec = 0;
	if(setsockopt(s, SOL_SOCKET, SO_RCVTIMEO, &tout, sizeof(tout)))
		logexit("socket-opt");

	if(connect(s, addrptr, sizeof(struct sockaddr_in)))
		logexit("connect");

	char *to_send = "stringtosend\n";

	ssize_t count;
	uint16_t size = htons(strlen(to_send));
	count = send(s, &size, sizeof(size), 0);
	if(count != sizeof(size)) logexit("send");

	count = send(s, to_send, strlen(to_send), 0);
	if(count != strlen(to_send)) logexit("send");

	char sync[8];
	count = recv(s, &sync, sizeof(sync), 0);
	if(count != sizeof(sync)) logexit("receive");
	printf("Received sync: %s\n", sync);

	count = recv(s, &sync, sizeof(sync), 0);
	if(count != sizeof(sync)) logexit("receive");
	printf("Received sync: %s\n", sync);

	char data_size[4];
	count = recv(s, &data_size, sizeof(data_size), 0);
	if(count != sizeof(data_size)) logexit("receive");
	printf("Received size: %s\n", data_size);

	char checksum[4];
	count = recv(s, &checksum, sizeof(checksum), 0);
	if(count != sizeof(checksum)) logexit("receive");
	printf("Received checksum: %s\n", checksum);

	char id[2];
	count = recv(s, &id, sizeof(id), 0);
	if(count != sizeof(id)) logexit("receive");
	printf("Received ID: %s\n", id);

	char flags[2];
	count = recv(s, &flags, sizeof(flags), 0);
	if(count != sizeof(flags)) logexit("receive");
	printf("Received flags: %s\n", flags);

	char *string = malloc(40);
	if(!string) logexit("malloc");
	count = recv(s, string, 40, 0);
	if(count != 40) logexit("receive");
	printf("Received data: %s\n", string);

	close(s);
	exit(EXIT_SUCCESS);
}

