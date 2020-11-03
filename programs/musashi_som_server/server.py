# -*- coding: utf-8 -*-
import socket
import socketserver
import threading
import struct


class Server:
    def __init__(self,):
        print('create multi client server')
        host = '172.16.44.101'
        port= 7000
        self.info = (host,port)
        print('server info:{}'.format(self.info))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = [] #client array
        self.threads = [] #thread array
        
        self.init()
        
    def init(self,): #for override
        pass
        
    def listen(self,num_client:int):
        print('socket bind')
        self.sock.bind(self.info)
        self.sock.setsockopt(socket.SOL_SOCKET,
                              socket.SO_REUSEADDR,
                              1)
        print('allow client {}'.format(num_client))
        self.sock.listen(num_client)
        self.sock.settimeout(1)
        
    def start(self,):
        while True:
            try:
                conn,addr = self.sock.accept()
                self.clients.append((conn, addr))
                print("new client")
                thread = threading.Thread(target=self.proccess,
                                          args=(conn, addr))
                thread.setDaemon(True)
                thread.start()
                # self.threads.append(thread)
                
            except socket.timeout:
                if len(self.clients)==0:
                    print('wait client ... {}'.format(len(self.clients)))

                else:
                    print('client num:{}'.format(len(self.clients)))
                continue
        
    def proccess(self, connection:socket.socket, address):
        pass
    
    def close(self,):
        self.sock.close()
        
# class TCPHandler(socketserver.BaseRequestHandler):   
#     def setup(self,):
#         pass
    
#     def handle(self,):
#         while True:
#             self.data = self.request.recv(1024).strip()
#             print(self.data)
    
#     def finish(self,):
#         print('close')
#         pass

if __name__=='__main__':
    server = Server()
    server.listen(num_client=5)
    server.start()
    server.close()
    # with socketserver.TCPServer(('127.0.0.1',7001), TCPHandler) as server:
        # server.serve_forever()
    
    
    
    
    
    
    
    
    
    
    
    
    