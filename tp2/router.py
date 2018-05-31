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
# reenviar para vizinhos assim que mudar algo?

import sys
import json
import copy
import threading
import socket as sck
from random import randint

MAX_PAYLOAD_SIZE = 65536
MAX_HISTORY_VERSION = 10000


# method to call function every 'secs' seconds
def set_interval(func, secs):
    def function_wrapper():
        func()
        set_interval(func, secs)
    t = threading.Timer(secs, function_wrapper)
    t.start()
    return t


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
        self.history_version = 0
        self.routing_version = 0
        self.routing = dict()
        self.update_routing_table()

    def add_neighbor(self, neighbor_ip, neighbor_weight):
        new_neighbor = dict()
        new_neighbor['ip'] = neighbor_ip
        new_neighbor['weight'] = int(neighbor_weight)
        self.neighbors.append(new_neighbor)
        new_route = dict()
        new_route['ip'] = new_neighbor['ip']
        new_route['distance'] = new_neighbor['weight']
        new_route['next'] = new_neighbor['ip']
        new_route['ttl'] = 4
        self.history.append(new_route)
        self.history_version = self.history_version + 1

    def remove_neighbor(self, neighbor_ip):
        # usar o histórico para definir nova rota
        # TODO remove routes learned from neighbor_ip
        pass

    def send_update(self):
        routing_table = self.get_routing_table()

        update_message = dict()
        update_message['type'] = 'update'
        update_message['source'] = self.ip
        update_message['destination'] = ''
        update_message['distances'] = dict()

        for ip in routing_table.keys():
            update_message['distances'][ip] = routing_table[ip][0]['distance']

        connection = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
        for neighbor in self.neighbors:
            # copy message to use original in other neighbor messages
            copy_message = copy.deepcopy(update_message)
            copy_message['destination'] = neighbor['ip']

            # by split horizon, remove route to destination of message
            if neighbor['ip'] in copy_message['distances'].keys():
                del copy_message['distances'][neighbor['ip']]

            # by split horizon, remove route learned from destination of message
            to_remove = []
            for ip in routing_table.keys():
                learned_from_destination = list(filter(lambda option: option['next'] == neighbor['ip'],
                                                       routing_table[ip]))
                if len(learned_from_destination) > 0 and ip in copy_message['distances'].keys():
                    to_remove.append(ip)
            for ip in to_remove:
                copy_message['distances'].pop(ip)

            # all routers have the same port
            connection.sendto(json.dumps(copy_message).encode(), (neighbor['ip'], self.port))

    def get_routing_table(self):
        # updating routing on-demand
        if self.routing_version < self.history_version:
            # update old routing table
            self.update_routing_table()
        return self.routing

    def update_routing_table(self):
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

        self.routing_version = self.history_version
        self.routing = routes_by_ip

    def subtract_ttl(self, source_ip):
        # subtract TTL from routes learned from source
        for route in self.history:
            if route['next'] == source_ip:
                route['ttl'] = route['ttl'] - 1
                if route['ttl'] == 0:
                    # remove routes with TTL equals to 0
                    self.history.remove(route)

    def receive_table_info(self, table_info):
        # find neighbor who sent that information
        source = list(filter(lambda neighbor: neighbor['ip'] == table_info['source'], self.neighbors))
        if len(source) == 0 or table_info['destination'] != self.ip:
            # leave if it's from unknown source or another destination
            return
        source = source[0]

        self.subtract_ttl(source['ip'])

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

        # adding history version to update routing on-demand
        self.history_version = self.history_version + 1
        if self.history_version > MAX_HISTORY_VERSION:
            self.history_version = 0
            self.update_routing_table()

    def send_trace(self, final_ip):
        trace_message = dict()
        trace_message['type'] = 'trace'
        trace_message['source'] = self.ip
        trace_message['destination'] = final_ip
        trace_message['hops'] = [self.ip]

        # send message with load balance
        self.send_message(trace_message)

    def send_data(self):
        # TODO
        pass

    def send_message(self, message):
        routing_table = self.get_routing_table()

        if message['destination'] in routing_table.keys():
            # select one of the best options for load balancing
            options = routing_table[message['destination']]
            selected_option = randint(0, len(options) - 1)
            selected_hop = options[selected_option]['next']

            connection = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
            # all routers have the same port
            connection.sendto(json.dumps(message).encode(), (selected_hop, self.port))


router = None


def star_router(address, update_period, startup_commands):
    global router
    router = Router(address, update_period)

    socket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
    socket.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
    socket.bind((router.ip, router.port))

    # read commands from file
    if startup_commands:
        read_command_file(startup_commands)

    # read commands from terminal
    read_thread = threading.Thread(target=read_commands, args=())
    read_thread.start()

    # receive data from routers
    read_thread = threading.Thread(target=receive_data, args=(socket,))
    read_thread.start()

    # send update message to neighbors
    set_interval(router.send_update, router.period)


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
        router.send_trace(read_line[1])


def receive_data(connection):
    global router

    while True:
        data = json.loads(connection.recv(MAX_PAYLOAD_SIZE))

        if data['type'] == 'update':
            router.receive_table_info(data)

            # TODO remove debug print
            r = router.get_routing_table()
            print('Routing>', r)
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

    star_router(address, int(update_period), startup_commands)

    return


# --------------------------------------------------------------------------- #
# calling main function
if __name__ == '__main__':
    main()
