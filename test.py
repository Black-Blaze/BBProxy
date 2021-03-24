import socket 
import multiprocessing 
import time  

sock = socket.socket()
sock.connect(("0.0.0.0", 3993))
while True:
    sock.send(input().encode())