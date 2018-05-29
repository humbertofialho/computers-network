import json
import socket as sck

IP = '127.0.1.1'
PORT = 55151
socket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)

obj1 = {
    'type': 'update',
    'source': '127.0.1.5',
    'destination': '127.0.1.1',
    'distances': {
        '127.0.1.2': 10,
        '127.0.1.3': 10,
        '127.0.1.5': 0,
        '127.0.1.7': 5
    }
}
socket.sendto(json.dumps(obj1).encode(), (IP, PORT))
obj2 = {
    'type': 'update',
    'source': '127.0.1.4',
    'destination': '127.0.1.1',
    'distances': {
        '127.0.1.2': 10,
        '127.0.1.3': 5,
        '127.0.1.4': 0,
        '127.0.1.5': 0,
        '127.0.1.6': 15
    }
}
socket.sendto(json.dumps(obj2).encode(), (IP, PORT))
obj3 = {
    'type': 'update',
    'source': '127.0.1.6',
    'destination': '127.0.1.1',
    'distances': {
        '127.0.1.3': 13,
        '127.0.1.6': 0,
        '127.0.1.7': 2
    }
}
socket.sendto(json.dumps(obj3).encode(), (IP, PORT))
obj4 = {
    'type': 'update',
    'source': '127.0.1.5',
    'destination': '127.0.1.1',
    'distances': {
        '127.0.1.2': 10,
        '127.0.1.3': 10,
        '127.0.1.5': 0,
        '127.0.1.7': 10
    }
}
socket.sendto(json.dumps(obj4).encode(), (IP, PORT))
obj5 = {
    'type': 'update',
    'source': '127.0.1.4',
    'destination': '127.0.1.1',
    'distances': {
        '127.0.1.3': 10,
        '127.0.1.5': 0,
        '127.0.1.4': 0,
        '127.0.1.6': 15,
        '127.0.1.8': 5
    }
}
socket.sendto(json.dumps(obj5).encode(), (IP, PORT))
socket.sendto(json.dumps(obj5).encode(), (IP, PORT))
socket.sendto(json.dumps(obj5).encode(), (IP, PORT))
socket.sendto(json.dumps(obj5).encode(), (IP, PORT))
