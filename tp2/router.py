# --------------------------------------------------------------------------- #
# ---------------------- Engenharia de Sistemas - UFMG ---------------------- #
# ----------------------- DCC023 - Redes de Computadores -------------------- #
# --------------------- Prof. Ítalo Fernando Scota Cunha -------------------- #
# ------------------------ Trabalho Prático II - DCCRIP --------------------- #
# ----------- Alunos :   Humberto Monteiro Fialho   (2013430811) ------------ #
# --------------------   Rafael Carneiro de Castro  (2013030210) ------------ #
# --------------------------------------------------------------------------- #

# TODO DÚVIDAS:
# algum jeito de ler qualquer tamanho no recv do UDP? qual seria o maximo?
# se passa parametro com flag, todos tem flag também?
# ctrl+c com stack trace pode atrapalhar?
# period é segundos mesmo?

import sys
import json
import threading
import socket as sck

MAX_PAYLOAD_SIZE = 65536


class Router:
    neighbors = []
    routing = []
    history = []

    def __init__(self, ip, period):
        self.ip = ip
        self.port = 55151
        self.period = period
        this_routing = dict()
        this_routing['ip'] = ip
        this_routing['distance'] = 0
        this_routing['next'] = ip
        self.routing.append(this_routing)

    def add_neighbor(self, neighbor_ip, neighbor_weight):
        new_neighbor = dict()
        new_neighbor['ip'] = neighbor_ip
        new_neighbor['weight'] = neighbor_weight
        self.neighbors.append(new_neighbor)

    def remove_neighbor(self, neighbor_ip):
        # usar o histórico para definir nova rota
        # TODO
        pass

    def send_table(self):
        # split horizon
        # TODO
        pass

    def receive_table_info(self):
        # manter um histórico com as rotas não otimizadas para fazer troca instantânea
        # quando um enlace for desativado
        # subtrair TTL dos dados do source
        # TODO
        pass


router = None


def star_router(address, update_period, startup_commands):
    global router
    router = Router(address, update_period)

    socket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
    socket.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
    socket.bind((router.ip, router.port))

    if startup_commands:
        read_command_file(startup_commands)

    read_thread = threading.Thread(target=read_commands, args=())
    read_thread.start()
    read_thread = threading.Thread(target=receive_tables, args=(socket,))
    read_thread.start()
    # TODO send from period
    # # TODO remove tests
    # print_thread = threading.Thread(target=read_command_file, args=('teste',))
    # print_thread.start()


def read_command_file(file_name):
    with open(file_name, 'r') as file:
        line = file.readline()
        while line:
            if line is not '\n':
                read_command(line)
            line = file.readline()


def read_commands():
    while True:
        read = input()
        read_command(read)


def read_command(read_line):
    read_line = read_line.split()

    if read_line[0] == 'add':
        router.add_neighbor(read_line[1], read_line[2])
    elif read_line[0] == 'del':
        # TODO
        pass
    elif read_line[0] == 'trace':
        # TODO
        pass


def receive_tables(connection):
    while True:
        data = json.loads(connection.recv(MAX_PAYLOAD_SIZE))
        # TODO remove debug print
        # TODO async log in file
        print('Data>', data)


# main: calling functions to receive inputs
def main():
    address = None
    update_period = None
    startup_commands = None

    if len(sys.argv) < 5:
        address = sys.argv[1]
        update_period = sys.argv[2]
        if len(sys.argv) > 3:
            startup_commands = sys.argv[3]
    else:
        if '--addr' in sys.argv:
            address = sys.argv[sys.argv.index('--addr') + 1]
        if '--update-period' in sys.argv:
            update_period = sys.argv[sys.argv.index('--update-period') + 1]
        if '--startup-commands' in sys.argv:
            startup_commands = sys.argv[sys.argv.index('--startup-commands') + 1]

    star_router(address, update_period, startup_commands)

    return


# --------------------------------------------------------------------------- #
# calling main function
if __name__ == '__main__':
    main()
