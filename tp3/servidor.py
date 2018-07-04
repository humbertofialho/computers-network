# --------------------------------------------------------------------------- #
# ---------------------- Engenharia de Sistemas - UFMG ---------------------- #
# ----------------------- DCC023 - Redes de Computadores -------------------- #
# --------------------- Prof. Ítalo Fernando Scota Cunha -------------------- #
# ---------------- Trabalho Prático III - Servidor de Mensagens ------------- #
# ----------- Alunos :   Humberto Monteiro Fialho   (2013430811) ------------ #
# --------------------   Rafael Carneiro de Castro  (2013030210) ------------ #
# --------------------------------------------------------------------------- #

import re
import sys
import socket as sck


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.tag_map = dict()

    def add_to_tag(self, tag, address):
        # add new listeners for tag in the map
        if tag in self.tag_map:
            self.tag_map[tag].add(address)
        else:
            self.tag_map[tag] = {address}

    def remove_from_tag(self, tag, address):
        # remove listener from tag
        if tag in self.tag_map and address in self.tag_map[tag]:
            self.tag_map[tag].remove(address)

    def send_message(self, message, socket):
        # find all tags in the message
        tags = list(set(re.findall('(?:#)(\w+)', message)))

        # set to avoid double dispatch
        to_send = set()
        for tag in tags:
            if tag in self.tag_map:
                registered = self.tag_map[tag]
                to_send = to_send.union(registered)

        for address in to_send:
            # send the message for each registered listener
            socket.sendto(message.encode(), address)


server = None


def start_server(ip, port):
    global server
    server = Server(ip, port)

    socket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
    socket.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
    socket.bind((server.ip, server.port))

    while True:
        message, address = socket.recvfrom(500)
        message = message.decode()

        # check if it is a message do add or remove tag
        to_add = list(set(re.findall('(?:\+)(\w+)', message)))
        to_remove = list(set(re.findall('(?:-)(\w+)', message)))
        if len(to_add) > 0:
            for tag in to_add:
                server.add_to_tag(tag, address)
            socket.sendto('Tag adicionada com sucesso.'.encode(), address)
        elif len(to_remove) > 0:
            for tag in to_remove:
                server.remove_from_tag(tag, address)
            socket.sendto('Tag removida com sucesso.'.encode(), address)
        else:
            server.send_message(message, socket)


# main: calling functions to receive inputs
def main():
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        start_server('127.0.0.1', port)

    return


# --------------------------------------------------------------------------- #
# calling main function
if __name__ == '__main__':
    main()
