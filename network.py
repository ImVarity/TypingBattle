import socket
import pickle
import details


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = details.IP
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
    
    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048 * 6))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048 * 6))
        except socket.error as e:
            print(e)