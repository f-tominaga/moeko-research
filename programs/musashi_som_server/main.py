# -*- coding: utf-8 -*-
import socket
#from musashi_som_server import som
#from musashi_som_server import server
import som
import server
import struct

class SOM_Server(server.Server):
    def init(self,):
        print('SOM_Server init')
        self.som = som.SOM()
        self.som.open('cfg/test.json')

    def proccess(self, connection:socket.socket, address):
        print('wait data ...')
        while True:
            try:
                sim_data = connection.recv(40) #recieve
                sim_data = struct.unpack('fffffiiiii', sim_data) #バイナリファイルをunpack
                print(sim_data)
                function = self.som.ploof(sim_data)
                function = struct.pack('i', int(function))
                connection.send(function)

            except Exception as ex:
                print(ex)
                break
        return

    def debug(self,):
        sim_data = [5.0, 3.5, 4.3, 2.1, 2.0, 2, 3, 1, 0, 2]
        print('sim_data', sim_data)
        self.som.ploof(sim_data)

if __name__=='__main__':
    som_server = SOM_Server()
    #som_server.debug()
    som_server.listen(num_client=5)
    som_server.start()
    som_server.close()