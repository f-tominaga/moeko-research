# -*- coding: utf-8 -*-
import socket
from musashi_som_server import som
from musashi_som_server import server

class SOM_Server(server.Server):
    def init(self,):
        self.som = som.SOM()
        self.som.open()

    def proccess(self, connection:socket.socket, address):
        #proccess
        pass

if __name__=='__main__':
    som_server = SOM_Server()
    som_server.listen(num_client=5)
    som_server.start()
    som_server.close()