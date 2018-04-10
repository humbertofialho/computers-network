# --------------------------------------------------------------------------- #
# ---------------------- Engenharia de Sistemas - UFMG ---------------------- #
# ----------------------- DCC023 - Redes de Computadores -------------------- # 
# --------------------- Prof. Ítalo Fernando Scota Cunha -------------------- #
# ------------------------ Trabalho Prático I - DCCNET ---------------------- #
# ----------- Alunos :   Humberto Monteiro Fialho   (2013430811) ------------ #
# -----------            Rafael Carneiro de Castro  (2013030210) ------------ #
# --------------------------------------------------------------------------- #

# libraries
import sys
import ctypes
import binascii
import socket as sck

SYNC = 'dcc023c3'
CONFIRMATION = {
    'id': 0,
    'confirmed': False
}


# start the code as server
def initialize_server():
    # reading inputs
    ip = '127.0.0.1'
    port = int(sys.argv[2])
    input_file_name = sys.argv[3]
    output_file_name = sys.argv[4]

    # starting socket with standard protocol
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(1)

    print('Server running on port', port)
    connection = s.accept()[0]

    print('Esperando dados:')
    data1 = connection.recv(2)
    print(data1)
    print(type(data1))

    print('Esperando dados2:')
    data2 = connection.recv(4)
    print(data2)

    return


# start the code as client
def initialize_client():
    # reading inputs
    ip = sys.argv[2].split(':')[0]
    port = int(sys.argv[2].split(':')[1])
    input_file_name = sys.argv[3]
    output_file_name = sys.argv[4]

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
    s.connect((ip, port))

    send_data(s, input_file_name)

    s.close()
    print('Done')


# encrypt
def encode16(data):
    return binascii.hexlify(data.encode())


# decrypt
def decode16(data):
    return binascii.unhexlify(data).decode()


# function to send data from file
def send_data(connection, file_name):
    with open(file_name) as file:
        data = SYNC + SYNC
        # TODO checar tamanho do dado passando por parametro no readline
        file_line = file.readline()

        data += get_length(file_line) + get_id()
        print(data)

        # connection.sendto(sck.htons(ctypes.c_uint16(3).value), 1)
        connection.send(SYNC.encode())
        connection.send(SYNC.encode())

        print('Send data from file', file_name)
        # TODO codificar antes de mandar


        # print('Mandando2')
        # resp = connection.send('efgh'.encode())
        # print('RESPOSTA2:')
        # print(resp)


def number_to_limited_hex(number, length):
    data = hex(number)[2:]
    while len(data) < length:
        data = '0' + data

    return data


def get_length(data):
    return number_to_limited_hex(len(data), 4)


def get_id():
    return number_to_limited_hex(CONFIRMATION['id'], 2)


def receive():
    # while True:
    #     data = recv()
    #     if data != SYNC:
    #         print('SYNC ERROR')
    #         break
    #
    #     data = recv()
    #     if data != SYNC:
    #         print('SYNC ERROR')
    #         break
    #
    #     tamanho = recv()
    #     checksum = recv()
    #     id = recv()
    #     flag = recv()
    #     body = recv()
    #
    #     if error_detection(checksum, ...):
    #         print('CHECKSUM ERROR')
    #         break
    #
    #     print_file('file', body)
    #
    # receive()
    pass


# main
def main():
    if sys.argv[1] == '-s':
        initialize_server()
    elif sys.argv[1] == '-c':
        initialize_client()

    return


# --------------------------------------------------------------------------- #
if __name__ == '__main__': # calling main function
    main()
