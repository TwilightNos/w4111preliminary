#!/usr/bin/env python3.10
from socket import *


class Proxy:
    def __init__(self, serverPort, clientPort, clientIp, serverIp):
        self.serverPort = serverPort
        self.clientPort = clientPort
        self.clientConnector = socket(AF_INET, SOCK_STREAM)
        self.clientIp = clientIp
        self.serverIp = serverIp
        self.clientConnector.bind((self.clientIp, self.clientPort))
        self.serverConnector = None

    def listening_to_client(self, listenNumber):
        self.clientConnector.listen(listenNumber)

    def connect_to_client(self):
        print('waiting for connection from client...')
        clientConnectionSocket, addr = self.clientConnector.accept()
        print('connection with client created.\nwaiting for connection to server...')
        return clientConnectionSocket,addr

    def connect_to_server(self):
        serverConnector = socket(AF_INET,SOCK_STREAM)
        serverConnector.connect((self.serverIp,self.serverPort))
        print('connection with server created.')
        return serverConnector

    def receive_msg_from_client(self,clientConnectionSocket):
        print('waiting for message from client...')
        message = clientConnectionSocket.recv(2048).decode()
        return message

    def send_msg_to_server(self,serverConnector,message):
        serverConnector.send(message.encode())

    def receive_msg_from_server(self,serverConnector):
        serverMessage = serverConnector.recv(2048).decode()
        print('Message received from server: '+serverMessage)
        return serverMessage

    def send_msg_to_client(self,clientConnectionSocket,serverMessage):
        clientConnectionSocket.send(serverMessage.encode())

    def close_all_sockets(self,serverConnector,clientConnectionSocket):
        # serverConnector.close()
        # clientConnectionSocket.close()
        self.clientConnector.close()


def main():
    proxy = Proxy(serverPort=8080, clientPort=1010, clientIp='localhost', serverIp='127.0.0.1')
    proxy.listening_to_client(3)
    running = True
    while running:
        clientConnectionSocket, addr = proxy.connect_to_client()
        serverConnector = proxy.connect_to_server()
        while True:
            message = proxy.receive_msg_from_client(clientConnectionSocket=clientConnectionSocket)
            if not message:
                clientConnectionSocket.close()
                break
            print('Message ' + message + ' from client:' + str(addr))
            proxy.send_msg_to_server(serverConnector=serverConnector, message=message)
            if message == 'exit':
                proxy.close_all_sockets(clientConnectionSocket=clientConnectionSocket, serverConnector=serverConnector)
                running = False
                break
            serverMessage = proxy.receive_msg_from_server(serverConnector=serverConnector)
            proxy.send_msg_to_client(clientConnectionSocket=clientConnectionSocket, serverMessage=serverMessage)
        serverConnector.close()
        clientConnectionSocket.close()
        print('proxy closed.')


if __name__ == '__main__':
    main()



