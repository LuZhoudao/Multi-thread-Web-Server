# For multi-thread
import MyThread
# import the socket library
import socket

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(128)
print('Listening on port %s ...\n' % SERVER_PORT)

while True:
    MyThread.acceptNewClient(server_socket)

# Close socket
server_socket.close()
