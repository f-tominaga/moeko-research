#include <iostream>
#include <stdio.h>
#include <stdlib.h>

#include "SOM_Client.h"

int main()
{
	std::cout << "Sample SOM client\n";
	SOM_Client *som_client = new SOM_Client();
	som_client->init();
	som_client->open("127.0.0.1", 7000);

	SOM_Client_Info::Send_t send;
	SOM_Client_Info::Recv_t recv;
	
	//set send values
	send.x = 1.0;
	send.y = 1.0;
	send.d_alpha = 2.0;
	send.d_beta = 3.0;
	send.d_gamma = 4.0;
	send.have_ball = 0;

	//send and recieve
	som_client->get(send, recv);
	
	//show reply
	printf(":>%d\n", recv.action);

	som_client->close();
}

