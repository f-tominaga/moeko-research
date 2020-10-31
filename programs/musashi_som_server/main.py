# -*- coding: utf-8 -*-
import socket
import som
import server
import struct
# from musashi_som_server import som
# from musashi_som_server import server

cfg = 'cfg/test.json'
max_client = 5

class SOM_Server(server.Server):
    def init(self,):
        self.som = som.SOM()
        self.som.open(cfg)

    def proccess(self, connection:socket.socket, address):
        
        #recieve process
        _recv = connection.recv(1024)
        recv = struct.unpack('fffffi', _recv)
        print(recv)
        
        #reply process
        action = 0
        send = struct.pack('i', action)
        connection.send(send)

if __name__=='__main__':
    som_server = SOM_Server()
    som_server.listen(num_client=max_client)

    som_server.start()

    som_server.close()