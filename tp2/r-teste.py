import sys
import json
import socket as sck

IP = '127.0.1.4' if len(sys.argv) < 2 else sys.argv[1]
print('Listening', IP)
socket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
socket.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
socket.bind((IP, 55151))

d = socket.recv(65536)
data = json.loads(d)
print('String>', d)
print('JSON>', data)
