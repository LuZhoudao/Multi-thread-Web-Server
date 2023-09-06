# Implements a simple HTTP client
import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

# Example 1
txt1 = "GET /helloworld.html HTTP/1.1"
txt2 = "HEAD / HTTP/1.1"
txt3 = "GET /helloworld.html HTTP/1,1" # wrong input
txt4 = "ab" # wrong input
txt5 = "GET /polyU.jpg HTTP/1.1"
txt6 = " GET / HTTP/1.1\r\nIf-Modified-Since: Fri, 5 May 23 12:00:00 GMT\r\n"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
request = ''
while request != '-1':
    request = input('Input HTTP request command:\n')
    client_socket.send(request.encode())
    response = client_socket.recv(1024)
    print('Server response:\n')
    print(response.decode())

client_socket.close()
