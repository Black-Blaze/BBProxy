import socket, multiprocessing, time, json, webob
import request

class proxy:
    def __init__(self, configFile, domain="0.0.0.0"):

        with open(configFile, "r") as f:
            self.config = json.load(f)

        self.outSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.outSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.d = "localhost"

        self.IP = self.config["config"]["addr"]
        self.port = int(self.config["config"]["port"])
        self.domain = domain   
        print(f"External port opened at {self.domain}:{self.port}")

    def alotServer(self, pre):
        return (self.config["hosts"][pre]["host"], int(self.config["hosts"][pre]["port"]))

    def receive(self, sock, chunk, hasContent=True):
        for trial in range(5):
            recv = sock.recv(chunk)
            req = request.request(recv)
            if len(req.body) > 1 or not hasContent:
                return req

    def proxyWorker(self, inf=None):
        sock, addr = inf
        inData = self.receive(sock, 2 ** 20, False)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as inSock:
            inSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server = self.alotServer("0.0.0.0:2000")#inData.headers["Host"])
            #inData.headers["Host"] = "www.sushantshah.ml"
            inSock.connect(server)
            inSock.send(inData.compile())
            rv = self.receive(inSock, self.config["config"]["maxRecieve"])
            print(rv.body)
            if(inData.proto != b"GET /favicon.ico HTTP/1.1"):
                with open("access-logs.txt", "a") as f:
                    f.writelines(f"\nRequest\n{str(inData.compile().decode())}")
                    try:
                        f.writelines(f"\n\nResponse\n{str(rv.compile().decode())}\n")
                    except:
                        f.writelines(f"Response\nNOT PLAIN TEXT")
                    f.writelines("\n***********************************************************************")
            #rv.headers["Host"] = "0.0.0.0:2000"
            print(f"Incoming at sock: {sock} addr: {addr}")
            sock.send(rv.compile())
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
