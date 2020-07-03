import socket
import sys


def send_html_file(socket, filename):
    try:
        http_header1 = "HTTP/1.1 200 OK\r\n"
        http_header2 = "Content-Type: text/html\r\n"
        file_stream = open(filename, encoding="utf8")
        sending_data = file_stream.read()
        print("Find found.")
        socket.send(http_header1.encode())
        socket.send(http_header2.encode())
        socket.send("\r\n".encode())
        for i in range(0, len(sending_data)):
            socket.send(sending_data[i].encode())
        socket.send("\r\n".encode())
        print("File sent: " + filename)
    except IOError:  # khi không tìm thấy file
        print("Can't find the file, send 404")
        file_stream = open("404.html", encoding="utf8")
        sending_data = file_stream.read()
        http_error_header = "HTTP/1.1 404 Not Found\r\n"
        http_header2 = "Content-Type: text/html\r\n"
        socket.send(http_error_header.encode())
        socket.send(http_header2.encode())
        socket.send("\r\n".encode())
        for i in range(0, len(sending_data)):
            socket.send(sending_data[i].encode())
        socket.send("\r\n".encode())
        print("File sent: " + "404.html")


def activeServer(serverAddress, serverPort):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((serverAddress, serverPort))
    serverSocket.listen(2)
    print("Ready, waiting for request")
    true_login_info = False
    while True:
        connectionSocket, connectionAddress = serverSocket.accept()
        print("Received a request from Address: {0}".format(connectionAddress))
        massage = connectionSocket.recv(2048).decode()
        massages = massage.split(' ')
        method = massages[0]
        if(method == "GET"):
            if(massages[1] == "/"):
                redirect(connectionSocket, "/login.html")
            elif(massages[1] == "/login.html"):
                send_html_file(connectionSocket, "login.html")
                true_login_info = False
            elif(massages[1] == "/info.html" and true_login_info):
                send_html_file(connectionSocket, "info.html")
            elif(massages[1] == "/404.html"):
                send_html_file(connectionSocket, "")
            else:
                redirect(connectionSocket, "/login.html")
        elif(method == "POST"):
            string = massages.pop()
            splitArr = string.split("\n")
            string = splitArr[len(splitArr)-1]
            temp = getUsernameAndPassword(string)
            true_login_info = checkUsernameAndPassword(temp[0], temp[1])
            if(true_login_info):
                redirect(connectionSocket, "/info.html")
            else:
                redirect(connectionSocket, "/404.html")
            connectionSocket.close()


def getUsernameAndPassword(string):
    temp = string.split('&')
    usnPart = temp[0]
    passWordPart = temp[1]
    usn = usnPart.split('=')
    psw = passWordPart.split('=')
    return [usn[1], psw[1]]


def checkUsernameAndPassword(usn, psw) -> bool:
    if usn == "admin" and psw == "admin":
        return True
    else:
        return False


def redirect(socket, url):
    http_header1 = "HTTP/1.1 302 Found\r\n"
    location = "Location: "+url+"\r\n"
    socket.send(http_header1.encode())
    socket.send(location.encode())
    socket.send("\r\n".encode())
    print("direct to "+url)


serverAddress = "127.0.0.1"
serverPort = 80
activeServer(serverAddress, serverPort)
