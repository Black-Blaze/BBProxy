import socket, multiprocessing, time, json, webob

class proxy:
    def __init__(self, configFile, IP="0.0.0.0", port=3993):

        with open(configFile, "r") as f:
            self.config = json.load(f)

        self.outSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.outSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


        self.IP = IP        
        self.port = port    
        print(f"External port opened at {IP}:{port}")

    def alotServer(self):
        pass

    def receive(self, sock, chunk):
        return sock.recv(chunk).replace(f"{self.IP}:{self.port}".encode(), "sushantshah.ml:80".encode())

    def proxyWorker(self, inf=None):
        sock, addr = inf
        inData = self.receive(sock, 2 ** 20)
        print(inData)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as inSock:
            inSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server = ("sushantshah.ml", 80)#self.alotServer()
            inSock.connect(server)
            inSock.send(inData)
            sock.send(self.receive(inSock, 2**20).replace("sushantshah.ml:80".encode(), f"{self.IP}:{self.port}".encode()))
        print(f"Incoming at sock: {sock} addr: {addr}")

    def run(self):
        outSock = self.outSock
        outSock.bind((self.IP, self.port))
        outSock.listen(5)   
        p = []
        while True:  
            inf = self.outSock.accept()
            if not inf == None:
                ps = multiprocessing.Process(target=self.proxyWorker, args=(inf,))
                ps.start()
                ps.join()
            inf = None
