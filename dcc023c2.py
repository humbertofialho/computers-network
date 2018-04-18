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
import signal
import binascii
import datetime
import socket as sck

MAX_LENGTH = 65535
SYNC = 'dcc023c2'


class DataTransfer:
    def __init__(self, data='', id=1, flags=0):
        self.data = data
        self.confirmed = False
        self.id = id
        self.flags = flags

    def prepare_for_new_data(self):
        self.confirmed = False
        self.id = 1 if self.id == 0 else 0

    @staticmethod
    def _format_numbers(number, is_2_bytes=True):
        pattern = '{:04x}' if is_2_bytes else '{:02x}'
        return pattern.format(number)

    def get_formatted_length(self):
        return self._format_numbers(len(self.data))

    def checksum(self):
        # TODO implementar
        return self._format_numbers(0)

    def get_formatted_id(self):
        return self._format_numbers(self.id, False)

    def get_formatted_flags(self):
        return self._format_numbers(self.flags, False)

    # encrypt
    def encode16(self):
        return binascii.hexlify(self.data.encode())

    # decrypt
    def decode16(self):
        return binascii.unhexlify(self.data).decode()

    def get_frame(self):
        length = self.get_formatted_length()
        checksum = self.checksum()
        id = self.get_formatted_id()
        flags = self.get_formatted_flags()
        encoded_data = self.encode16()
        header = (length + checksum + id + flags).encode()
        return header + encoded_data


data_to_send = DataTransfer()
data_to_receive = DataTransfer(id=0)


class AckTimeoutError(Exception):
    pass


def handle_ack_timeout(*_):
    raise AckTimeoutError()


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

    print(datetime.datetime.now(), 'Server running on port', port)
    connection = s.accept()[0]

    # TODO multithread
    # receive_data(connection, output_file_name)
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

    # TODO multithread
    receive_data(connection, output_file_name)
    # send_data(connection, input_file_name)

    connection.close()
    print('Done')


# function to send data from file
def send_data(connection, file_name):
    with open(file_name) as file:
        file_line = file.readline(MAX_LENGTH)

        while file_line:
            data_to_send.data = file_line
            data_to_send.prepare_for_new_data()

            connection.send(SYNC.encode())
            connection.send(SYNC.encode())
            connection.send(data_to_send.get_frame())
            print(datetime.datetime.now(), 'Data sent from file', file_name)

            signal.signal(signal.SIGALRM, handle_ack_timeout)
            signal.alarm(1)
            try:
                while True:
                    if data_to_send.confirmed:
                        file_line = file.readline(MAX_LENGTH)
                        break
            except AckTimeoutError:
                print(datetime.datetime.now(), 'ACK not received')
            signal.alarm(0)


def receive_data(connection, file_name):
    while True:
        print(datetime.datetime.now(), 'Waiting for data')

        sync = connection.recv(8)
        if sync.decode() != SYNC:
            print(datetime.datetime.now(), 'Resynchronizing')
            continue

        sync = connection.recv(8)
        if sync.decode() != SYNC:
            print(datetime.datetime.now(), 'Resynchronizing')
            continue

        length = connection.recv(4)
        data_to_receive.length = int(length.decode(), base=16)

        checksum = connection.recv(4)
        data_to_receive.checksum = int(checksum.decode(), base=16)

        id = connection.recv(2)
        data_to_receive.id = int(id.decode(), base=16)

        flags = connection.recv(2)
        data_to_receive.flags = int(flags.decode(), base=16)

        data = connection.recv(2*length)
        print('DATA:', data)

        if flags == 128:
            # tratar ACK recebido
            pass

    # data1 = connection.recv(2)
    # test_length = struct.unpack('!H', data1)[0]
    # print(test_length)
    # # ler o htons: struct.unpack('!H', data1)[0]
    #
    # print('Esperando dados2:')
    # data2 = connection.recv(test_length)
    # print(data2.decode())
    #
    # print('Received data saved on file', file_name)
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
