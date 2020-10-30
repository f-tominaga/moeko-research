# -*- coding: utf-8 -*-
import socket
import som
import server
# from musashi_som_server import som
# from musashi_som_server import server

cfg = 'cfg/test.json'
max_client = 5

class SOM_Server(server.Server):
    def init(self,):
        self.som = som.SOM()
        self.som.open(cfg)

    def proccess(self, connection:socket.socket, address):
        
        pass

if __name__=='__main__':
    som_server = SOM_Server()
    som_server.listen(num_client=max_client)

    som_server.start()

    som_server.close()