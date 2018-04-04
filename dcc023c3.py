# --------------------------------------------------------------------------- #
# ---------------------- Engenharia de Sistemas - UFMG ---------------------- #
# ----------------------- DCC023 - Redes de Computadores -------------------- # 
# --------------------- Prof. Ítalo Fernando Scota Cunha -------------------- #
# ------------------------ Trabalho Prático I - DCCNET ---------------------- #
# ----------- Alunos :   Humberto Monteiro Fialho   (2013430811) ------------ #
# -----------            Rafael Carneiro de Castro  (2013030210) ------------ #
# --------------------------------------------------------------------------- #

# librarys
import sys
import socket as sck


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
    data1 = connection.recv(4)
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
    print('Mandando')
    resp = s.send('abcdefgh'.encode())
    print('RESPOSTA:')
    print(resp)


    # print('Mandando2')
    # resp = s.send('efgh'.encode())
    # print('RESPOSTA2:')
    # print(resp)

    s.close()
    print('Done')


# codification
def encrypt(number):
    binary = bin(number)
    binary = binary[2:len(binary)]
    binary_int = int(binary)

    # ascii = ord('a')
    # bin(ascii)
    # hex(110)
    # int('d', 16)

    return binary_int


def decrypt(number):
    decimal = int(number)
    decimal = decimal[2:len(decimal)]
    decimal_int = int(decimal)
    return decimal_int


# framework
def framework():
    pass


# error detection
def error_detection():
    pass


# sequencing
def sequencing():
    pass


#  retransmission
def retransmission():
    pass


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
