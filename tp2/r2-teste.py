import json
import socket as sck

socket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
socket.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
socket.bind(('127.0.1.3', 55151))

data = json.loads(socket.recv(65536))
print('Received>', data)
