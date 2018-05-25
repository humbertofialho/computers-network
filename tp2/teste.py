import json
import socket as sck

IP = '127.0.1.1'
PORT = 55151

socket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
socket.bind((IP, PORT))

recv = socket.recv(1024)
print(recv)
recv = socket.recv(1024)
obj = json.loads(recv)
print(obj)
print(obj['a'])
print(obj['b'])
