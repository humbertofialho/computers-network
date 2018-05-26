import json
import socket as sck

IP = '127.0.1.1'
PORT = 55151
socket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)

obj = {
    'type': 'update',
    'source': '127.0.1.5',
    'destination': '127.0.1.1',
    'distances': {
        '127.0.1.2': 10,
        '127.0.1.3': 10,
        '127.0.1.4': 10,
        '127.0.1.5': 0
    }
}
socket.sendto(json.dumps(obj).encode(), (IP, PORT))
obj['distances']['127.0.1.7'] = 7
socket.sendto(json.dumps(obj).encode(), (IP, PORT))

# socket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
# socket.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
# socket.bind((IP, PORT))
#
# recv = socket.recv(1024)
# print(recv)
# recv = socket.recv(1024)
# obj = json.loads(recv)
# print(obj)
# print(obj['a'])
# print(obj['b'])
