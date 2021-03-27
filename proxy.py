import socket, multiprocessing, time, json, webob
import request

class proxy:
    def __init__(self, configFile, IP="0.0.0.0", port=3993, domain="0.0.0.0"):

        with open(configFile, "r") as f:
            self.config = json.load(f)

        self.outSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.outSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.d = "localhost"

        self.IP = IP        
        self.port = port 
        self.domain = domain   
        print(f"External port opened at {self.domain}:{port}")

    def alotServer(self, pre):
        return (self.config[pre]["host"], int(self.config[pre]["port"]))

    def receive(self, sock, chunk):
        recv = sock.recv(chunk)#.replace(f"{self.domain}:{self.port}".encode(), "self.d:80".encode())
        req = request.request(recv.decode())
        print(recv)
        print(req.compile())
        return req

    def proxyWorker(self, inf=None):
        sock, addr = inf
        inData = self.receive(sock, 2 ** 20)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as inSock:
            inSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server = self.alotServer("*")
            print("****************")
            print(inData.compile())
            print("*************1111")
            inData.headers["Host"] = "www.sushantshah.ml"
            inSock.connect(server)
            inSock.send(inData.compile())
            rv = self.receive(inSock, 2**20)
            print(f"Incoming at sock: {sock} addr: {addr}")
            sock.send(rv.compile())
        print("################")
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
