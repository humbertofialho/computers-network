# --------------------------------------------------------------------------- #
# ---------------------- Engenharia de Sistemas - UFMG ---------------------- #
# ----------------------- DCC023 - Redes de Computadores -------------------- # 
# --------------------- Prof. Ítalo Fernando Scota Cunha -------------------- #
# ------------------------ Trabalho Prático I - DCCNET ---------------------- #
# ----------- Alunos :   Humberto Monteiro Fialho   (2013430811) ------------ #
# --------------------   Rafael Carneiro de Castro  (2013030210) ------------ #
# --------------------------------------------------------------------------- #

# libraries
import os
import sys
import binascii
import datetime
import threading
import socket as sck

MAX_LENGTH = 65000
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

    def checksum(self):
        data = 2 * SYNC
        data += self._format_numbers(len(self.data))
        data += self._format_numbers(0)
        data += self._format_numbers(self.id, False)
        data += self._format_numbers(self.flags, False)
        encoded_data = self.encode16()
        data = data.encode() + encoded_data

        checksum = 0
        pointer = 0
        size = len(data)

        while size > 1:
            checksum += int(str('%02x' % (data[pointer],)) + str('%02x' % (data[pointer + 1],)), 16)
            size -= 2
            pointer += 2
        if size:
            checksum += data[pointer]

        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum += (checksum >> 16)

        return (~checksum) & 0xFFFF

    # encrypt
    def encode16(self):
        return binascii.hexlify(self.data)

    # decrypt
    def decode16(self, new_data):
        self.data = binascii.unhexlify(new_data)

    def get_frame(self):
        formatted_length = self._format_numbers(len(self.data))
        formatted_checksum = self._format_numbers(self.checksum())
        formatted_id = self._format_numbers(self.id, False)
        formatted_flags = self._format_numbers(self.flags, False)
        encoded_data = self.encode16()
        header = (formatted_length + formatted_checksum + formatted_id + formatted_flags).encode()
        return header + encoded_data


# global variables
data_to_send = DataTransfer(id=0)
data_to_receive = DataTransfer()
ack_timeout = False


def log(message):
    print('[', threading.currentThread().getName(), ']', datetime.datetime.now(), message)


# start the code as server
def initialize_server():
    # reading inputs
    ip = '127.0.0.1'
    port = int(sys.argv[2])
    input_file_name = sys.argv[3]
    output_file_name = sys.argv[4]

    if os.path.exists(output_file_name):
        os.remove(output_file_name)

    # starting socket with standard protocol
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(1)

    log('Server running on port ' + str(port))
    connection = s.accept()[0]

    # starting one thread to send and other to receive
    send_thread = threading.Thread(target=send_data, args=(connection, input_file_name))
    send_thread.start()
    receive_thread = threading.Thread(target=receive_data, args=(connection, output_file_name))
    receive_thread.start()


# start the code as client
def initialize_client():
    # reading inputs
    ip = sys.argv[2].split(':')[0]
    port = int(sys.argv[2].split(':')[1])
    input_file_name = sys.argv[3]
    output_file_name = sys.argv[4]

    # deleting output file before to use, if exist
    if os.path.exists(output_file_name):
        os.remove(output_file_name)

    connection = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    connection.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
    connection.connect((ip, port))

    # starting one thread to send and other to receive
    send_thread = threading.Thread(target=send_data, args=(connection, input_file_name))
    send_thread.start()
    receive_thread = threading.Thread(target=receive_data, args=(connection, output_file_name))
    receive_thread.start()


# function to send data from file
def send_data(connection, file_name):
    with open(file_name, 'rb') as file:
        file_line = file.read(MAX_LENGTH)

        while file_line:
            data_to_send.data = file_line

            connection.send(SYNC.encode())
            connection.send(SYNC.encode())
            connection.send(data_to_send.get_frame())
            log('Data sent from file ' + file_name)

            global ack_timeout
            ack_timeout = False

            def handle_timeout():
                global ack_timeout
                ack_timeout = True

            # to measure time
            timer = threading.Timer(1, handle_timeout)
            timer.start()
            while True:
                if ack_timeout:
                    log('ACK not received.')
                    break

                if data_to_send.confirmed:
                    file_line = file.read(MAX_LENGTH)
                    data_to_send.prepare_for_new_data()
                    break


# function to receive data from file
def receive_data(connection, file_name):
    last_received_id = 1

    while True:
        log('Waiting for data.')

        # finding SYNC expression
        sync = connection.recv(8)
        if sync.decode() != SYNC:
            log('Resynchronizing...')
            continue

        sync = connection.recv(8)
        if sync.decode() != SYNC:
            log('Resynchronizing...')
            continue

        # collecting information in the string
        length = connection.recv(4)
        data_to_receive.length = int(length.decode(), base=16)

        received_checksum = connection.recv(4)
        received_checksum = int(received_checksum.decode(), base=16)

        id = connection.recv(2)
        data_to_receive.id = int(id.decode(), base=16)

        flags = connection.recv(2)
        data_to_receive.flags = int(flags.decode(), base=16)

        try:
            data = connection.recv(2*data_to_receive.length)
            data_to_receive.decode16(data)
        except binascii.Error or UnicodeDecodeError:
            log('Conversion error!')
            continue

        # verifying checksum value
        if data_to_receive.checksum() != received_checksum:
            log('Checksum error!')
            continue

        if data_to_receive.flags == 128:
            # treat received ACK
            if data_to_receive.id == data_to_send.id:
                log('ACK received.')
                data_to_send.confirmed = True

        else:
            # treat new data
            expected_id = 1 if last_received_id == 0 else 0
            if data_to_receive.id != expected_id:
                log('Retransmission data, resending ACK.')
                data_to_receive.data = b''
                data_to_receive.flags = 128

                connection.send(SYNC.encode())
                connection.send(SYNC.encode())
                connection.send(data_to_receive.get_frame())
                continue

            with open(file_name, 'ab') as file:
                file.write(data_to_receive.data)
                log('Data written on file {}, sending ACK.'.format(file_name))
                data_to_receive.data = b''
                data_to_receive.flags = 128
                last_received_id = data_to_receive.id

                connection.send(SYNC.encode())
                connection.send(SYNC.encode())
                connection.send(data_to_receive.get_frame())


# main: calling functions to receive inputs
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
