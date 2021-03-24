import socket 
import multiprocessing 
import time  

sock = socket.socket()
sock.connect
sock.bind(("0.0.0.0", 4000))
sock.listen(5)
while True:
    sck, addr = sock.accept()
    rv = sck.recv(2 ** 20)
    if(rv != ""): sck.send(rv)