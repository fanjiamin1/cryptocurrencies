import socket
import sys
import pychat

HOST = ''
PORT = 8898
KEY = 89

def bob():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Server socket, go Bob!')

    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print(str(msg[0]))
        sys.exit()

    print('Bob is binded')
    s.listen(2)
    print('Bob is listening')

    while 1:
        conn, addr = s.accept()
        print('Bob is connected with ' + addr[0] + ':' + str(addr[1]))
        data = conn.recv(1024)
        if not data:
            break
        print("Received", pychat.decrypt(KEY, data))

    conn.close()
    s.close()
