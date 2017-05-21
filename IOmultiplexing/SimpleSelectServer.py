# 来自「Python基础教程」

""" 
socket是同步,会阻塞, select是I/O复用, 和阻塞I/O所不同的的，这两个函数可以同时阻塞多个I/O操作。
而且可以同时对多个读操作，多个写操作的I/O函数进行检测，直到有数据可读或可写时，才真正调用I/O操作函数。
"""
# 只能接受信息
import socket, select

server_socket = socket.socket()

addr = '', 8888

server_socket.bind(addr)
server_socket.listen()

readTodo = [server_socket]
while True:
	readList, writeList, errorList = select.select(readTodo, [], [])

	for sock in readList:
		if sock is server_socket:
			client_socket, client_addr = server_socket.accept()
			print('Got connection from', client_addr)
			readTodo.append(client_socket)

		else:
			try:
				data = sock.recv(1024)
				disconnected = not data

			except socket.error:
				disconnected = True

			if disconnected:
				print(sock.getpeername(), 'disconnected')
				readTodo = remove(sock)
			else:
				print(data)