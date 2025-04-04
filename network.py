import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server ="192.168.0.105"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect() # id to indentify players

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode() # send validation that connection is successfull ("Connected")
        except:
            pass