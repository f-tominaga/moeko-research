#include "SOM_Client.h"

SOM_Client::SOM_Client()
{


}

SOM_Client::~SOM_Client()
{

}

int SOM_Client::init()
{
	WSADATA wsa;

	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
		printf("Failed. Error Code:%d\n", WSAGetLastError());
		return -1;
	}

	sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock == INVALID_SOCKET) {
		printf("Could not create socket:%d\n", WSAGetLastError());
		return -1;
	}

	addr.sin_family = AF_INET;
	addr.sin_port = htons(7000);
	addr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");

	printf("Initialized.\n");
	return 0;
}

int SOM_Client::open()
{
	int ret = 0;
	ret = connect(sock, (struct sockaddr*)&addr, sizeof(struct sockaddr));

	if (ret < 0) {
		printf("Connection Error:%d\n", WSAGetLastError());
		return -1;
	}

	return 0;
}

int SOM_Client::close()
{
	closesocket(sock);
	WSACleanup();
	return 0;
}

int SOM_Client::send()
{
	return 0;
}
