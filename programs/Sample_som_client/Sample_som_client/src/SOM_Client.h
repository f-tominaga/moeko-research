#pragma once
#ifndef _WINSOCK_DEPRECATED_NO_WARNINGS
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#endif

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <winsock2.h>


namespace SOM_Client_Info
{
	struct Send_t {
		float x, y;
		float d_alpha, d_beta, d_gamma;
		int have_ball;
	};

	struct Recv_t {
		int action;
	};
}

class SOM_Client
{
public:
	SOM_Client();
	~SOM_Client();

	int init();
	int open();
	int close();

	int _send(SOM_Client_Info::Send_t send);

private:
	SOCKET sock;
	struct sockaddr_in addr;
};

