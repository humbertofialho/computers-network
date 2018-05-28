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
# se TTL igual a zero, tem que pegar do histórico também? ou seja, recuperação também é em TTL igual a zero? ou só DEL?

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
        # the next vector contains IPs with TTLs
        this_routing['next'] = {ip: 4}
        self.routing.append(this_routing)

    def add_neighbor(self, neighbor_ip, neighbor_weight):
        new_neighbor = dict()
        new_neighbor['ip'] = neighbor_ip
        new_neighbor['weight'] = int(neighbor_weight)
        self.neighbors.append(new_neighbor)

    def remove_neighbor(self, neighbor_ip):
        # usar o histórico para definir nova rota
        # TODO
        pass

    def send_table(self):
        # split horizon
        # TODO
        pass

    def update_history(self, ip, next_hop, distance, ttl):
        on_history = list(filter(lambda route: route['ip'] == ip and route['distance'] == distance, self.history))
        if len(on_history) > 0:
            # there is a history with that host and distance, just add or update next
            on_history[0]['next'][next_hop] = ttl
        else:
            # add new history
            new_history = dict()
            new_history['ip'] = ip
            new_history['next'] = {next_hop: ttl}
            new_history['distance'] = distance
            self.history.append(new_history)

    def receive_table_info(self, table_info):
        source = list(filter(lambda neighbor: neighbor['ip'] == table_info['source'], self.neighbors))[0]
        # TODO subtract tll FROM ROUTING AND HISTORY and remove tll equals to 0

        for ip in table_info['distances'].keys():
            on_routing = list(filter(lambda route: route['ip'] == ip, self.routing))
            if len(on_routing) > 0:
                # there is already a route to this IP
                if on_routing[0]['distance'] > table_info['distances'][ip] + source['weight']:
                    # if the new distance is better, then update the routing table with TTL 4
                    for next_hop in on_routing[0]['next'].keys():
                        # add to history old entry
                        self.update_history(ip, next_hop, on_routing[0]['distance'], on_routing[0]['next'][next_hop])
                    on_routing[0]['next'] = {source['ip']: 4}
                    on_routing[0]['distance'] = table_info['distances'][ip] + source['weight']
                elif on_routing[0]['distance'] == table_info['distances'][ip] + source['weight']:
                    # if the new distance is equals, then add or update the option with TTL 4
                    on_routing[0]['next'][source['ip']] = 4
                else:
                    # the new distance is worse
                    # TODO weight changed, remove from history and update current routing
                    # TODO if there are other routes (load balancing), keep them, just remove
                    # TODO else, just update history
                    # manter um histórico com as rotas não otimizadas para fazer troca instantânea
                    # quando um enlace for desativado
                    pass
            else:
                # there isn't a route to this IP, just add with TTL 4 by the source
                new_route = dict()
                new_route['ip'] = ip
                new_route['distance'] = table_info['distances'][ip] + source['weight']
                new_route['next'] = {source['ip']: 4}
                self.routing.append(new_route)


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
    read_thread = threading.Thread(target=receive_data, args=(socket,))
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
    global router

    read_line = read_line.split()
    if read_line[0] == 'add':
        router.add_neighbor(read_line[1], read_line[2])
    elif read_line[0] == 'del':
        # TODO update routing from history
        pass
    elif read_line[0] == 'trace':
        # TODO
        pass


def receive_data(connection):
    global router

    while True:
        data = json.loads(connection.recv(MAX_PAYLOAD_SIZE))

        if data['type'] == 'update':
            router.receive_table_info(data)
            # TODO remove debug print
            print('Routing>', router.routing)
            print('History>', router.history)
        elif data['type'] == 'trace':
            # TODO
            pass
        elif data['type'] == 'data':
            # TODO
            pass
        # TODO remove debug print
        # TODO async log in file with received data


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
