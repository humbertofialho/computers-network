# --------------------------------------------------------------------------- #
# ---------------------- Engenharia de Sistemas - UFMG ---------------------- #
# ----------------------- DCC023 - Redes de Computadores -------------------- #
# --------------------- Prof. Ítalo Fernando Scota Cunha -------------------- #
# ---------------- Trabalho Prático III - Servidor de Mensagens ------------- #
# ----------- Alunos :   Humberto Monteiro Fialho   (2013430811) ------------ #
# --------------------   Rafael Carneiro de Castro  (2013030210) ------------ #
# --------------------------------------------------------------------------- #

import sys
import socket as sck


# main: calling functions to receive inputs
def main():
    if len(sys.argv) > 3:
        local_port = int(sys.argv[1])
        server_ip = sys.argv[2]
        server_port = int(sys.argv[3])

        # TODO remover
        print(local_port, server_port, server_ip)
        socket = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
        socket.bind(('127.0.0.1', local_port))
        socket.sendto('Mensgem do cliente'.encode(), (server_ip, server_port))

    return


# --------------------------------------------------------------------------- #
# calling main function
if __name__ == '__main__':
    main()
