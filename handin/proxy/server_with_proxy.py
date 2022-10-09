import time
from socket import *



if __name__ == '__main__':
    # create serverPort
    serverPort = 8080
    serverIP = '127.0.0.1'
    # listening to connection from proxy
    proxyConnector = socket(AF_INET, SOCK_STREAM)
    # listening every connect with port number serverPort
    proxyConnector.bind((serverIP, serverPort))

    proxyConnector.listen(3)

    running = True
    while running:
        print('waiting for connection...')
        # get info from socket
        connectionSocket,addr = proxyConnector.accept()
        print('connect created.')
        while True:
            # get message from proxy
            message = connectionSocket.recv(2048).decode()
            # if there is no message, close the connection
            if message == 'exit':
                running = False
                break
            elif not message:
                connectionSocket.close()
                break
            print('Message '+ message+' received from proxy: '+str(addr))
            # send message to proxy
            connectionSocket.send(message.encode())
        # finish sending message, close the connection, waiting for next request
        connectionSocket.close()
        print('connect closed.')

    proxyConnector.close()
    print('server closed.')