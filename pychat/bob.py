import socket
import sys

HOST = ''
PORT = 8898

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
	reply = 'Received' + data
	if not data:
		break

	conn.sendall(reply)

conn.close()
s.close()