# -*- coding: utf-8 -*-
import socket
import som
import server

class SOM_Server(server.Server):
    def init(self,): #@override
        self.som = som.SOM()
        self.som.open()
        
    def proccess(self, connection:socket.socket, address): #@override
        #proccess
        pass
        
if __name__=='__main__':
    som_server = SOM_Server()
    som_server.listen(num_client=5)
    som_server.start()
    som_server.close()