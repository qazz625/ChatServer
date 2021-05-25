import socket
import threading
import time

PORT = 5052
SERVER = "localhost"
ADDR = (SERVER, PORT)
HEADER = 64

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

active = {}

print("Server is starting")
print(f'Server is listening on {SERVER}')


def send_others(msg):
	msg = msg.encode('utf-8')
	# print(msg, type(msg))
	for x in active:
		x[0].sendall(msg)


def handle_client(conn, addr):
	print(addr, "has connected")
	connected = True
	while connected:
		msg_len = conn.recv(HEADER).decode('utf-8').strip()
		if msg_len:
			msg_len = int(msg_len)
			msg = conn.recv(HEADER).decode('utf-8').strip()
			print(msg)
			if len(msg.split()) == 2 and msg.split()[-1] == "QUIT":
				connected = False
				msg = str(addr) + ' has left'
				del active[(conn, addr)]
			# print(addr, msg)
			send_others(msg)
	print('closing a connection')
	conn.close()

def initializeUname(conn, addr):
	uname = conn.recv(HEADER).decode('utf-8').strip()
	active[(conn, addr)] = uname
	# print(active)
	thread = threading.Thread(target=handle_client, args=(conn, addr))
	thread.start()



def start():
	server.listen()
	while True:
		conn, addr = server.accept()
		print("NEW CONNECTION")
		send_others(str(addr) + ' has connected')
		initializeUname(conn, addr)
		
start()

