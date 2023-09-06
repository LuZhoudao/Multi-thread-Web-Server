COMP2322 Computer Networking
Multi-thread Web Server

This project aims to develop a socket program to implement a Web service using the HTTP protocol.



Base Interpreter:
Python 3.11




Usage:

Run:  MyHttpServer.py

The main codes: HttpRequest.py, HttpResponse.py, MyHttpServer.py, MyThread.py, and MyTime.py.

Help test: TestClient.py (Just copy from 'Lab5' to help do some test. There may be some errors because of it. The client programming isn't one part of the project so that I didn't adjust it.)

htdocs: htdocs is where the server's resource locate.




Design requirements
In this project, you are required to develop a multi-threaded Web server in Python that is
capable of processing HTTP requests sent from browsers or some other client programs.
This multi-threaded program will be able to handle multiple requests at the same time.
Specifically, your Web server will

(i) create a connection socket when contacted by a client (browser);
(ii) receive the HTTP request from this connection;
(iii) parse the request to determine the specific file being requested;
(iv) get the requested file from the server’s file system;
(v) create an HTTP response message consisting of the requested file preceded by
header lines;
(vi) send the response over the TCP connection to the requesting client. If the client
requests a file that is not present in your server, your server should return a “404
Not Found” error message.

Your task is to implement the server program, run your server program, and then test
your server program by sending requests from the client programs running on different
hosts. You may run the server on your own computer, using the IP address of 127.0.0.1. If
you run your server on a host that already has a Web server running on it, then you should
use a different port than port 80 for your Web server.

You can develop your code in two stages. In the first stage, you can simply implement the
server program to receive the HTTP request messages and display the contents. After this
is running properly, you can add the code to generate appropriate responses in the second
stage. The Web server needs a log file to record statistics of the client requests. Each
request corresponds to one line of record in the log. Write down client hostname/IP 
address, access time, requested file name and response type for each record. Your Web
server also needs to handle some simple errors, such as web-page not found.
You can use either Python, Java or C/C++ languages for the project. When implementing
the Web server, you are expected to use basic socket programming classes to build the
Web server from scratch instead of using the HTTPServer class directly.