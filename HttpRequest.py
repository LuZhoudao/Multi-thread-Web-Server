import MyTime


# The HTTP request class
class Request:
    def __init__(self, request, client_connection, client_address):
        self.client_connection = client_connection
        self.client_host_name = client_address[0]
        self.method = None
        self.condition_date = None
        self.URL = None
        self.version = None
        self.connectionOrNot = False
        self.split_request(request)
        self.access_time = MyTime.AccessTime()
        self.end_time = None

    def setEndTime(self, end_time):
        """
        To set end time of a request. This helps to handle timeout
        :param end_time:
        """
        self.end_time = end_time

    def __eq__(self, other):
        """
        Override __eq__ method to compare if two requests are the same
        :param other:
        :return: bool
        """
        if id(self) == id(other):
            return True
        else:
            return False

    def setSpecificStatusCode(self, file):
        self.URL = file

    def split_request(self, request):
        """
        Handle the HTTP request.
        :param request:
        """
        # Parse HTTP headers
        headers = request.split('\n')

        # Handle  'If-Modified-Since' and 'Connection'
        for i in range(1, len(headers)):
            line = headers[i]
            if line.lower().startswith("if-modified-since: "):
                conditionDate = MyTime.Time(line[19:45])
                self.condition_date = conditionDate
            elif line.lower().startswith("connection: "):
                if line[12:len(line)-1].lower() == "keep-alive":
                    self.connectionOrNot = True

        # Handle first line
        fields = headers[0].split()

        # For out of range
        if len(fields) == 3:
            request_type = fields[0]
            # Record the method
            self.method = request_type
            # Record the requested file name
            filename = fields[1]
            if filename == '/':
                filename = '/index.html'
            # if filename == '/favicon.ico':
            #     filename = ''
            self.URL = filename[1:len(filename)]
            # Record the HTTP version
            version = fields[2]
            if version[-2:] == '\r':
                self.version = version[:-2]
            self.version = version
            if self.version == "HTTP/1.1":
                self.connectionOrNot = True
        elif len(fields) > 0:
            # This is to send 'Bad request' for some wrong input, otherwise the client will receive nothing
            self.method = fields[0]

