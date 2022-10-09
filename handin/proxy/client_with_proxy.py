from socket import *

if __name__ == '__main__':
    # create a socket for connection
    serverIP = 'localhost'
    serverPort = 1010
    clientSocket = socket(AF_INET,SOCK_STREAM)
    # client try to connect to the proxy, input a tuple
    clientSocket.connect((serverIP,serverPort))

    # while cycle to provide continuous communicating
    while True:
        # try to send some message to proxy
        message = input('message send to proxy(enter exit to quit):')
        # if no message received, close the connection
        if not message:
            print('client closed')
            break
        # send the encoded message to proxy
        clientSocket.send(message.encode())
        if message == 'exit':
            print('client closed.')
            print('server and proxy closed.')
            break
        # wait for the proxy to send back message
        receivedMessage = clientSocket.recv(2048)
        print('From proxy: ' + receivedMessage.decode())
    # if there's no new message, close the socket
    clientSocket.close()