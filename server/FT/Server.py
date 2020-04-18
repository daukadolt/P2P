import socket


class Server:
    def __init__(self, host='127.0.0.1', port=None):
        if port is None:
            port = 0
        self.host = host
        self.port = port
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.port = self.socket.getsockname()[1]

    def start(self):
        pass
