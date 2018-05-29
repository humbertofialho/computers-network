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
# se TTL igual a zero, tem que pegar do histórico também? ou seja, recuperação também é em TTL igual a zero? ou só DEL?
# reenviar assim que atualizar?

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
        this_routing['ttl'] = 4
        self.history.append(this_routing)

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

    def get_routing_table(self):
        # get the best options of routes for each IP
        # each one can have more than one route with the same distance (load balancing)
        routes_by_ip = dict()
        for history in self.history:
            ip_key = history['ip']
            if ip_key not in routes_by_ip.keys() or routes_by_ip[ip_key][0]['distance'] > history['distance']:
                # if there isn't a route for that IP on the routing table,
                # or the new history has a better distance, update de routing entry
                routes_by_ip[ip_key] = [history]
            elif routes_by_ip[ip_key][0]['distance'] == history['distance']:
                # if already exists a route for that IP with that distance, add new option
                routes_by_ip[ip_key].append(history)

        return routes_by_ip

    def receive_table_info(self, table_info):
        source = list(filter(lambda neighbor: neighbor['ip'] == table_info['source'], self.neighbors))
        if len(source) == 0 or table_info['destination'] != self.ip:
            # leave if it's from unknown source or another destination
            return
        source = source[0]

        # TODO subtract tll FROM ROUTING AND HISTORY and remove tll equals to 0

        for ip in table_info['distances'].keys():
            # update the history with the route for that IP by that source
            on_history = list(filter(lambda route: route['ip'] == ip and route['next'] == table_info['source'],
                                     self.history))
            # there should only exists one history for that IP by that source
            if len(on_history) > 0:
                # there is a history for that IP by that source, just update distance and TTL
                on_history[0]['distance'] = table_info['distances'][ip] + source['weight']
                on_history[0]['ttl'] = 4
            else:
                # there isn't a history for that IP by that source, add new
                new_history = dict()
                new_history['ip'] = ip
                new_history['distance'] = table_info['distances'][ip] + source['weight']
                new_history['next'] = table_info['source']
                new_history['ttl'] = 4
                self.history.append(new_history)


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
            print('Routing>', router.get_routing_table())
            print('History>', router.history)
            print('\n\n')
        elif data['type'] == 'trace':
            # TODO
            pass
        elif data['type'] == 'data':
            # TODO
            # TODO ponto extra: avisar origem se não tem rota
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
