#pragma once
#ifndef _WINSOCK_DEPRECATED_NO_WARNINGS
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#endif

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <winsock2.h>
#include <string>

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
	int open(std::string IP, int port);
	int close();

	int get(SOM_Client_Info::Send_t s, SOM_Client_Info::Recv_t &r);

private:
	SOCKET sock;
	struct sockaddr_in addr;
};

