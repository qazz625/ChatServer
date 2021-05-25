import socket
import threading
import time

uname = input("Enter your username: ")

PORT = 5052
SERVER = "localhost"
ADDR = (SERVER, PORT)
HEADER = 64

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
connected = True

def send():
	global connected
	while connected:
		msg = input()
		msg = uname + ': ' + msg
		message = msg.encode('utf-8')
		msg_len = len(message)
		send_length = str(msg_len).encode('utf-8')
		send_length += b' ' * (HEADER-len(send_length))
		client.send(send_length)
		client.send(message)
		time.sleep(0.2)
		if len(msg.split()) == 2 and msg.split()[-1] == "QUIT":
			connected = False
			break

def recv():
	global connected
	while connected:
		msg = client.recv(HEADER).decode('utf-8').strip()
		if len(msg):
			print(msg)

client.send(uname.encode('utf-8'))

send_thread = threading.Thread(target=send, args=())
send_thread.start()
recv_thread = threading.Thread(target=recv, args=())
recv_thread.start()
send_thread.join()





