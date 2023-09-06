import threading
import HttpRequest
import HttpResponse
import time

# Connecting Pools
connection_pool = {}


#  https://blog.csdn.net/linxinfa/article/details/104001443
def acceptNewClient(server_socket):
    """
    Acceptance of new connections
    """
    # Wait for new client connections
    client_connection, client_address = server_socket.accept()
    # Create a separate thread for each client to manage
    thread = MyThread(client_connection, client_address)
    thread.daemon = True
    thread.start()


def manageTimeout(request):
    """
    To manage timeout. If 'removeClient()' is called, this function will return true, and the tread should be closed.
    :param request:
    """
    while True:
        current_time = time.time()
        if request.client_connection in connection_pool:
            client = connection_pool[request.client_connection]
            if client.end_time < current_time:
                removeClient(request)
                break


def removeClient(request: HttpRequest.Request) -> None:
    """
     To remove the client who close its connection
    :rtype: HttpRequest.Request
    :param request:
    """
    client = connection_pool[request.client_connection]
    if request.__eq__(client) and client is not None:
        client.client_connection.close()
        # To protect the connection_pool
        lock = threading.Lock()
        lock.acquire()
        connection_pool.pop(request.client_connection)
        lock.release()
        print("client offline: {}\n".format(str(request.client_host_name)))


# For keep-live, we should count number of cycles for each thread
class MyThread(threading.Thread):
    def __init__(self, client_connection, client_address):
        threading.Thread.__init__(self)
        self.client_connection = client_connection
        self.client_address = client_address
        self.first_time = True
        self.number = 0

    def run(self):
        """
        To handle messages
        """
        while True:
            try:
                # Get the client request
                originalRequest = self.client_connection.recv(1024).decode()
                print(originalRequest+'\n')
                # analyze the request
                request = HttpRequest.Request(originalRequest, self.client_connection, self.client_address)
                # I always get some empty requests, and I don't know why
                if request.method is None:
                    break

                # Get HTTP response
                response = HttpResponse.Response(request)

                # Store the records in a log file
                logList = response.setRecord()
                logFile = open("log.txt", "a+")
                line = "[" + ",".join(logList) + "]\n"
                logFile.write(line)
                logFile.close()

                # Set HTTP response
                returnableResponse = response.returnableResponse()
                self.client_connection.sendall(returnableResponse.encode())
                if response.content_type is not None and response.content_type.startswith("image"):
                    self.client_connection.sendall(response.entity_body)

                # https://www.jb51.net/article/204072.htm
                lock = threading.Lock()
                if request.connectionOrNot:
                    # To protect the connection_pool
                    lock.acquire()
                    connection_pool[self.client_connection] = request
                    lock.release()
                    timeout = response.keep_alive.timeout
                    if timeout < 0:
                        raise ValueError("'timeout' must be a non-negative number")
                    else:
                        end_time = request.access_time.calculable_time + timeout
                        request.setEndTime(end_time)
                        if end_time < time.time():
                            removeClient(request)

                    # Set timeout
                    if self.first_time:
                        self.first_time = False
                        # Build a thread to clean this thread when conditions met
                        threading.Thread(target=manageTimeout, args=(request,)).start()

                    # For maximum number of connections for keep-alive
                    self.number += 1
                    if self.number >= response.keep_alive.max:
                        removeClient(request)
                else:
                    self.client_connection.close()

            except (ConnectionAbortedError, OSError):
                pass
