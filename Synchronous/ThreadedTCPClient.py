import socket,time

def client(addr, message):
	with socket.socket() as client_socket:
		client_socket.connect(addr)
		client_socket.sendall(bytes(message, 'utf-8'))
		response = client_socket.recv(1024)
		print('Received: {}'.format(str(response, 'utf-8')))

if __name__ == '__main__':
	addr = 'localhost', 8888

	
	# message = input('What do you want to say?   ')
	message = 'Hello !'
	client(addr, message)
