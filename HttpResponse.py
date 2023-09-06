from enum import Enum
import os
import time
import MyTime


def handleNone(message):
    """
    To handle None in 'setRecord()'
    :param message:
    :return: str
    """
    if message is None:
        return "None"
    else:
        return message


# Handle the parameters (timeout, max) of keep-alive
class KeepAlive:
    def __init__(self, timeoutValue, maxValue):
        self.timeout = timeoutValue
        self.max = maxValue


# The HTTP response class
class Response:
    # Enum: https://juejin.cn/post/6844903901922066445
    class StatusCode(Enum):
        OK = "200 OK"
        BAD_REQUEST = "400 Bad Request"
        NOT_FOUND = "404 Not Found"
        NOT_MODIFIED = "304 Not Modified"

    def __init__(self, request):
        self.request = request
        self.version = request.version
        # In case of the version is wrong input, like HTTP/1,1
        self.status_code = None
        if self.version != "HTTP/1.1" and self.version != "HTTP/1.0":
            self.status_code = self.StatusCode.BAD_REQUEST
        self.date = MyTime.AccessTime()
        self.last_modified_time = None
        self.content_length = None
        self.content_type = None
        self.entity_body = None
        self.connectionOrNot = request.connectionOrNot
        self.keep_alive = None
        self.handle_request(request)

    def setWrongFile(self):
        fin = None
        if self.status_code is not None and self.status_code is not self.StatusCode.OK:
            self.request.setSpecificStatusCode("{}.html".format(self.status_code.value[:3]))
            file_path = 'htdocs/' + self.request.URL
            fin = open(file_path, 'r')
            content = fin.read()
            fin.close()
            self.content_length = len(content)
            self.entity_body = content

    # Handle the extension of the files
    def handle_extension(self, extension):
        if extension == "png" or extension == "jpg":
            self.content_type = f"image/{extension}"
            return extension
        elif extension == "html":
            self.content_type = f"text/html"
            return "html"

    # Handle the request
    def handle_request(self, request):
        # access the request type
        request_type = request.method
        request_file = request.URL
        file_path = 'htdocs/'
        if request_file is None:
            self.status_code = self.StatusCode.BAD_REQUEST
        else:
            file_path += request_file

        if self.status_code is None:
            try:
                # Record the last modified time
                # https://juejin.cn/s/python%20%E6%9F%A5%E7%9C%8B%E6%96%87%E4%BB%B6%E6%9C%80%E5%90%8E%E4%BF%AE%E6%94%B9%E6%97%B6%E9%97%B4
                last_modified_time = os.path.getmtime(file_path)
                self.last_modified_time = MyTime.Time(
                    time.strftime('%a, %d %b %y %H:%M:%S GMT', time.localtime(last_modified_time)))
                # Handle the method and open this file
                fin = None
                if request_type == "GET" or request_type == "HEAD":
                    # Get the extension of the file
                    extension = self.handle_extension(os.path.splitext(request_file)[1][1:])
                    # Decide the reading style
                    if extension == "html":
                        fin = open(file_path, 'r')
                    elif extension == "png" or extension == "jpg":
                        fin = open(file_path, 'rb')
                    content = fin.read()
                    fin.close()
                    self.content_length = len(content)
                    if request_type == "GET":
                        self.entity_body = content
                    self.status_code = self.StatusCode.OK
                else:
                    self.status_code = self.StatusCode.BAD_REQUEST

            # If there is no file, should return "404 Not Found"
            except FileNotFoundError:
                self.status_code = self.StatusCode.NOT_FOUND

        # set the value of 'Keep-alive', I just set timeout = 100, max = 1000 by default
        if self.connectionOrNot:
            self.keep_alive = KeepAlive(100, 3)

        # Handle problems like web-page not found
        self.setWrongFile()

        # Compare the date to decide whether sent the object
        if request.condition_date is not None and not self.last_modified_time.compare(request.condition_date):
            self.status_code = self.StatusCode.NOT_MODIFIED

    # handle the response to prepare the returnable message
    def returnableResponse(self):
        response = "{} {}\r\n".format(self.version, self.status_code.value)
        response += "Date: {}\r\n".format(self.date.now_time)
        response += "Server: LZD's Web Server\r\n"
        # To save space, if the status code is not '200 OK', other information is omitted
        if self.status_code != self.StatusCode.OK:
            response += "\r\n{}\r\n".format(self.entity_body)
            return response
        # Remaining information
        response += "Last-Modified: {}\r\n".format(self.last_modified_time.time)
        response += "Content-Type: {}\r\n".format(self.content_type)
        response += "Content-Length: {}\r\n".format(str(self.content_length))
        if self.connectionOrNot:
            response += "Keep-Alive: timeout = {}, max = {}\r\n".format(self.keep_alive.timeout, self.keep_alive.max)
            response += "Connection: Keep-Alive\r\n\r\n"
        else:
            response += "Connection: Close\r\n\r\n"

        if self.entity_body is not None and self.content_type.startswith("text"):
            response += "{}\r\n".format(self.entity_body)
        return response

    def setRecord(self):
        """
        Set the record of a client request
        """
        record = [handleNone(self.request.client_host_name), handleNone(self.request.access_time.time),
                  handleNone(self.request.URL), handleNone(self.status_code.value)]
        return record
