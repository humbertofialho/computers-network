# --------------------------------------------------------------------------- #
# ---------------------- Engenharia de Sistemas - UFMG ---------------------- #
# ----------------------- DCC023 - Redes de Computadores -------------------- # 
# --------------------- Prof. Ítalo Fernando Scota Cunha -------------------- #
# ------------------------ Trabalho Prático I - DCCNET ---------------------- #
# ----------- Alunos :   Humberto Monteiro Fialho   (2013430811) ------------ #
# -----------            Rafael Carneiro de Castro  (2013030210) ------------ #
# --------------------------------------------------------------------------- #

# librarys
import socket as sck


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
    # reading inputs
    ip = '127.0.0.1'
    port = 5050
    # input =
    # output =


    # starting socket with standard protocol = 0
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    # server and port
    s.bind((ip, port))
    s.listen(1)
    print('Servidor na porta 5050')
    connection = s.accept()[0]

    print('Esperando dados:')
    data1 = connection.recv(8)
    print(data1)
    print(type(data1))
    # data2 = connection.recv(4)
    # print(data2)

    return


# --------------------------------------------------------------------------- #
if __name__ == '__main__': # calling main function
    main()