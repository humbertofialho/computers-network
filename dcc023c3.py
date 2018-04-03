# --------------------------------------------------------------------------- #
# ---------------------- Engenharia de Sistemas - UFMG ---------------------- #
# ----------------------- DCC023 - Redes de Computadores -------------------- # 
# --------------------- Prof. Ítalo Fernando Scota Cunha -------------------- #
# ------------------------ Trabalho Prático I - DCCNET ---------------------- #
# ----------- Alunos :   Humberto Monteiro Fialho   (2013430811) ------------ #
# -----------            Rafael Carneiro de Castro  (2013XXXXXX) ------------ #
# --------------------------------------------------------------------------- #

# librarys
from socket import *

# codification
def encrypt(number):
     binary = bin(number)
     binary = binary[2:len(binary)]
     binaryInt = int(binary)
return binaryInt;

def decrypt(number):
     decimal = dec(number)
     decimal = decimal[2:len(decimal)]
     decimalInt = int(decimal)
return decimalInt;

# framework
def framework ():
    
return 0;

# error detection
def errorDetection ():
    
return 0;

# sequencing
def sequencing():
    
return 0;

#  retransmission
def retransmission ():
    
return 0;

# main
def main ():
    
    # reading inputs
    ip = 
    port = 
    Input = 
    output = 
    
    
    # starting socket with standard protocol = 0
    s = socket(AF_INET, SOCK_STREAM)
    # server and port
    s.bind(ip, port)
    
    
return;
    

# --------------------------------------------------------------------------- #

if __name__ == '__main__': # calling main function
    main()