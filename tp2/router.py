# --------------------------------------------------------------------------- #
# ---------------------- Engenharia de Sistemas - UFMG ---------------------- #
# ----------------------- DCC023 - Redes de Computadores -------------------- #
# --------------------- Prof. Ítalo Fernando Scota Cunha -------------------- #
# ------------------------ Trabalho Prático II - DCCRIP --------------------- #
# ----------- Alunos :   Humberto Monteiro Fialho   (2013430811) ------------ #
# --------------------   Rafael Carneiro de Castro  (2013030210) ------------ #
# --------------------------------------------------------------------------- #

# manter um histórico com as rotas não otimizadas para fazer troca instantânea
# quando um enlace for desativado

# DÚVIDAS:
# algum jeito de ler qualquer tamanho no recv do UDP? qual seria o maximo?
# se passa parametro com flag, todos tem flag também?

import sys
import json
# TODO remove import
import time
import threading
import socket as sck

IP = '127.0.1.1'
PORT = 55151

test_data = dict()
test_data['a'] = 1
test_data['b'] = 'string'
string = json.dumps(test_data)

socket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
socket.sendto('teste'.encode(), (IP, PORT))
socket.sendto(string.encode(), (IP, PORT))


def star_router(address, update_period, startup_commands):
    # TODO remove debug print
    print(address, update_period, startup_commands)

    # TODO remove tests
    read_thread = threading.Thread(target=read_commands, args=())
    read_thread.start()
    print_thread = threading.Thread(target=read_command_file, args=())
    print_thread.start()


def read_command_file():
    # TODO remove tests
    for index in range(5):
        print('File processed', index)
        time.sleep(1)


def read_commands():
    # TODO remove tests
    read = input()
    print('Read data>', read)


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
