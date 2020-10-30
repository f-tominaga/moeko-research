#include <iostream>
#include <stdio.h>
#include <stdlib.h>

#include "SOM_Client.h"

int main()
{
	std::cout << "Sample SOM client\n";
	SOM_Client *som_client = new SOM_Client();
	som_client->init();
	som_client->open();

	som_client->close();
}

