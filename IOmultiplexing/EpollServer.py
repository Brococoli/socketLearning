import select
import socket

def EpollServer(addr):
	server_socket = socket.socket()
	server_socket.bind(addr)
	server_socket.listen(10)

	server_socket.setblocking(False)

	epoll = select.epoll()
	epoll = register(server_socket.fileno(), select.EPOLLIN)

	try:
		fdmap = {}
		readList = {}
		SendList = {}

		while True:
			events = epoll.poll(1)
			for fileno, event in events:
				sock = fdmap[fileno]
				if sock is server_socket:
					client_socket, client_addr = server_socket.accept()
					print('Got connection from', client_addr)

					client_socket.setblocking(False)
					client_fileno = client_socket.fileno()

					epoll.register(client_fileno, select.EPOLLIN)
					fdmap[client_fileno] = client_socket
					readList[client_fileno] = b''

				elif event & select.EPOLLIN:
					data = sock.recv(1024)
					readList[fileno] = data
					print('Received {} from {}'.format(data, sock.getpeername()))

					if not data:
						del fdmap[fileno]
						del readList[fileno]
						print('Close connection from', sock.getpeername())
						sock.close()
						epoll.modify(fileno, 0)

					else:
						epoll.modify(fileno, select.EPOLLOUT)

				elif event & select.EPOLLOUT:
					response = readList[fileno]
					sock.sendall(response)

					epoll.modify(fileno, select.EPOLLIN)

				elif event & select.EPOLLHUP:
					print('End Hup from', sock.getpeername())

					epoll.unregister(fileno)
					sock.close()
					del fdmap[fileno]
	finally:
		epoll.unregister(server_socket.fileno())
		epoll.close()
		server_socket.close()

if __name__ == '__main__':
	addr = '', 8888
	EpollServer(addr)


	