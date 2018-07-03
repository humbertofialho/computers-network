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
        tags = list(set(re.findall('(?:#)(\w+)', message)))

        # TODO remover
        print('RECEIVED MESSAGE>', message)
        print(tags)
        print('Address:', address)
        socket.sendto('Teste do servidor para o cliente'.encode(), address)


# main: calling functions to receive inputs
def main():
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

        # TODO remover
        print(port)
        start_server('127.0.0.1', port)

    return


# --------------------------------------------------------------------------- #
# calling main function
if __name__ == '__main__':
    main()
