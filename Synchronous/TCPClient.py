import socket

addr = 'localhost', 8888

client_socket = socket.socket()
client_socket.connect(addr)


# while True:
	
	

print('Client has connected!', client_socket.getpeername())
recv = client_socket.recv(1024) # 服务器的socket的数据: Receive data from the socket.
if not recv:
	print('Not recv anything, connect again!')
else:
	print('recv: ' + str(recv, 'utf-8'))


terminal = '\r\n'
data = input('What you wants to say?  ')
client_socket.sendall(bytes(data, 'utf-8'))
data = input('What you wants to say?  ')
client_socket.sendall(bytes(data, 'utf-8'))
client_socket.sendall(bytes(terminal, 'utf-8'))

recv = client_socket.recv(1024) # 服务器的socket的数据: Receive data from the socket.
if not recv:
	print('Not recv anything, connect again!')
else:
	print('recv: ' + str(recv, 'utf-8'))


client_socket.close()

