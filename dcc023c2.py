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
import struct
import binascii
import socket as sck

MAX_LENGTH = 65535
SYNC = b'dcc023c2'
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

    receive_data(connection, output_file_name)
    send_data(connection, input_file_name)

    return


# start the code as client
def initialize_client():
    # reading inputs
    ip = sys.argv[2].split(':')[0]
    port = int(sys.argv[2].split(':')[1])
    input_file_name = sys.argv[3]
    output_file_name = sys.argv[4]

    connection = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    connection.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
    connection.connect((ip, port))

    receive_data(connection, output_file_name)
    send_data(connection, input_file_name)

    connection.close()
    print('Done')


# encrypt
def encode16(data):
    return binascii.hexlify(data)


# decrypt
def decode16(data):
    return binascii.unhexlify(data).decode()


# function to send data from file
def send_data(connection, file_name):
    with open(file_name) as file:
        file_line = file.readline(MAX_LENGTH)

        # TODO remover
        # data += get_length(file_line) + get_id()
        # print(data)
        print(file_line)

        # TODO para mandar:
        # length: struct.pack('!H', length)
        # data: struct.pack('!3s', 'asd'.encode())
        # both: result = struct.pack('!H3s', length, 'asd'.encode())
        # send: sck.send(encode16(result))
        # length = len(file_line)
        # fmt = '!16sH{length}s'.format(length=length)
        # data = struct.pack(fmt, 2*SYNC, length, file_line.encode())
        # TODO descobrir se é jeito certo de mandar SYNC
        sentinel = struct.pack('!LL', int(SYNC, base=16), int(SYNC, base=16))
        connection.send(sentinel)

        # TODO codificar antes de mandar
        length = len(file_line)
        fmt = '!H{length}s'.format(length=length)
        data = struct.pack(fmt, length, file_line.encode())
        connection.send(data)

        print('Send data from file', file_name)

        # print('Mandando2')
        # resp = connection.send('efgh'.encode())
        # print('RESPOSTA2:')
        # print(resp)


def receive_data(connection, file_name):
    print('Esperando dados:')
    data1 = connection.recv(2)
    test_length = struct.unpack('!H', data1)[0]
    print(test_length)
    # ler o htons: struct.unpack('!H', data1)[0]

    print('Esperando dados2:')
    data2 = connection.recv(test_length)
    print(data2.decode())

    print('Received data saved on file', file_name)
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
    # pass


# main
def main():
    if sys.argv[1] == '-s':
        initialize_server()
    elif sys.argv[1] == '-c':
        initialize_client()

    return


# --------------------------------------------------------------------------- #
# calling main function
if __name__ == '__main__':
    main()
