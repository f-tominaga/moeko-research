#pragma once
#ifndef _WINSOCK_DEPRECATED_NO_WARNINGS
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#endif

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <winsock2.h>

class SOM_Client
{
public:
	SOM_Client();
	~SOM_Client();

	int init();
	int open();
	int close();

	int send();

private:
	SOCKET sock;
	struct sockaddr_in addr;
};

