import socket
import sys
import cgi

# serverSocket.close()
# sys.exit()
# Kích hoạt server


def activeServer(serverAddres, serverPort):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((serverAddress, serverPort))
    serverSocket.listen(2)
    print("Ready, waiting for request")
    while True:
        connectionSocket, connectionAddress = serverSocket.accept()
        print("Received a request from Address: {0}".format(connectionAddress))
        try:
            massage = connectionSocket.recv(2048).decode()
            massages = massage.split(' ')
            method = massages[0]
            if(method == "GET"):
                sendLoginForm(connectionSocket)
            elif(method == "POST"):
                string = massages.pop()
                splitArr = string.split("\n")
                string = splitArr[len(splitArr)-1]
                temp = getUsernameAndPassword(string)
                checkUsernameAndPassword(temp[0], temp[1])
                print(temp[0]+" "+temp[1])
                sendInfoFile(connectionSocket)
            connectionSocket.close()
        except IOError:
            pass




def getUsernameAndPassword(string):
    temp = string.split('&')
    usnPart = temp[0]
    passWordPart = temp[1]
    usn = usnPart.split('=')
    psw = passWordPart.split('=')
    return [usn[1], psw[1]]


def checkUsernameAndPassword(usn, psw):
    pass


serverAddress = "127.0.0.1"
serverPort = 80
activeServer(serverAddress, serverPort)
