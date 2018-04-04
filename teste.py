import socket as sck


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect(('127.0.0.1', 5050))
    print('Mandando')
    resp = s.send('abcd'.encode())
    print('RESPOSTA:')
    print(resp)


    print('Mandando2')
    resp = s.send('efgh'.encode())
    print('RESPOSTA2:')
    print(resp)

    s.close()
    print('Done')


if __name__ == '__main__': # calling main function
    main()